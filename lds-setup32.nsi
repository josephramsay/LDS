# Auto-generated by EclipseNSIS Script Wizard
# 19/03/2013 1:16:51 PM

Name "LDS Replicate"

#lds-replicate-setup-win32-0.0.7.exe

# General Symbol Definitions
!define APPNAME $(^Name)
!define REGKEY "SOFTWARE\${APPNAME}"
!define VERSION 0.0.7
!define PLATFORM "win32"
!define COMPANY "Land Information New Zealand"
!define URL https://www.linz.govt.nz/

# Included files
!include Sections.nsh
!include nsDialogs.nsh
!include InstallOptions.nsh
!include EnvVarUpdate.nsh

# Reserved Files
ReserveFile "${NSISDIR}\Plugins\StartMenu.dll"

# Variables
Var StartMenuGroup

# Installer pages
Page license
Page components
Page directory
Page custom StartMenuGroupSelect "" ": Start Menu Folder"
Page instfiles
Page custom EnvReqCreate EnvReqLeave
Page custom ConfigWizzCreate ConfigWizzLeave

# Installer attributes
OutFile C:\data\lds-replicate-setup-${PLATFORM}-r${VERSION}.exe
InstallDir "$PROGRAMFILES\LDS Replicate"
CRCCheck on
XPStyle on
Icon F:\git\LDS\LDSReplicate\doc\LINZsmall.ico
ShowInstDetails show
AutoCloseWindow false
LicenseData "F:\git\LDS\license\LDS\linz-license.txt"
VIProductVersion 0.0.5.0
VIAddVersionKey ProductName "LDS Replicate"
VIAddVersionKey ProductVersion "${VERSION}"
VIAddVersionKey CompanyName "${COMPANY}"
VIAddVersionKey CompanyWebsite "${URL}"
VIAddVersionKey FileVersion "${VERSION}"
VIAddVersionKey FileDescription ""
VIAddVersionKey LegalCopyright ""
InstallDirRegKey HKLM "${REGKEY}" Path
UninstallIcon "${NSISDIR}\Contrib\Graphics\Icons\win-uninstall.ico"
ShowUninstDetails show

# Installer sections
!macro CREATE_SMGROUP_SHORTCUT NAME PATH
    Push "${NAME}"
    Push "${PATH}"
    Call CreateSMGroupShortcut
!macroend

Section -Main SEC0000
    SetOutPath $INSTDIR
    SetOverwrite on
    File F:\git\LDS\LDSReplicate\ldsreplicate.cmd
    File F:\git\LDS\LDSReplicate\ldsreplicate_gui.cmd
    File F:\git\LDS\LDSReplicate\setup_vars.cmd
    WriteRegStr HKLM "${REGKEY}\Components" Main 1
SectionEnd

