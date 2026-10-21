# Nexus Photo Studio – Änderungen

## 0.5 Alpha – Icon und upstream Bugfixes

- Das nachweislich eingebettete Nexus-Icon wird im Build jetzt mit allen sieben Größen geprüft.
- Native Windows-Ressourcen sind Pflicht, statt Fehler still zu ignorieren.
- Die portable ZIP entpackt in einen versionierten Ordner (Schutz vor altem Windows-Icon-Cache).
- PhotoCraft PR #7948: PSB/Photoshop-Signaturen für lange Metadatenblöcke korrigiert.
- PhotoCraft PR #6918: PageUp/Down und Pfeiltasten bei Tastaturbelegungen repariert (noch nicht upstream gemergt).
- PhotoCraft PR #8137: Tooltip im Textwerkzeug übersetzbar gemacht (noch nicht upstream gemergt).


## 0.4 Alpha – Trickkiste und Hilfe

- Originalprojekt-Link aus dem Hilfe-Menü entfernt; Herkunft und Source-Link im Über-Dialog erhalten.
- Zauberstab-Schnellzugriff auf die bereits funktionierende Trickkiste in der oberen Leiste (bei offenem Dokument).
- Die Filtergalerie bietet echte Effektvorschauen, Kategorien, Parameter und Kombination mehrerer Effekte.
- Deutsche Titel und Startseitenhinweise vereinfacht.
- Keine neuen KI-Effekte oder eigenen PhotoImpact-Vorlagen behauptet.


## 0.3 Alpha (Testversion)

- Den Link „Originalprojekt“ vom Startbildschirm entfernt; Herkunftsnachweise weiterhin im Über-Dialog und in den Lizenzdateien.
- Fenstertitel heißt auch ohne geöffnetes Bild „Nexus Photo Studio“.
- Neuer Arbeitsbereich **Einfach** mit Navigator, Ebenen, Eigenschaften und Verlauf.
- Startseitenlinks führen zum Nexus-Projekt und zur Fehlermeldungsseite.
- Die bestehende PhotoCraft-Bildbearbeitungsengine samt PSD-Funktionen bleibt unangetastet.


## 0.2 Alpha (Windows-Testversion, noch nicht öffentlich freigegeben)

- Eigenständiges, hochwertigeres blau-violettes Nexus-Icon mit stilisierter Kamerablende und Metall-N.
- Neue Nexus-Startseite mit klarem Namen und Motto statt der alten PhotoCraft-Anzeige.
- Erläuternde Schnellstart-Hinweise für das Erstellen von Designs und das Öffnen von PSD-Dateien.
- **Trickkiste** als verständlicher deutscher Name für die bereits vorhandene Filtergalerie.
- Deutschsprachiger Hinweis auf fertige Effekte direkt auf der Startseite.
- Bestehende PhotoCraft-Bildbearbeitungsengine und PSD-Kompatibilität unverändert erhalten.
- Windows-Installer, portable ZIP und GitHub-Build auf 0.2 Alpha vorbereitet.
- Build-Automatik so eingeschränkt, dass nur ein ausdrücklich angeforderter Windows-Build startet.

**Wichtig:** Ein professionelles Retuschepaket oder zusätzliche Photoshop-Spezialfunktionen wurden mit dieser Alpha nicht neu implementiert.
Die vorhandenen Bildbearbeitungswerkzeuge werden in späteren Etappen anhand echter Praxisfälle verbessert.

## 0.1 Alpha

- Erster Nexus-Fork des nativen PhotoCraft-Bildeditors mit getrennten Einstellungen.
- Eigenes Windows-Paket, Build-Workflow und erste grundlegende Übersetzungen.
