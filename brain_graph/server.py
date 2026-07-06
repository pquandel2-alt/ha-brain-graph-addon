"""Brain Graph Add-on backend.

Verbindet sich via Supervisor-Token mit HA Core (WebSocket + REST),
baut den Entitäten-Graphen und streamt Live-Events an den Browser.
"""

import asyncio
import json
import logging
import os

from aiohttp import ClientSession, WSMsgType, web

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
_LOG = logging.getLogger("brain_graph")

SUPERVISOR_TOKEN = os.environ.get("SUPERVISOR_TOKEN", "")
CORE_WS = "ws://supervisor/core/websocket"
CORE_API = "http://supervisor/core/api"
PORT = 8099

VALID_DESIGNS = {"free", "kaskade", "radial", "puls-kaskade", "sonar-halo"}


def _load_design_option():
    """Liest die vom Nutzer in der Add-on-Konfiguration gewählte Design-Option
    aus /data/options.json (Supervisor-Konvention). Fällt auf "free" zurück,
    falls die Datei fehlt (z. B. lokaler Testlauf ohne Supervisor)."""
    try:
        with open("/data/options.json", encoding="utf-8") as f:
            options = json.load(f)
        design = options.get("design", "free")
        return design if design in VALID_DESIGNS else "free"
    except (FileNotFoundError, json.JSONDecodeError, OSError) as exc:
        _LOG.warning("Could not read /data/options.json (%s) — using default design", exc)
        return "free"


DESIGN = _load_design_option()

ACTIVE_STATES = {"on", "playing", "running", "active", "home", "open"}

NODE_COLORS = {
    "ha-core": "#f97316",
    "floor": "#8b5cf6",
    "area": "#3b82f6",
    "device": "#06b6d4",
    "light": "#fbbf24",
    "switch": "#34d399",
    "sensor": "#94a3b8",
    "automation": "#f472b6",
    "script": "#a78bfa",
    "binary_sensor": "#6b7280",
    "media_player": "#ef4444",
}


def _extract_entity_ids(value):
    """Extrahiert entity_ids (String oder Liste) aus Trigger/Action-Feldern."""
    result = []
    if isinstance(value, str):
        result.append(value)
    elif isinstance(value, list):
        for v in value:
            if isinstance(v, str):
                result.append(v)
    return result


class HAClient:
    """Persistente WebSocket-Verbindung zu HA Core."""

    def __init__(self, session: ClientSession):
        self.session = session
        self.ws = None
        self._id = 0
        self._futures = {}
        self._event_cbs = {}
        self.browser_clients: set = set()
        self._loop = None

    async def connect(self):
        self._loop = asyncio.get_event_loop()
        self.ws = await self.session.ws_connect(CORE_WS, heartbeat=30, max_msg_size=0)

        msg = await self.ws.receive_json()
        if msg.get("type") != "auth_required":
            raise RuntimeError(f"Unexpected first message: {msg}")

        await self.ws.send_json({"type": "auth", "access_token": SUPERVISOR_TOKEN})
        msg = await self.ws.receive_json()
        if msg.get("type") != "auth_ok":
            raise RuntimeError(f"Auth failed: {msg}")

        asyncio.create_task(self._reader())
        _LOG.info("Connected and authenticated to HA Core")

    async def _reader(self):
        try:
            async for m in self.ws:
                if m.type != WSMsgType.TEXT:
                    continue
                data = json.loads(m.data)
                t = data.get("type")
                if t == "result":
                    fut = self._futures.pop(data["id"], None)
                    if fut and not fut.done():
                        fut.set_result(data)
                elif t == "event":
                    cb = self._event_cbs.get(data["id"])
                    if cb:
                        cb(data.get("event", {}))
        except Exception as exc:  # noqa: BLE001
            _LOG.error("Reader loop ended: %s", exc)

    async def cmd(self, payload: dict):
        self._id += 1
        i = self._id
        payload = {**payload, "id": i}
        fut = self._loop.create_future()
        self._futures[i] = fut
        await self.ws.send_json(payload)
        res = await fut
        if not res.get("success", False):
            raise RuntimeError(f"Command failed: {payload.get('type')} -> {res}")
        return res["result"]

    async def subscribe(self, event_type: str, cb):
        self._id += 1
        i = self._id
        self._event_cbs[i] = cb
        fut = self._loop.create_future()
        self._futures[i] = fut
        await self.ws.send_json({"id": i, "type": "subscribe_events", "event_type": event_type})
        await fut
        _LOG.info("Subscribed to %s", event_type)

    async def rest_get(self, path: str):
        headers = {"Authorization": f"Bearer {SUPERVISOR_TOKEN}"}
        try:
            async with self.session.get(f"{CORE_API}{path}", headers=headers) as r:
                if r.status != 200:
                    return None
                return await r.json()
        except Exception as exc:  # noqa: BLE001
            _LOG.warning("REST GET %s failed: %s", path, exc)
            return None

    def broadcast(self, message: dict):
        """Event an alle verbundenen Browser-Clients senden."""
        if not self.browser_clients:
            return
        payload = json.dumps(message)
        for ws in list(self.browser_clients):
            if ws.closed:
                self.browser_clients.discard(ws)
                continue
            asyncio.create_task(self._safe_send(ws, payload))

    async def _safe_send(self, ws, payload):
        try:
            await ws.send_str(payload)
        except Exception:  # noqa: BLE001
            self.browser_clients.discard(ws)


