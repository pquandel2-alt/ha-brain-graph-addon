# Home

Nach dem Start öffnet sich „Brain Graph" in der Sidebar. Der 3D-Graph lädt automatisch alle Entitäten deiner Installation.

## Bedienung

- **Ziehen**: Kamera rotieren (Auto-Rotation stoppt bei Interaktion, setzt danach wieder ein)
- **Scrollen**: Zoomen
- **Klick auf Knoten**: Details anzeigen, Kamera fokussiert
- **Filter-Chips oben links**: Nach Domain filtern

## Screensaver-/Kiosk-Modus

Hänge `?kiosk` (oder `?screensaver`) an die URL an — dann verschwinden Filter, Legende
und Status, und nur der rotierende, glühende Graph bleibt. Ideal für Wand-Tablets oder als
ambienter Screensaver auf einem Dashboard.

Einbindung in ein Lovelace-Dashboard als Vollbild-Kachel (Beispiel `iframe`-Karte):

```yaml
type: iframe
url: /api/hassio_ingress/<DEIN-INGRESS-TOKEN>/?kiosk
aspect_ratio: 100%
```

Den Ingress-Pfad findest du, wenn du das Panel öffnest (URL in der Adressleiste). In
Kombination mit HACS-Karten wie **wallpanel** oder **browser_mod** lässt sich der Graph
auch als Idle-Screensaver einblenden.

## Troubleshooting

Logs: Add-on-Seite → Tab „Log". Suche nach `[BrainGraph]` oder Python-Tracebacks.

Wenn der Graph leer bleibt: Prüfe im Log, ob `Graph built: N nodes` erscheint. Bei 0 Knoten: Supervisor-Token-Problem — Add-on neu starten.
