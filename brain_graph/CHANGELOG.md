## 1.9.0

- Der Graph ist jetzt vollständig live, ohne dass ein manuelles Neuladen der
  Seite nötig ist:
  - **Struktur live**: neue/entfernte/umbenannte Entitäten, Geräte, Bereiche
    und Automationen (inkl. geänderter Trigger/Aktionen) lösen serverseitig
    einen automatischen Neuaufbau des Graphen aus (debounced, ca. 2s nach der
    letzten Änderung), der an alle verbundenen Browser gepusht wird — zusätzlich
    ein Sicherheitsnetz-Neuaufbau alle 5 Minuten, falls ein Event doch mal
    durchrutscht
  - **Status-Anzeige live**: der im Detail-Panel angezeigte Status eines
    Knotens war bisher nur der Wert beim ersten Laden — jetzt wird er bei
    jeder Zustandsänderung aktualisiert, auch während das Panel bereits
    geöffnet ist
- Backend abonniert zusätzlich `entity_registry_updated`,
  `device_registry_updated`, `area_registry_updated` und
  `automation_reloaded`, um strukturelle Änderungen zu erkennen

## 1.8.0

- Neue Add-on-Konfigurationsoption `visible_domains`: kommagetrennte Liste von
  Entitäts-Domains, die im Graph geladen werden sollen (z. B.
  `light,switch,automation,media_player`) — hilft, überladene Graphen bei
  großen Installationen zu reduzieren. Default `all` (bisheriges Verhalten,
  alles sichtbar). Bereiche/Geräte/HA-Core bleiben immer sichtbar
- Action-Log bleibt jetzt auch im Kiosk-/Screensaver-Modus sichtbar (z. B. für
  ein Dash-Voice-Tablet als Aktivitäts-Übersicht)

## 1.7.0

- Etagen-Ebene entfernt: Bereiche hängen jetzt direkt am HA-Core
  (HA-Core → Bereich → Gerät → Entität) — wird von den meisten Nutzern
  ohnehin nicht verwendet
- Neues Action-Log unten rechts: zeigt die letzten 5 aktivierten Knoten
  (Entitäten, die aktiv wurden, sowie ausgelöste Automationen) mit Uhrzeit
- Datenfluss-Anzeige korrigiert: bei jeder Aktivierung wird jetzt der
  tatsächliche Verarbeitungsweg gezeigt — welche Automation die Entität
  gesteuert hat (woher) und welche Automation sie selbst auslöst inkl. deren
  gesteuerter Ziele (wohin) — statt wie zuvor nur der physischen
  Container-Hierarchie (Gerät/Bereich) zu folgen. Gilt einheitlich in allen
  Layout-Designs
- Hintergrund bleibt weiterhin tief schwarz (`#000000`)

## 1.6.0

- Auswählbares Layout-Design über die Add-on-Konfiguration (Tab „Konfiguration"):
  Frei (bisheriges Kräfte-Layout), Ebenen-Kaskade, Radial-Halo, Puls-Kaskade,
  Sonar-Halo — jeweils ein DAG-Layout, das die Hierarchie (HA-Core → Etage →
  Bereich → Gerät → Entität) lesbar hält, statt frei im Raum zu schweben
- Etagen und Bereiche sind in allen Designs jetzt direkt im Graph beschriftet
- Puls-Kaskade/Sonar-Halo zeigen keinen dauerhaften Hintergrund-Partikelstrom
  mehr — nur echte Live-Aktivierungen sind sichtbar
- Neu: wenn eine Entität aktiv wird, fließt der Datenstrom sichtbar Hop für Hop
  durch die echten Hierarchie-Kanten nach oben bis zum HA-Core (nicht mehr nur
  ein aufleuchtender Einzelknoten) — funktioniert in allen Designs
- Radial-Halo/Sonar-Halo: Kräfte-Tuning für Ringe angepasst, damit Knoten
  innerhalb ihres vorgesehenen Radius bleiben statt weit nach außen zu driften
- Für Kiosk/Screensaver zusätzlich per `&design=<kaskade|radial|puls-kaskade|sonar-halo|free>`
  in der URL überschreibbar
- Hintergrund bleibt weiterhin tief schwarz (`#000000`)

## 1.5.0

- Kiosk-Modus (`?kiosk`/`?screensaver`) verwendet jetzt einen festen Kamera-Abstand
  statt des zeitabhängigen `zoomToFit` — auf schwächerer Tablet-Hardware braucht die
  Kräfte-Simulation für große Graphen oft länger als jeder sinnvolle Timeout, wodurch
  die Kamera zu früh auf einen noch nicht ausgebreiteten Graphen einrastete
  ("zu nah dran" trotz v1.4.0-Fix)
- Abstand per `&zoom=<Zahl>` in der URL einstellbar (Default 2200), z. B.
  `http://<HA-IP>:8099/?kiosk&zoom=2800` für einen weiter herausgezoomten Blick
- Die interaktive Panel-Ansicht (ohne `?kiosk`) nutzt weiterhin den automatischen
  `zoomToFit` nach dem Einpendeln der Simulation

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
