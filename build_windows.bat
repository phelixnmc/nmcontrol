C:\Python27\Scripts\pyinstaller -p lib;plugin;service ^
    --hidden-import=asyncore --hidden-import=win32gui_struct --hidden-import=win32gui ^
    --hidden-import=winxpgui --hidden-import=commctrl --hidden-import=pywintypes ^
    --noconfirm --noconsole --icon=./lib/icon.ico nmcontrolwin.pyw

@if %errorlevel% EQU 0 goto continue
@pause
:continue

mkdir dist\nmcontrolwin\lib\
mkdir dist\nmcontrolwin\plugin\
mkdir dist\nmcontrolwin\service\

xcopy lib dist\nmcontrolwin\lib /s /e /h /y
xcopy plugin dist\nmcontrolwin\plugin /s /e /h /y
xcopy service dist\nmcontrolwin\service /s /e /h /y
