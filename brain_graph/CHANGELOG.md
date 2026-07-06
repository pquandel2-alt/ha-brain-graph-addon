## 1.4.0

- Kamera zoomt nach dem Einpendeln der Kräfte-Simulation automatisch heraus
  (`zoomToFit`), damit bei großen Graphen (1000+ Knoten) immer der komplette
  Graph sichtbar ist statt eines zu nah herangezoomten Ausschnitts
- Fallback-Timeout (5s), falls die Simulation bei sehr großen Graphen ungewöhnlich
  lange braucht, um vollständig zu stoppen

## 1.3.0

- Fester LAN-Port 8099 (zusätzlich zu Ingress): stabile iframe-Einbindung ohne
  rotierenden Token — ideal als Screensaver auf dem Wandtablet unter
  http://<HA-IP>:8099/?kiosk

## 1.2.0

- Hintergrund wieder tiefschwarz — Bloom-Schwelle erhöht (0.35), Radius verkleinert (0.35):
  nur wirklich helle/aktive Knoten glühen, der graue Schleier durch tausende dimme Knoten ist weg
- Screensaver-/Kiosk-Modus: URL-Parameter `?kiosk` oder `?screensaver` blendet alle
  Bedien-Elemente aus und zeigt nur den rotierenden, glühenden Graphen (für Wand-Displays/Dashboards)

## 1.1.0

- Neon-Glühen (Bloom-Postprocessing) für die gesamte Szene — deutlich beeindruckendere Optik
- Datenflüsse dauerhaft sichtbar: Flow-Kanten strömen permanent mit sanften Partikeln (Hintergrund-Prozesse)
- Richtungspfeile auf Flow-Kanten zeigen woher → wohin
- Trigger-Burst: löst eine Automation aus, schießen helle schnelle Partikel, Quell- und Zielknoten flashen hell auf
- Hellere Struktur-Kanten und größere Hub-Knoten für bessere Lesbarkeit
- Einschalten einer Entität poppt jetzt sichtbar auf

## 1.0.0

- Initial release: Standalone 3D Brain Graph als HA Add-on mit Ingress
- Live-Datenfluss-Animation für Automations-Trigger
- Ersetzt die frühere Panel-Custom-Integration (Rendering-Probleme im Shadow DOM)
