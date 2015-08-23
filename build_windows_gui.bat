C:\Python27\Scripts\pyinstaller -p lib;plugin;service ^
    --hidden-import=asyncore --hidden-import=win32gui_struct --hidden-import=win32gui ^
    --hidden-import=winxpgui --hidden-import=commctrl --hidden-import=pywintypes ^
    --hidden-import=bottle --hidden-import=cgi --hidden-import=hmac --hidden-import=Cookie ^
    --hidden-import=wsgiref --hidden-import=wsgiref.simple_server --hidden-import=wsgiref.handlers ^
    --hidden-import=wsgiref.util --hidden-import=wsgiref.headers ^
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

rmdir dist\nmcontrolwin\_MEI\tk\images /s /q
rmdir dist\nmcontrolwin\_MEI\tcl\tzdata /s /q
rmdir dist\nmcontrolwin\_MEI\tcl\msgs /s /q

del dist\*.pyc /s /q