async def build_graph(client: HAClient) -> dict:
    """Baut das Graph-Datenmodell aus allen HA-Registries."""
    states = await client.cmd({"type": "get_states"})
    devices = await client.cmd({"type": "config/device_registry/list"})
    areas = await client.cmd({"type": "config/area_registry/list"})
    entity_reg = await client.cmd({"type": "config/entity_registry/list"})

    _LOG.info(
        "Loaded: %d states, %d devices, %d areas, %d entities",
        len(states), len(devices), len(areas), len(entity_reg),
    )

    nodes = []
    links = []
    node_ids = set()

    def add_node(node):
        if node["id"] not in node_ids:
            nodes.append(node)
            node_ids.add(node["id"])

    # Layer 0: HA Core Hub
    add_node({"id": "ha-core", "label": "Home Assistant", "type": "ha-core", "val": 8})

    # Layer 1: Areas (direkt unter HA-Core — Etagen werden nicht genutzt)
    for area in areas:
        aid = f"area-{area['area_id']}"
        add_node({"id": aid, "label": area.get("name", aid), "type": "area", "val": 4})
        links.append({"source": "ha-core", "target": aid, "rel_type": "contains"})

    # Layer 3: Devices
    for device in devices:
        did = f"device-{device['id']}"
        label = device.get("name_by_user") or device.get("name") or did
        add_node({"id": did, "label": label, "type": "device", "val": 3})
        parent = f"area-{device['area_id']}" if device.get("area_id") else "ha-core"
        links.append({"source": parent, "target": did, "rel_type": "contains"})

    # Layer 4: Entities
    entity_reg_map = {e["entity_id"]: e for e in entity_reg}
    for state in states:
        entity_id = state["entity_id"]
        domain = entity_id.split(".")[0]
        reg = entity_reg_map.get(entity_id, {})
        attrs = state.get("attributes", {})

        add_node({
            "id": entity_id,
            "label": attrs.get("friendly_name", entity_id),
            "type": domain,
            "state": state.get("state"),
            "val": 1.5,
        })

        if reg.get("device_id"):
            links.append({"source": f"device-{reg['device_id']}", "target": entity_id, "rel_type": "contains"})
        elif reg.get("area_id"):
            links.append({"source": f"area-{reg['area_id']}", "target": entity_id, "rel_type": "contains"})
        else:
            links.append({"source": "ha-core", "target": entity_id, "rel_type": "contains"})

    # Automation-Flows: Trigger/Action-Kanten aus Konfigs parsen
    automation_states = [s for s in states if s["entity_id"].startswith("automation.")]
    for state in automation_states:
        entity_id = state["entity_id"]
        aid = state.get("attributes", {}).get("id")
        if not aid:
            continue
        config = await client.rest_get(f"/config/automation/config/{aid}")
        if not config:
            continue

        # Trigger (HA nutzt 'trigger' oder 'triggers')
        triggers = config.get("triggers") or config.get("trigger") or []
        if isinstance(triggers, dict):
            triggers = [triggers]
        for trig in triggers:
            if not isinstance(trig, dict):
                continue
            for eid in _extract_entity_ids(trig.get("entity_id")):
                if eid in node_ids:
                    links.append({"source": eid, "target": entity_id, "rel_type": "triggers", "isFlowEdge": True})

        # Action (HA nutzt 'action' oder 'actions')
        actions = config.get("actions") or config.get("action") or []
        if isinstance(actions, dict):
            actions = [actions]
        for act in actions:
            if not isinstance(act, dict):
                continue
            eids = _extract_entity_ids(act.get("entity_id"))
            target = act.get("target", {})
            if isinstance(target, dict):
                eids += _extract_entity_ids(target.get("entity_id"))
            for eid in eids:
                if eid in node_ids:
                    links.append({"source": entity_id, "target": eid, "rel_type": "controls", "isFlowEdge": True})

    _LOG.info("Graph built: %d nodes, %d links", len(nodes), len(links))
    return {"nodes": nodes, "links": links}