Section "LDS Replicate" SEC0001
    SetOverwrite on
    SetOutPath $INSTDIR\apps\ldsreplicate
    File F:\git\LDS\LDSReplicate\ldsreplicate.py
    File F:\git\LDS\LDSReplicate\ldsreplicate_gui.py
    SetOutPath $INSTDIR\apps\ldsreplicate\conf
    AccessControl::GrantOnFile "$INSTDIR\apps\ldsreplicate\conf" "(S-1-5-32-545)" "FullAccess"
    File F:\git\LDS\LDSReplicate\conf\getcapabilities.file.xsl
    File F:\git\LDS\LDSReplicate\conf\getcapabilities.json.xsl
    File /a /oname=gui.prefs F:\git\LDS\LDSReplicate\conf\empty.gui.prefs
    File F:\git\LDS\LDSReplicate\conf\ldsincr.conf
    File F:\git\LDS\LDSReplicate\conf\ldspk.csv
    File F:\git\LDS\LDSReplicate\conf\sufiselector.xsl
    SetOutPath $INSTDIR\apps\ldsreplicate\doc
    File F:\git\LDS\LDSReplicate\doc\demo2_commands.txt
    File F:\git\LDS\LDSReplicate\doc\LDSReplicate_instructions.pdf
    File F:\git\LDS\LDSReplicate\doc\README
    SetOutPath $INSTDIR\apps\ldsreplicate\img
    File F:\git\LDS\LDSReplicate\img\linz_static.png
    File F:\git\LDS\LDSReplicate\img\busy_static.png
    File F:\git\LDS\LDSReplicate\img\clean_static.png
    File F:\git\LDS\LDSReplicate\img\error_static.png
    File F:\git\LDS\LDSReplicate\img\linz.gif
    File F:\git\LDS\LDSReplicate\img\busy.gif
    File F:\git\LDS\LDSReplicate\img\clean.gif
    File F:\git\LDS\LDSReplicate\img\error.gif
    SetOutPath $INSTDIR\apps\ldsreplicate\lds
    File F:\git\LDS\LDSReplicate\lds\__init__.py
    File F:\git\LDS\LDSReplicate\lds\ConfigWrapper.py
    File F:\git\LDS\LDSReplicate\lds\DataStore.py
    File F:\git\LDS\LDSReplicate\lds\ESRIDataStore.py
    File F:\git\LDS\LDSReplicate\lds\FileGDBDataStore.py
    File F:\git\LDS\LDSReplicate\lds\LDSDataStore.py
    File F:\git\LDS\LDSReplicate\lds\LDSUtilities.py
    File F:\git\LDS\LDSReplicate\lds\MSSQLSpatialDataStore.py
    File F:\git\LDS\LDSReplicate\lds\PostgreSQLDataStore.py
    File F:\git\LDS\LDSReplicate\lds\ProjectionReference.py
    File F:\git\LDS\LDSReplicate\lds\ReadConfig.py
    File F:\git\LDS\LDSReplicate\lds\SpatiaLiteDataStore.py
    File F:\git\LDS\LDSReplicate\lds\TransferProcessor.py
    File F:\git\LDS\LDSReplicate\lds\VersionUtilities.py
    File F:\git\LDS\LDSReplicate\lds\WFSDataStore.py
    SetOutPath $INSTDIR\apps\ldsreplicate\lds\gui
    File F:\git\LDS\LDSReplicate\lds\gui\__init__.py
    File F:\git\LDS\LDSReplicate\lds\gui\LayerConfigSelector.py
    File F:\git\LDS\LDSReplicate\lds\gui\LDSGUI.py
    File F:\git\LDS\LDSReplicate\lds\gui\MainConfigWizard.py
    File F:\git\LDS\LDSReplicate\lds\gui\ConfigConnector.py
    SetOutPath $INSTDIR\apps\ldsreplicate\lds\test
    File F:\git\LDS\LDSReplicate\lds\test\__init__.py
    File F:\git\LDS\LDSReplicate\lds\test\SuiteRunAllTests.py
    File F:\git\LDS\LDSReplicate\lds\test\TestDemo1.py
    File F:\git\LDS\LDSReplicate\lds\test\TestDemo2.py
    File F:\git\LDS\LDSReplicate\lds\test\TestSize.py
    File F:\git\LDS\LDSReplicate\lds\test\TestUI.py
    File F:\git\LDS\LDSReplicate\lds\test\TestURL.py
    SetOutPath $INSTDIR\apps\ldsreplicate\log
    AccessControl::GrantOnFile "$INSTDIR\apps\ldsreplicate\log" "(S-1-5-32-545)" "FullAccess"
    ;Makes sure we aren't leaking test logs in installer. Instead use touched empty file with RW attributes
    File /a /oname=debug.log F:\git\LDS\LDSReplicate\log\empty.debug.log
    SetOutPath $INSTDIR
    WriteRegStr HKLM "${REGKEY}\Components" "LDS Replicate" 1
SectionEnd

Section "Python 2.7" SEC0002
    SetOutPath $INSTDIR\apps\python27
    SetOverwrite on
    File /r /x *.pyc /x *.pyo /x *.tmp F:\temp\ldsreplicate_builddir\32\apps\python27\*
    WriteRegStr HKLM "${REGKEY}\Components" "Python 2.7" 1
SectionEnd

Section GDAL SEC0003
    SetOutPath $INSTDIR\bin\gdal
    SetOverwrite on
    File /r F:\temp\ldsreplicate_builddir\32\bin\gdal\*
    WriteRegStr HKLM "${REGKEY}\Components" GDAL 1
SectionEnd

Section -License SEC0004
    SetOutPath $INSTDIR\license
    SetOverwrite on
    File /r F:\git\LDS\license\*
    WriteRegStr HKLM "${REGKEY}\Components" License 1
