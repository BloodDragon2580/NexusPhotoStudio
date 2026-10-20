; Nexus Photo Studio ALPHA - Windows Inno Setup 6.
; Built only after the source has received the original Nexus icons.
#define AppName "Nexus Photo Studio"
#define AppVersion "0.1.0-alpha"
#define AppExe "NexusPhotoStudio.exe"

[Setup]
AppId={{6A646547-9417-4262-BD19-0F9012DD4D72}
AppName={#AppName}
AppVersion={#AppVersion}
AppVerName={#AppName} {#AppVersion}
AppPublisher=Nexus Photo Studio Community
DefaultDirName={localappdata}\Programs\Nexus Photo Studio
DefaultGroupName=Nexus Photo Studio
OutputDir=..\..\dist\nexus
OutputBaseFilename=NexusPhotoStudio-0.1-alpha-win64-setup
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=lowest
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
UninstallDisplayIcon={app}\{#AppExe}
SetupIconFile=..\..\assets\app-icon\photocraft.ico
LicenseFile=..\..\LICENSE-MIT
ChangesAssociations=no
DisableProgramGroupPage=yes

[Languages]
Name: "german"; MessagesFile: "compiler:Languages\German.isl"
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "Desktop-Verknüpfung erstellen"; Flags: unchecked

[Files]
Source: "..\..\target\release\photocraft.exe"; DestDir: "{app}"; DestName: "{#AppExe}"; Flags: ignoreversion
Source: "..\..\LICENSE-MIT"; DestDir: "{app}\Lizenzen"; Flags: ignoreversion
Source: "..\..\LICENSE-APACHE"; DestDir: "{app}\Lizenzen"; Flags: ignoreversion
Source: "..\..\NOTICE"; DestDir: "{app}\Lizenzen"; Flags: ignoreversion
Source: "..\..\ATTRIBUTION.md"; DestDir: "{app}\Lizenzen"; Flags: ignoreversion
Source: "..\..\assets\fonts\OFL-Inter.txt"; DestDir: "{app}\Lizenzen"; Flags: ignoreversion
Source: "..\..\assets\fonts\OFL-JetBrainsMono.txt"; DestDir: "{app}\Lizenzen"; Flags: ignoreversion
Source: "..\..\assets\icons\LICENSE-lucide.txt"; DestDir: "{app}\Lizenzen"; Flags: ignoreversion
Source: "..\..\assets\dict\LICENSE-SCOWL.txt"; DestDir: "{app}\Lizenzen"; Flags: ignoreversion
Source: "..\..\crates\algo\data\LICENSE-libfacedetection.txt"; DestDir: "{app}\Lizenzen"; Flags: ignoreversion

[Icons]
Name: "{autoprograms}\Nexus Photo Studio"; Filename: "{app}\{#AppExe}"
Name: "{autodesktop}\Nexus Photo Studio"; Filename: "{app}\{#AppExe}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#AppExe}"; Description: "Nexus Photo Studio starten"; Flags: postinstall nowait skipifsilent
