# Home

Nach dem Start öffnet sich „Brain Graph" in der Sidebar. Der 3D-Graph lädt automatisch alle Entitäten deiner Installation.

## Bedienung

- **Ziehen**: Kamera rotieren (Auto-Rotation stoppt bei Interaktion, setzt danach wieder ein)
- **Scrollen**: Zoomen
- **Klick auf Knoten**: Details anzeigen, Kamera fokussiert
- **Filter-Chips oben links**: Nach Domain filtern

## Troubleshooting

Logs: Add-on-Seite → Tab „Log". Suche nach `[BrainGraph]` oder Python-Tracebacks.

Wenn der Graph leer bleibt: Prüfe im Log, ob `Graph built: N nodes` erscheint. Bei 0 Knoten: Supervisor-Token-Problem — Add-on neu starten.