SectionEnd

Section -post SEC0005
    WriteRegStr HKLM "${REGKEY}" Path $INSTDIR
    WriteRegStr HKLM "${REGKEY}" StartMenuGroup $StartMenuGroup
    SetOutPath $INSTDIR
    createShortcut "$SMPROGRAMS\${APPNAME}\${APPNAME}.lnk" "$INSTDIR\ldsreplicate_gui.cmd" "" "F:\git\LDS\LDSReplicate\doc\LINZsmall.ico"
    WriteUninstaller $INSTDIR\uninstall.exe
    !insertmacro CREATE_SMGROUP_SHORTCUT "Uninstall ${APPNAME}" $INSTDIR\uninstall.exe
    WriteRegStr HKLM "SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" DisplayName "${APPNAME}"
    WriteRegStr HKLM "SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" DisplayVersion "${VERSION}"
    WriteRegStr HKLM "SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" Publisher "${COMPANY}"
    WriteRegStr HKLM "SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" URLInfoAbout "${URL}"
    WriteRegStr HKLM "SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" DisplayIcon $INSTDIR\uninstall.exe
    WriteRegStr HKLM "SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" UninstallString $INSTDIR\uninstall.exe
    WriteRegDWORD HKLM "SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" NoModify 1
    WriteRegDWORD HKLM "SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" NoRepair 1
SectionEnd

# Macro for selecting uninstaller sections
!macro SELECT_UNSECTION SECTION_NAME UNSECTION_ID
    Push $R0
    ReadRegStr $R0 HKLM "${REGKEY}\Components" "${SECTION_NAME}"
    StrCmp $R0 1 0 next${UNSECTION_ID}
    !insertmacro SelectSection "${UNSECTION_ID}"
    GoTo done${UNSECTION_ID}
next${UNSECTION_ID}:
    !insertmacro UnselectSection "${UNSECTION_ID}"
done${UNSECTION_ID}:
    Pop $R0
!macroend

# Uninstaller sections
!macro DELETE_SMGROUP_SHORTCUT NAME
    Push "${NAME}"
    Call un.DeleteSMGroupShortcut
!macroend

Section /o -un.License UNSEC0003
    RmDir /r /REBOOTOK $INSTDIR\license
    DeleteRegValue HKLM "${REGKEY}\Components" License
SectionEnd

Section /o -un.GDAL UNSEC0002
    RmDir /r /REBOOTOK $INSTDIR\bin\gdal
    DeleteRegValue HKLM "${REGKEY}\Components" GDAL
SectionEnd

Section /o "-un.Python 2.7" UNSEC0001
    RmDir /r /REBOOTOK $INSTDIR\apps\python27
    DeleteRegValue HKLM "${REGKEY}\Components" "Python 2.7"
SectionEnd

Section /o "-un.LDS Replicate" UNSEC0000
    Delete /REBOOTOK $INSTDIR\setup_vars.bat
    Delete /REBOOTOK $INSTDIR\ldsreplicate_gui.bat
    Delete /REBOOTOK $INSTDIR\ldsreplicate.bat
    RmDir /r /REBOOTOK $INSTDIR\apps\ldsreplicate
    DeleteRegValue HKLM "${REGKEY}\Components" "LDS Replicate"
SectionEnd

Section -un.post UNSEC0004
    Call un.EnvReqUninstall
    DeleteRegKey HKLM "SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}"
    !insertmacro DELETE_SMGROUP_SHORTCUT "Uninstall ${APPNAME}"
    delete "$SMPROGRAMS\${APPNAME}\${APPNAME}.lnk"
    Delete /REBOOTOK $INSTDIR\uninstall.exe
    DeleteRegValue HKLM "${REGKEY}" StartMenuGroup
    DeleteRegValue HKLM "${REGKEY}" Path
    DeleteRegKey /IfEmpty HKLM "${REGKEY}\Components"
    DeleteRegKey /IfEmpty HKLM "${REGKEY}"
    RmDir /REBOOTOK $SMPROGRAMS\$StartMenuGroup
    RmDir /REBOOTOK $INSTDIR\apps
    RmDir /REBOOTOK $INSTDIR\bin
    RmDir /REBOOTOK $INSTDIR
    Push $R0
    StrCpy $R0 $StartMenuGroup 1
    StrCmp $R0 ">" no_smgroup
