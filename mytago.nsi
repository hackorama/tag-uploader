; basic script template for NSIS installers
;
; Written by Philip Chu
; Copyright (c) 2004-2005 Technicat, LLC
;
; This software is provided 'as-is', without any express or implied warranty.
; In no event will the authors be held liable for any damages arising from the use of this software.
 
; Permission is granted to anyone to use this software for any purpose,
; including commercial applications, and to alter it ; and redistribute
; it freely, subject to the following restrictions:
 
;    1. The origin of this software must not be misrepresented; you must not claim that
;       you wrote the original software. If you use this software in a product, an
;       acknowledgment in the product documentation would be appreciated but is not required.
 
;    2. Altered source versions must be plainly marked as such, and must not be
;       misrepresented as being the original software.
 
;    3. This notice may not be removed or altered from any source distribution.
 
!define setup "Mytago1.02.43Setup.exe"
 
; change this to wherever the files to be packaged reside
!define srcdir "."
 
!define company "Mytago"
 
!define prodname "Mytago Uploader"
!define unprodname "Uninstall Mytago Uploader"
!define exec "Mytago.exe"
 
; !define website "http://www.mytago.com"

; optional stuff
 
; text file to open in notepad after installation
; !define notefile "README.txt"
 
; license text file
!define licensefile license.txt
 
; icons must be Microsoft .ICO files
!define icon "mytago.ico"

!define unicon "uninstall.ico"
 
; installer background screen
; !define screenimage installer.bmp
 
; file containing list of file-installation commands
!define files "files.nsi"
 
; file containing list of file-uninstall commands
!define unfiles "unfiles.nsi"
 
; registry stuff
 
!define regkey "Software\${company}\${prodname}"
!define uninstkey "Software\Microsoft\Windows\CurrentVersion\Uninstall\${prodname}"
 
!define startmenu "$SMPROGRAMS\${prodname}"
!define uninstaller "uninstall.exe"
 
;--------------------------------
 
InstallColors 000000 FFFFFF
XPStyle on
ShowInstDetails hide
ShowUninstDetails hide
 
Name "${prodname}"
Caption "${prodname}"
 
!ifdef icon
Icon "${icon}"
!endif
 
OutFile "${setup}"
 
SetDateSave on
SetDatablockOptimize on
CRCCheck on
SilentInstall normal
 
InstallDir "$PROGRAMFILES\${company}\${prodname}"
InstallDirRegKey HKLM "${regkey}" ""
 
!ifdef licensefile
LicenseText "License"
LicenseData "${srcdir}\${licensefile}"
!endif
 
; pages
; we keep it simple - leave out selectable installation types
 
!ifdef licensefile
Page license
!endif
 
; Page components
Page directory
Page instfiles
 
UninstPage uninstConfirm
UninstPage instfiles
 
;--------------------------------
 
AutoCloseWindow false
; ShowInstDetails show
 
 
!ifdef screenimage
 
; set up background image
; uses BgImage plugin
 
Function .onGUIInit
	; extract background BMP into temp plugin directory
	InitPluginsDir
	File /oname=$PLUGINSDIR\1.bmp "${screenimage}"
 
	BgImage::SetBg /NOUNLOAD /FILLSCREEN $PLUGINSDIR\1.bmp
	BgImage::Redraw /NOUNLOAD
FunctionEnd

Function .onGUIEnd
	; Destroy must not have /NOUNLOAD so NSIS will be able to unload and delete BgImage before it exits
	BgImage::Destroy
FunctionEnd
 
!endif
 
; beginning (invisible) section
Section
 
  WriteRegStr HKLM "${regkey}" "Install_Dir" "$INSTDIR"
  ; write uninstall strings
  WriteRegStr HKLM "${uninstkey}" "DisplayName" "${prodname} (remove only)"
  WriteRegStr HKLM "${uninstkey}" "UninstallString" '"$INSTDIR\${uninstaller}"'
 
