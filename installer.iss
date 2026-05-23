; Inno Setup script for Lexia

#define MyAppName "Lexia"
#define MyAppVersion "1.2.1"
#define MyAppPublisher "Muhammad Jawad Bashir"
#define MyAppURL "https://github.com/stardust-96/lexia"
#define MyAppExeName "Lexia.exe"

[Setup]
AppId={{F5E7A1B2-3C4D-5E6F-8A9B-0C1D2E3F4567}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes
OutputDir=dist
OutputBaseFilename=Lexia-Setup-{#MyAppVersion}
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=admin
ArchitecturesInstallIn64BitMode=x64
UninstallDisplayIcon={app}\{#MyAppExeName}
SetupIconFile=lexia.ico
LicenseFile=LICENSE
WizardImageFile=installer_wizard.bmp
WizardSmallImageFile=installer_wizard_small.bmp

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "startupicon"; Description: "Start {#MyAppName} when Windows starts"; GroupDescription: "Additional options:"; Flags: unchecked

[Files]
Source: "dist\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "lexia.ico"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon
Name: "{userstartup}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: startupicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[UninstallRun]
Filename: "{cmd}"; Parameters: "/C taskkill /f /im {#MyAppExeName}"; Flags: runhidden; RunOnceId: "KillLexiaProcess"

[Code]
var
  RemoveUserDataOnUninstall: Boolean;

procedure InitializeUninstallProgressForm();
begin
  RemoveUserDataOnUninstall :=
    MsgBox(
      'Do you also want to remove local Lexia data and stored API keys?' + #13#10 + #13#10 +
      'This removes:' + #13#10 +
      '- %LOCALAPPDATA%\Lexia settings' + #13#10 +
      '- Stored OpenAI/Groq credentials from Windows Credential Manager',
      mbConfirmation,
      MB_YESNO
    ) = IDYES;
end;

procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep);
var
  ResultCode: Integer;
begin
  if (CurUninstallStep = usUninstall) and RemoveUserDataOnUninstall then
  begin
    if FileExists(ExpandConstant('{app}\{#MyAppExeName}')) then
      Exec(
        ExpandConstant('{app}\{#MyAppExeName}'),
        '--cleanup-secrets',
        '',
        SW_HIDE,
        ewWaitUntilTerminated,
        ResultCode
      );

    DelTree(ExpandConstant('{localappdata}\Lexia'), True, True, True);
  end;
end;