no_smgroup:
    Pop $R0
    
SectionEnd

# Installer functions
Function StartMenuGroupSelect
    Push $R1
    StartMenu::Select /checknoshortcuts "Do not create shortcuts" /autoadd /text "Select the Start Menu folder in which to create the program's shortcuts:" /lastused $StartMenuGroup "LDS Replicate"
    Pop $R1
    StrCmp $R1 success success
    StrCmp $R1 cancel done
    MessageBox MB_OK $R1
    Goto done
success:
    Pop $StartMenuGroup
done:
    Pop $R1
FunctionEnd

Function .onInit
    InitPluginsDir
FunctionEnd

#Custom user page functions
Function EnvReqCreate
    Var /Global Dialog1
    Var /Global Label1
    Var /Global Label2
    Var /Global CheckBox1
    Var /Global CheckBox1_State
    Var /Global CheckBox2
    Var /Global CheckBox2_State
    Var /Global CheckBox3
    Var /Global CheckBox3_State
    
    nsDialogs::Create /NOUNLOAD 1018
    Pop $Dialog1
    ${If} $Dialog1 == error
        Abort
    ${EndIf}
    
    ${NSD_CreateLabel} 0 0 100% 12u "Permanently Install LDSReplicate Environment Variables?"
    Pop $Label1
    ${NSD_CreateLabel} 0 20 100% 24u "(NOT required if using the supplied batch (.cmd) startup scripts$\n or when components and their paths are already installed)"
    Pop $Label2
    
    ${NSD_CreateCheckbox} 0 50u 100% 10u "&System PATH"
    Pop $CheckBox1
    ${If} $CheckBox1_State == ${BST_CHECKED}
        ${NSD_UnCheck} $CheckBox1
    ${EndIf}
    
    ${NSD_CreateCheckbox} 0 65u 100% 10u "&PYTHONPATH"
    Pop $CheckBox2
    ${If} $CheckBox2_State == ${BST_CHECKED}
        ${NSD_UnCheck} $CheckBox2
    ${EndIf}
    
    ${NSD_CreateCheckbox} 0 80u 100% 10u "&GDAL_DRIVER and GDAL_PLUGINS"
    Pop $CheckBox3
    ${If} $CheckBox3_State == ${BST_CHECKED}
        ${NSD_UnCheck} $CheckBox3
    ${EndIf}

    nsDialogs::Show
FunctionEnd

Function EnvReqLeave
	Var /GLOBAL evChanged
	StrCpy $evChanged "FALSE"
	
    ;system path
    ${NSD_GetState} $CheckBox1 $CheckBox1_State
    ${If} $CheckBox1_State == ${BST_CHECKED}
    	StrCpy $evChanged "TRUE"
        ${EnvVarUpdate} $0 "PATH" "P" "HKLM" "$INSTDIR"
        ${EnvVarUpdate} $0 "PATH" "P" "HKLM" "$INSTDIR\bin\gdal"
        ${EnvVarUpdate} $0 "PATH" "A" "HKLM" "$INSTDIR\apps\python27"
        ${EnvVarUpdate} $0 "PATH" "A" "HKLM" "$INSTDIR\apps\ldsreplicate"
        ${EnvVarUpdate} $0 "PATH" "A" "HKLM" "$INSTDIR\gdal\bin"
        ${EnvVarUpdate} $0 "PATH" "A" "HKLM" "$INSTDIR\gdal\gdalplugins"
        ${EnvVarUpdate} $0 "PATH" "A" "HKLM" "$INSTDIR\gdal\gdal-data"  
    ${EndIf}
    
    ;pythonpath
    ${NSD_GetState} $CheckBox2 $CheckBox2_State
    ${If} $CheckBox2_State == ${BST_CHECKED}
       StrCpy $evChanged "TRUE"
       ${EnvVarUpdate} $0 "PYTHONHOME" "A" "HKLM" "$INSTDIR\python27"
       ${EnvVarUpdate} $0 "PYTHONPATH" "A" "HKLM" "$INSTDIR\python27"
       ${EnvVarUpdate} $0 "PYTHONPATH" "A" "HKLM" "$INSTDIR\apps\python27\DLLs"
       ${EnvVarUpdate} $0 "PYTHONPATH" "A" "HKLM" "$INSTDIR\apps\python27\lib"
       ${EnvVarUpdate} $0 "PYTHONPATH" "A" "HKLM" "$INSTDIR\apps\python27\lib\lib-tk"
       ${EnvVarUpdate} $0 "PYTHONPATH" "A" "HKLM" "$INSTDIR\apps\python27\lib\site-packages"
       ${EnvVarUpdate} $0 "PYTHONPATH" "A" "HKLM" "$INSTDIR\apps\python27\lib\site-packages\osgeo" 
    ${EndIf}
   
    ;gdal
    ${NSD_GetState} $CheckBox3 $CheckBox3_State
    ${If} $CheckBox3_State == ${BST_CHECKED}
       StrCpy $evChanged "TRUE"
       ${EnvVarUpdate} $0 "GDAL_DATA" "A" "HKLM" "$INSTDIR\bin\gdal\gdal-data"
       ${EnvVarUpdate} $0 "GDAL_DRIVER_PATH" "A" "HKLM" "$INSTDIR\bin\gdal\gdalplugins"
       ${EnvVarUpdate} $0 "PROJ_LIB" "A" "HKLM" "$INSTDIR\bin\gdal\projlib"
    ${EndIf}
    
    ${If} $evChanged == "TRUE"
    	SendMessage ${HWND_BROADCAST} ${WM_WININICHANGE} 0 "STR:Environment" /TIMEOUT=5000
    ${EndIf}

