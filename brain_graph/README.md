# Brain Graph

Live 3D-Visualisierung aller Home Assistant Entitäten, Geräte, Bereiche und Automationen — als eigenständiges Add-on mit Sidebar-Panel.

## Warum ein Add-on statt einer Integration?

Die 3D-Grafik läuft in einer eigenen, isolierten Seite (Ingress) statt in einem HA-Panel-Shadow-DOM. Das vermeidet Rendering-Probleme mit dem HA-Frontend und gibt dem WebGL-Kontext den vollen Bildschirm.

## Features

- Hierarchischer 3D-Graph: HA Core → Etagen → Bereiche → Geräte → Entitäten
- Automatische, sanfte Rotation
- Live-Glow bei aktiven Entitäten, goldener Puls am HA-Core-Knoten
- Partikel-Datenfluss-Animation: Automation-Trigger → Automation → Aktion
- Domain-Filter (Lichter, Schalter, Automationen, Sensoren, Media)
- Klick auf Knoten zeigt Details + Kamera-Fokus

## Installation

1. Settings → Add-ons → Add-on Store → ⋮ → Repositories
2. `https://github.com/pquandel2-alt/ha-brain-graph-addon` hinzufügen
3. „Brain Graph" installieren, starten
4. Sidebar-Eintrag „Brain Graph" erscheint

## Berechtigungen

Das Add-on benötigt `homeassistant_api` (Core-WebSocket via Supervisor-Token) für Live-Daten. Es schreibt nichts in die HA-Konfiguration.
