[Setup]
AppName=Voxa Pro
AppVersion=1.0
AppPublisher=ceob68 / Vaultly
AppPublisherURL=https://github.com/ceob68
DefaultDirName={autopf}\VoxaPro
DefaultGroupName=Voxa Pro
OutputDir=Output
OutputBaseFilename=VoxaPro_Setup_v1.0
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Files]
Source: "dist\VoxaPro\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "docs\Manual.pdf"; DestDir: "{app}"; Flags: ignoreversion skipifsourcedoesntexist
Source: "docs\Guia_Rapida.pdf"; DestDir: "{app}"; Flags: ignoreversion skipifsourcedoesntexist
Source: "LICENSE.txt"; DestDir: "{app}"; Flags: ignoreversion
Source: "README.md"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Voxa Pro"; Filename: "{app}\VoxaPro.exe"
Name: "{commondesktop}\Voxa Pro"; Filename: "{app}\VoxaPro.exe"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Crear acceso directo en el escritorio"; GroupDescription: "Iconos adicionales:"

[Run]
Filename: "{app}\VoxaPro.exe"; Description: "Iniciar Voxa Pro"; Flags: nowait postinstall skipifsilent