FunctionEnd

Function ConfigWizzCreate
    Var /Global Dialog2
    Var /Global CheckBox4
    Var /Global CheckBox5 
    Var /Global CheckBox6
    Var /Global CheckBox4_State
    Var /Global CheckBox5_State 
    Var /Global CheckBox6_State
    
    nsDialogs::Create /NOUNLOAD 1018
    Pop $Dialog2
    ${If} $Dialog2 == error
        Abort
    ${EndIf}
    
    
    ${NSD_CreateLabel} 0 0 100% 12u "Start the Configuration Wizard to initial user and connection preferences,"
    ${NSD_CreateLabel} 0 15 100% 12u "start the Layer Config Setup to initialise your layer selections and Run"
    ${NSD_CreateLabel} 0 30 100% 12u "Application to begin replicating LDS"
    ${NSD_CreateLabel} 0 45 100% 24u "(You will also be prompted to complete the config and layer setup on first run)"
    
    ${NSD_CreateCheckBox} 0 60u 100% 10u "Start &Config Wizard"
    Pop $CheckBox4
    ${NSD_SetState} $CheckBox4_State ${BST_CHECKED}
    ${NSD_Check} $CheckBox4
    
    ${NSD_CreateCheckBox} 0 75u 100% 10u "Start &Layer Setup"
    Pop $CheckBox5
    ${NSD_SetState} $CheckBox5_State ${BST_CHECKED}
    ${NSD_Check} $CheckBox5
    
    ${NSD_CreateCheckBox} 0 90u 100% 10u "&Run Application"
    Pop $CheckBox6
    ${NSD_SetState} $CheckBox6_State ${BST_CHECKED}
    ${NSD_Check} $CheckBox6
    

    nsDialogs::Show
FunctionEnd

Function ConfigWizzLeave
    
    ${NSD_GetState} $CheckBox4 $CheckBox4_State
    ${If} $CheckBox4_State == ${BST_CHECKED}
        ExecWait '"$INSTDIR\ldsreplicate_gui.cmd" W'
    ${EndIf}
    
    ${NSD_GetState} $CheckBox5 $CheckBox5_State
    ${If} $CheckBox5_State == ${BST_CHECKED}
        ExecWait '"$INSTDIR\ldsreplicate_gui.cmd" L'
    ${EndIf}
    
    ${NSD_GetState} $CheckBox6 $CheckBox6_State
    ${If} $CheckBox6_State == ${BST_CHECKED}
        Exec '"$INSTDIR\ldsreplicate_gui.cmd"'
    ${EndIf}

FunctionEnd

