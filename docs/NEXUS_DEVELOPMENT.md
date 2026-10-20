# Nexus Photo Studio – Entwicklung

## Stand: 0.2 Alpha / 20. Oktober 2026

Der nächste Schritt baut auf der erfolgreich gestarteten portablen Windows-Alpha 0.1 auf. Die überarbeitete App erhält ein blau-violettes Objektiv-Icon, eine klarer benannte Startseite und die deutsche Trickkiste-Bezeichnung für die Filtergalerie.

Der erste Schritt ist ein **Branchen-Fork** der PhotoCraft-Quellen mit
eigenen Produkttexten, getrenntem Einstellungen-Ordner, eigener N-Marke,
Windows-Build und GitHub-Actions-Artefakt.

Das Produkt basiert weiterhin auf dem Rust/egui/wgpu-Editor PhotoCraft.
Der Quellcode wird nicht als Electron-Anwendung neu verpackt.

## Branding

- In der Benutzeroberfläche und im Windows-Fenster: **Nexus Photo Studio**.
- Rust-Workspace- und Crate-Namen bleiben zunächst `photocraft-*`, um
  den Image-Editor ohne riskante Massenumbenennung weiterzuentwickeln.
- Das generierte N-Symbol ersetzt bei jedem Nexus-Build die originalen
  PhotoCraft-Icons. Die binären upstream Icons und Artwork in alten Commits
  sind **keine** Nexus-Markenelemente.
- Die vorhandenen Copyright- und Lizenzdateien bleiben erhalten.
- Offen: vollständiger Asset- und Marken-Audit vor dem ersten Release.

## Build

```powershell
python tools/generate_nexus_icons.py .
cargo test -p photocraft --locked
cargo build --release --locked -p photocraft
Copy-Item target/release/photocraft.exe NexusPhotoStudio.exe
```

Die native Windows-Version wird als `NexusPhotoStudio.exe` paketiert.
`portable.txt` neben der EXE aktiviert das portable Profil; normale
Installationen verwenden getrennte Nutzerdaten.

Für den Installer kann Inno Setup 6 das Skript
`packaging/nexus/NexusPhotoStudio.iss` kompilieren. CI stellt ein
**nicht signiertes** Test-Artefakt bereit; für reguläre Downloads später
Signatur/SmartScreen-Reputation und ein sicheres Update-Verfahren vorsehen.

## Prüfung vor Freigabe

- Windows-11-Start, GPU-Fallback, Hoch-DPI, deutsche Sprache
- PSD-Dateien mit Pixel-, Text-, Effekt- und Gruppenebenen
- Pinsel, Auswahl, Textwerkzeug, Ebenenmasken, Rückgängig/Wiederholen
- Datei laden/speichern mit Dateivergleich und Absturz-Wiederherstellung
- Installer/Uninstaller, Nutzerrechte, getrennte PhotoCraft-Einstellungen
- Branding und alle eingebundenen Drittanbieter-Assets
- Keine automatische Update-Installation ohne prüfbare Integrität/Signatur

**Wichtig:** Die Bezeichnung Nexus Photo Studio muss vor öffentlicher
Veröffentlichung markenrechtlich geprüft werden. Das Repository ist
kein offizielles Projekt des PhotoCraft-/ArtCraft-Teams.