# ---------------------------------------------------------------------------
# HTTP Routes
# ---------------------------------------------------------------------------

async def handle_index(request):
    return web.FileResponse("/www/index.html")

async def handle_graph(request):
    client: HAClient = request.app["ha"]
    try:
        graph = await build_graph(client)
        graph["design"] = DESIGN
        return web.json_response(graph)
    except Exception as exc:  # noqa: BLE001
        _LOG.error("build_graph failed: %s", exc)
        return web.json_response({"error": str(exc), "nodes": [], "links": []}, status=500)

async def handle_live(request):
    client: HAClient = request.app["ha"]
    ws = web.WebSocketResponse(heartbeat=30)
    await ws.prepare(request)
    client.browser_clients.add(ws)
    _LOG.info("Browser client connected (%d total)", len(client.browser_clients))
    try:
        async for _ in ws:
            pass
    finally:
        client.browser_clients.discard(ws)
        _LOG.info("Browser client disconnected (%d total)", len(client.browser_clients))
    return ws


async def on_startup(app):
    session = ClientSession()
    app["session"] = session
    client = HAClient(session)
    app["ha"] = client
    await client.connect()

    def on_state_changed(event):
        data = event.get("data", {})
        new_state = data.get("new_state") or {}
        client.broadcast({
            "type": "state_changed",
            "entity_id": data.get("entity_id"),
            "state": new_state.get("state"),
        })

    def on_automation_triggered(event):
        data = event.get("data", {})
        client.broadcast({
            "type": "automation_triggered",
            "entity_id": data.get("entity_id"),
        })

    await client.subscribe("state_changed", on_state_changed)
    await client.subscribe("automation_triggered", on_automation_triggered)


async def on_cleanup(app):
    session = app.get("session")
    if session:
        await session.close()


def main():
    if not SUPERVISOR_TOKEN:
        _LOG.error("No SUPERVISOR_TOKEN found — cannot connect to HA Core")

    app = web.Application()
    app.router.add_get("/", handle_index)
    app.router.add_get("/api/graph", handle_graph)
    app.router.add_get("/api/live", handle_live)
    app.router.add_static("/", "/www")
    app.on_startup.append(on_startup)
    app.on_cleanup.append(on_cleanup)

    _LOG.info("Brain Graph server listening on 0.0.0.0:%d", PORT)
    web.run_app(app, host="0.0.0.0", port=PORT, print=None)


if __name__ == "__main__":
    main()
