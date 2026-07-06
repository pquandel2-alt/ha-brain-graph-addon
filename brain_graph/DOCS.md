# Home

Nach dem Start öffnet sich „Brain Graph" in der Sidebar. Der 3D-Graph lädt automatisch alle Entitäten deiner Installation.

## Bedienung

- **Ziehen**: Kamera rotieren (Auto-Rotation stoppt bei Interaktion, setzt danach wieder ein)
- **Scrollen**: Zoomen
- **Klick auf Knoten**: Details anzeigen, Kamera fokussiert
- **Filter-Chips oben links**: Nach Domain filtern
- **Layout-Design**: wird über die Add-on-Konfiguration eingestellt (siehe unten)

## Layout-Designs

Das Layout wird nicht im Graph selbst, sondern über die Add-on-Konfiguration
gewählt: Home Assistant → Einstellungen → Add-ons → Brain Graph → Tab
„Konfiguration" → Option `design`. Nach dem Speichern das Add-on neu starten,
damit die Änderung greift.

Verfügbare Werte:

- **free** (Frei) — das ursprüngliche freie Kräfte-Layout
- **kaskade** (Ebenen-Kaskade) — Hierarchie als Wasserfall von oben (HA-Core)
  nach unten (Etage → Bereich → Gerät → Entität), Etagen/Bereiche beschriftet
- **radial** (Radial-Halo) — dieselbe Hierarchie als konzentrische Ringe um den HA-Core
- **puls-kaskade** / **sonar-halo** — wie oben, aber ohne dauerhaften
  Hintergrund-Partikelstrom: nur echte Live-Aktivierungen sind sichtbar

In allen Designs gilt: aktiviert sich eine Entität, fließt der Datenstrom sichtbar
Hop für Hop über die echten Verbindungen nach oben bis zum HA-Core — nicht nur der
einzelne Knoten leuchtet auf.

Für Kiosk/Screensaver lässt sich das konfigurierte Design per URL zusätzlich
überschreiben: `&design=kaskade` (oder `radial`, `puls-kaskade`, `sonar-halo`,
`free`), z. B. `?kiosk&design=sonar-halo`.

## Screensaver-/Kiosk-Modus

Hänge `?kiosk` (oder `?screensaver`) an die URL an — dann verschwinden Filter, Legende
und Status, und nur der rotierende, glühende Graph bleibt. Ideal für Wand-Tablets oder als
ambienter Screensaver auf einem Dashboard.

Im Kiosk-Modus verwendet die Kamera einen festen Abstand (Default 2200), statt sich nach
der Kräfte-Simulation automatisch einzupassen — auf schwächerer Hardware (Tablets) kann
die Simulation bei großen Graphen lange brauchen, ein fester Abstand ist sofort korrekt.
Passe ihn bei Bedarf über `&zoom=<Zahl>` an, z. B. `?kiosk&zoom=2800` für weiter draußen
oder `?kiosk&zoom=1600` für näher dran.

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
