# Nexus Photo Studio – Entwicklung

## Stand: 0.5 Alpha / 20. Oktober 2026

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

## 0.3: Bedienung und Branding

Auf der Startseite erscheinen jetzt nur noch eigene Nexus-Verknüpfungen. Die PhotoCraft-Herkunft bleibt im Über-Dialog sowie in NOTICE und den Lizenzdateien angegeben.
Der Arbeitsbereich **Einfach** ergänzt die bestehenden Modi mit Navigator, Ebenen, Eigenschaften und Verlauf. Die Fenstertitelleiste zeigt nur noch den Nexus-Namen an.

## Nexus 0.4: Trickkiste und Quellenangaben

Der Hilfemenüpunkt zum PhotoCraft-Original wurde entfernt. Der Originalquellcode
ist weiterhin über „Über Nexus Photo Studio“ verlinkt, und NOTICE/ATTRIBUTION
sowie die Open-Source-Lizenzen bleiben enthalten.

Bei genügend Platz bietet die obere Leiste einen Zauberstab-Button zur
Trickkiste. Ohne geöffnetes Dokument ist er deaktiviert. Die Trickkiste
öffnet die bestehende funktionierende Filtergalerie mit echten Effektvorschauen,
sechs Kategorien, einstellbaren Parametern und kombinierbaren Effekten.

Ein vollständig eigenständiges PhotoImpact-Effektbibliotheks-Panel mit
speicherbaren Nutzer-Favoriten ist ein späterer Ausbau.

## 0.5: Upstream-Backports und Icon-Validierung

Gezielt übernommen: PhotoCraft PRs #7948 (gemergt, PSB-Signatur),
#6918 (offen, Tastenkombinationen) und #8137 (offen, lokalisierte Tooltipps).
Die zwei offenen PRs sind Backports unter Vorbehalt weiterer Tests.

Die 0.4 EXE wurde auf PE-Ressourcenebene geprüft und enthält bereits das
blau-violette Nexus-Symbol in sieben Größen. Deshalb sind alte Symbole auf dem
Windows-Desktop vermutlich durch Windows-Symbolcache, alte Verknüpfungen
oder einen veralteten Download verursacht. Das 0.5-Portable-Paket nutzt einen
**eigenen Versionsordner**. `tools/verify_nexus_exe_icon.py` vergleicht
im Windows-CI nun auch die tatsächliche EXE-Ressource mit dem neuen ICO.
Die Winresource-Kompilierung darf nicht mehr nur warnen und weiterlaufen.
