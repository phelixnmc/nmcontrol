; also in the code
#define version "0.8"

#define sourceFolder "dist\nmcontrolwin"
#define progname "Namecontrol"
#define exefile "nmcontrolwin.exe"

[Messages]
WelcomeLabel2=%nThis will install [name/ver] on your computer and modify your registry to catch DNS requests for .bit domain.%n
ClickFinish=Click Finish to exit Setup.
ConfirmUninstall=Are you sure you want to remove %1 and undo any registry changes?%n%nThis will leave config files alone.
UninstalledAll=%1 was successfully removed from your computer.%n%nThere might still be configuration data in %APPDATA%\Nmcontrol

[Setup]
AppVerName={#progname} {#version}
AppName={#progname}
DefaultDirName={pf}\{#progname}
DefaultGroupName={#progname}
UninstallDisplayIcon={uninstallexe}
Compression=lzma2/ultra
SolidCompression=yes
OutputDir=.\installer
OutputBaseFilename={#progname}_v{#version}_setup

[Files]
Source: "{#sourceFolder}\{#exefile}"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#sourceFolder}\*.*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs

[Tasks]
Name: desktopicon; Description: "Create a &desktop icon"; GroupDescription: "Additional icons:"
Name: desktopicon\common; Description: "For all users"; GroupDescription: "Additional icons:"; Flags: exclusive
Name: desktopicon\user; Description: "For the current user only"; GroupDescription: "Additional icons:"; Flags: exclusive unchecked
Name: quicklaunchicon; Description: "Create a &Quick Launch icon"; GroupDescription: "Additional icons:"; Flags: unchecked

[Icons]
Name: "{group}\{#progname}"; Filename: "{app}\{#exefile}"
Name: "{commondesktop}\Namecontrol"; Filename: "{app}\{#exefile}"; Tasks: desktopicon\common
Name: "{userdesktop}\Namecontrol"; Filename: "{app}\{#exefile}"; Tasks: desktopicon\user
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\Namecontrol"; Filename: "{app}\{#exefile}"; Tasks: quicklaunchicon
Name: "{group}\uninstall"; Filename: "{uninstallexe}";

[Run]
Filename: "{app}\{#exefile}"; Description: "Launch application"; Flags: postinstall skipifsilent nowait

[Registry]
Root: HKLM; Subkey: "System\CurrentControlSet\services\Dnscache\Parameters\DnsPolicyConfig\NMControl"; Flags: uninsdeletekey
Root: HKLM; Subkey: "System\CurrentControlSet\services\Dnscache\Parameters\DnsPolicyConfig\NMControl"; ValueType: dword; ValueName: "ConfigOptions"; ValueData: "8"; Flags: uninsdeletekey
Root: HKLM; Subkey: "System\CurrentControlSet\services\Dnscache\Parameters\DnsPolicyConfig\NMControl"; ValueType: multisz; ValueName: "Name"; ValueData: ".bit"; Flags: uninsdeletekey
Root: HKLM; Subkey: "System\CurrentControlSet\services\Dnscache\Parameters\DnsPolicyConfig\NMControl"; ValueType: string; ValueName: "IPSECCARestriction"; ValueData: ""; Flags: uninsdeletekey
Root: HKLM; Subkey: "System\CurrentControlSet\services\Dnscache\Parameters\DnsPolicyConfig\NMControl"; ValueType: string; ValueName: "GenericDNSServers"; ValueData: "127.0.0.1"; Flags: uninsdeletekey
Root: HKLM; Subkey: "System\CurrentControlSet\services\Dnscache\Parameters\DnsPolicyConfig\NMControl"; ValueType: dword; ValueName: "Version"; ValueData: "2"; Flags: uninsdeletekey