Function un.EnvReqUninstall

    ${NSD_GetState} $CheckBox1 $CheckBox1_State
    ${If} $CheckBox1_State == ${BST_CHECKED}
        ${un.EnvVarUpdate} $0 "PATH" "R" "HKLM" "$INSTDIR"
        ${un.EnvVarUpdate} $0 "PATH" "R" "HKLM" "$INSTDIR\bin\gdal"
        ${un.EnvVarUpdate} $0 "PATH" "R" "HKLM" "$INSTDIR\apps\python27"
        ${un.EnvVarUpdate} $0 "PATH" "R" "HKLM" "$INSTDIR\apps\ldsreplicate"
        ${un.EnvVarUpdate} $0 "PATH" "R" "HKLM" "$INSTDIR\gdal\bin"
        ${un.EnvVarUpdate} $0 "PATH" "R" "HKLM" "$INSTDIR\gdal\gdalplugins"
        ${un.EnvVarUpdate} $0 "PATH" "R" "HKLM" "$INSTDIR\gdal\gdal-data"  
    ${EndIf}


    ${NSD_GetState} $CheckBox2 $CheckBox2_State
    ${If} $CheckBox2_State == ${BST_CHECKED}
        ${un.EnvVarUpdate} $0 "PYTHONHOME" "R" "HKLM" "$INSTDIR\python27"
        ${un.EnvVarUpdate} $0 "PYTHONPATH" "R" "HKLM" "$INSTDIR\python27"
        ${un.EnvVarUpdate} $0 "PYTHONPATH" "R" "HKLM" "$INSTDIR\apps\python27\DLLs"
        ${un.EnvVarUpdate} $0 "PYTHONPATH" "R" "HKLM" "$INSTDIR\apps\python27\lib"
        ${un.EnvVarUpdate} $0 "PYTHONPATH" "R" "HKLM" "$INSTDIR\apps\python27\lib\lib-tk"
        ${un.EnvVarUpdate} $0 "PYTHONPATH" "R" "HKLM" "$INSTDIR\apps\python27\lib\site-packages"
        ${un.EnvVarUpdate} $0 "PYTHONPATH" "R" "HKLM" "$INSTDIR\apps\python27\lib\site-packages\osgeo" 
    ${EndIf}

    ${NSD_GetState} $CheckBox3 $CheckBox3_State
    ${If} $CheckBox3_State == ${BST_CHECKED}
        ${un.EnvVarUpdate} $0 "GDAL_DATA" "R" "HKLM" "$INSTDIR\bin\gdal\gdal-data"
        ${un.EnvVarUpdate} $0 "GDAL_DRIVER_PATH" "R" "HKLM" "$INSTDIR\bin\gdal\gdalplugins"
        ${un.EnvVarUpdate} $0 "PROJ_LIB" "R" "HKLM" "$INSTDIR\bin\gdal\projlib"
    ${EndIf}
    
    SendMessage ${HWND_BROADCAST} ${WM_WININICHANGE} 0 "STR:Environment" /TIMEOUT=5000

FunctionEnd

Function CreateSMGroupShortcut
    Exch $R0 ;PATH
    Exch
    Exch $R1 ;NAME
    Push $R2
    StrCpy $R2 $StartMenuGroup 1
    StrCmp $R2 ">" no_smgroup
    SetOutPath $SMPROGRAMS\$StartMenuGroup
    CreateShortcut "$SMPROGRAMS\$StartMenuGroup\$R1.lnk" $R0
no_smgroup:
    Pop $R2
    Pop $R1
    Pop $R0
FunctionEnd

# Uninstaller functions
Function un.onInit
    ReadRegStr $INSTDIR HKLM "${REGKEY}" Path
    ReadRegStr $StartMenuGroup HKLM "${REGKEY}" StartMenuGroup
    
    !insertmacro SELECT_UNSECTION "LDS Replicate" ${UNSEC0000}
    !insertmacro SELECT_UNSECTION "Python 2.7" ${UNSEC0001}
    !insertmacro SELECT_UNSECTION GDAL ${UNSEC0002}
    !insertmacro SELECT_UNSECTION License ${UNSEC0003}
FunctionEnd

Function un.DeleteSMGroupShortcut
    Exch $R1 ;NAME
    Push $R2
    StrCpy $R2 $StartMenuGroup 1
    StrCmp $R2 ">" no_smgroup
    Delete /REBOOTOK "$SMPROGRAMS\$StartMenuGroup\$R1.lnk"
no_smgroup:
    Pop $R2
    Pop $R1
FunctionEnd

