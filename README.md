# Nexus Photo Studio

**Nexus Photo Studio** ist ein freier Fotoeditor für Windows, der auf dem
Open-Source-Projekt [PhotoCraft](https://github.com/storytold/photocraft) basiert.
Ziel: eine einfach zu bedienende, moderne Bildbearbeitung mit Ebenen, Masken,
PSD-Dateien, Retusche und Effekten – inspiriert von PhotoImpact und Photoshop.

> **Status: 0.3 Alpha (Entwicklung).** Dieser Fork wird gerade umbenannt und
> getestet. Noch **keine** fertige oder geprüfte Community-Veröffentlichung.

## Erste Windows-Testversion bauen

Benötigt: Windows 11, [Git](https://git-scm.com/download/win),
[Rust](https://rustup.rs/) (MSVC Toolchain), Visual Studio Build Tools mit
**Desktop development with C++** und Python 3.

In PowerShell, im geklonten Repository:

```powershell
python tools/generate_nexus_icons.py .
cargo build --release --locked -p photocraft
Copy-Item target/release/photocraft.exe NexusPhotoStudio.exe
.\NexusPhotoStudio.exe
```

Wichtig: Der Icon-Generator ersetzt die ursprünglichen Programmsymbole im
lokalen Arbeitsverzeichnis durch ein eigenes geometrisches Nexus-N. Auf den
Windows-Builds und im späteren Installer soll **kein ArtCraft-Logo** erscheinen.
Die Windows-Buildpipeline erzeugt jetzt ein überarbeitetes blau-violettes Nexus-Symbol. Das Windows-Programm heißt vor dem Umkopieren technisch noch
`photocraft.exe`, weil der upstream Rust-Crate-Name bewusst unverändert
bleibt.

**Automatisierter Build:** Der Workflow
[`Nexus Windows Alpha`](.github/workflows/nexus-windows-alpha.yml) erzeugt
nach erfolgreichem Windows-Build eine portable ZIP und optional einen
Setup-Installer als **GitHub-Actions-Artefakt**. Das ist noch kein öffentliches
GitHub Release. Der Fork benötigt aktivierte GitHub Actions.

## Was ist schon enthalten?

Die zugrunde liegenden Werkzeuge kommen derzeit von PhotoCraft, nicht von
einer vollständig neu implementierten Nexus-Bildbearbeitung: Pinsel,
Auswahlwerkzeuge, Ebenen, Masken, Filter, Text, PSD-Import/Export und mehr.
Die genaue PSD-Fidelity und Stabilität müssen wir für Nexus mit echten
Dokumenten verifizieren. Einen garantierten Photoshop-1:1-Ersatz stellt
diese Alpha-Version **nicht** dar.

## Nächste Entwicklungsschritte

1. Eigene Marke, Dialoge, Icons und Installer unter Windows testen.
2. Verbliebene upstream Projektlinks, Logos und Produkttexte auditieren.
3. Deutsche und englische Oberfläche vollständig prüfen.
4. PSD-Roundtrip mit mehrschichtigen PSDs testen.
5. Einfachen Arbeitsbereich und PhotoImpact-inspirierte Trickkiste ergänzen.
6. Nach Tests und Lizenzprüfung erste Community-Beta veröffentlichen.

## Herkunft und Lizenz

Nexus Photo Studio ist eine **unabhängige, nicht offiziell unterstützte
Weiterentwicklung** von PhotoCraft und steht in keiner Verbindung zum
ArtCraft-Team. Der Quellcode von PhotoCraft ist wahlweise MIT / Apache-2.0
lizenziert. Die ursprünglichen Lizenz- und Copyright-Hinweise bleiben in
[`LICENSE-MIT`](LICENSE-MIT), [`LICENSE-APACHE`](LICENSE-APACHE),
[`NOTICE`](NOTICE) und [`ATTRIBUTION.md`](ATTRIBUTION.md) bestehen.

Die Logos, Wortmarken und Icons von ArtCraft/PhotoCraft sind **keine**
allgemein freigegebenen Open-Source-Markenzeichen. Eigene Builds müssen
darum Nexus-Branding verwenden. Details: [Nexus Entwicklung](docs/NEXUS_DEVELOPMENT.md).

Bevor die Software öffentlich angeboten wird, sind eine Markenrecherche
und die Prüfung aller verwendeten Assets notwendig.
