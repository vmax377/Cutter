; Script d'Inno Setup per Cutter

#define MyAppName "Cutter"
#define MyAppVersion "3.1"
#define MyAppPublisher "Espai-Soft"
#define MyAppExeName "Cutter.exe"

[Setup]
AppId={{CUTTER-2026-TANQUI}}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
OutputDir=C:\CutterPython\instalador
OutputBaseFilename=CutterSetupV31
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=admin
ArchitecturesInstallIn64BitMode=x64

; ---- ICONES ----
SetupIconFile=C:\CutterPython\icona.ico
UninstallDisplayIcon={app}\Cutter.exe

[Languages]
Name: "catalan"; MessagesFile: "compiler:Languages\Catalan.isl"

[Tasks]
Name: "desktopicon"; Description: "Crear una drecera a l'escriptori"; GroupDescription: "Dreceres:"

[Files]
Source: "C:\CutterPython\dist\Cutter.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\CutterPython\icona.ico"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\icona.ico"; IconIndex: 0
Name: "{group}\Desinstal·lar {#MyAppName}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\icona.ico"; IconIndex: 0; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Executar {#MyAppName}"; Flags: nowait postinstall skipifsilent

[Code]
procedure CreateFolders();
begin
  if not DirExists('C:\CutterPython\dades') then
    ForceDirectories('C:\CutterPython\dades');
  if not DirExists('C:\MacrosTall') then
    ForceDirectories('C:\MacrosTall');
  if not DirExists('C:\MacrosTall\D2K') then
    ForceDirectories('C:\MacrosTall\D2K');
  if not DirExists('C:\MacrosTall\Ordres') then
    ForceDirectories('C:\MacrosTall\Ordres');
  if not DirExists('C:\MacrosTall\Etiquetes') then
    ForceDirectories('C:\MacrosTall\Etiquetes');
end;

procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then
  begin
    CreateFolders();
  end;
end;