!ifdef filetype
  WriteRegStr HKCR "${filetype}" "" "${prodname}"
!endif
 
  WriteRegStr HKCR "${prodname}\Shell\open\command\" "" '"$INSTDIR\${exec} "%1"'
 
!ifdef icon
  WriteRegStr HKCR "${prodname}\DefaultIcon" "" "$INSTDIR\${icon}"
!endif
 
  SetOutPath $INSTDIR
 
 
; package all files, recursively, preserving attributes
; assume files are in the correct places
File /a "${srcdir}\${exec}"
 
!ifdef licensefile
File /a "${srcdir}\${licensefile}"
!endif
 
!ifdef notefile
File /a "${srcdir}\${notefile}"
!endif
 
!ifdef icon
File /a "${srcdir}\${icon}"
!endif
 
!ifdef unicon
File /a "${srcdir}\${unicon}"
!endif

; any application-specific files
!ifdef files
!include "${files}"
!endif
 
  WriteUninstaller "${uninstaller}"
  
SectionEnd
 
; create shortcuts
Section
  
  CreateDirectory "${startmenu}"
  SetOutPath $INSTDIR ; for working directory
!ifdef icon
  CreateShortCut "${startmenu}\${prodname}.lnk" "$INSTDIR\${exec}" "" "$INSTDIR\${icon}"
!else
  CreateShortCut "${startmenu}\${prodname}.lnk" "$INSTDIR\${exec}"
!endif
 
!ifdef unicon
  CreateShortCut "${startmenu}\${unprodname}.lnk" "$INSTDIR\uninstall.exe" "" "$INSTDIR\${unicon}"
!else
  CreateShortCut "${startmenu}\${unprodname}.lnk" "$INSTDIR\uninstall.exe"
!endif

!ifdef notefile
  CreateShortCut "${startmenu}\Release Notes.lnk "$INSTDIR\${notefile}"
!endif
 
!ifdef helpfile
  CreateShortCut "${startmenu}\Documentation.lnk "$INSTDIR\${helpfile}"
!endif
 
!ifdef website
WriteINIStr "${startmenu}\www.mytago.com.url" "InternetShortcut" "URL" ${website}
 ; CreateShortCut "${startmenu}\Web Site.lnk "${website}" "URL"
!endif
 
!ifdef notefile
ExecShell "open" "$INSTDIR\${notefile}"
!endif

CreateShortCut "$DESKTOP\${prodname}.lnk" "$INSTDIR\${exec}" ""
 
SectionEnd
 
; Uninstaller
; All section names prefixed by "Un" will be in the uninstaller
 
UninstallText "This will uninstall ${prodname}."
 
!ifdef unicon
UninstallIcon "${unicon}"
!endif
 
Section "Uninstall"
 
  DeleteRegKey HKLM "${uninstkey}"
  DeleteRegKey HKLM "${regkey}"
 
!ifdef licensefile
Delete "$INSTDIR\${licensefile}"
!endif
 
!ifdef notefile
Delete "$INSTDIR\${notefile}"
!endif
 
!ifdef icon
Delete "$INSTDIR\${icon}"
!endif
 
!ifdef unicon
Delete "$INSTDIR\${unicon}"
!endif

Delete "$INSTDIR\${exec}"
 
!ifdef unfiles
!include "${unfiles}"
!endif

  Delete "$DESKTOP\${prodname}.lnk"

  Delete "$INSTDIR\uninstall.exe"

  Delete "${startmenu}\*.*"

  RMDir "${startmenu}"
  RMDir /r "$INSTDIR"
 
SectionEnd

;Function that calls a messagebox when installation finished correctly
Function .onInstSuccess
  MessageBox MB_OK "Congratulations, You have successfully installed ${prodname}.$\n$\nPlease use the desktop icon to start the program.$\nYou can also start it from the Start menu All Programs list."
FunctionEnd
