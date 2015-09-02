C:\Python27\Scripts\pyinstaller -p lib;plugin;service ^
    --hidden-import=asyncore --hidden-import=win32gui_struct --hidden-import=win32gui ^
    --hidden-import=winxpgui --hidden-import=commctrl --hidden-import=pywintypes ^
    --hidden-import=bottle --hidden-import=cgi --hidden-import=hmac --hidden-import=Cookie ^
    --hidden-import=wsgiref --hidden-import=wsgiref.simple_server --hidden-import=wsgiref.handlers ^
    --hidden-import=wsgiref.util --hidden-import=wsgiref.headers ^
    --noconfirm --icon=./lib/icon.ico nmcontrol.py

@if %errorlevel% EQU 0 goto continue
@pause
:continue

mkdir dist\nmcontrol\lib\
mkdir dist\nmcontrol\plugin\
mkdir dist\nmcontrol\service\

xcopy lib dist\nmcontrol\lib /s /e /h /y
xcopy plugin dist\nmcontrol\plugin /s /e /h /y
xcopy service dist\nmcontrol\service /s /e /h /y

rmdir dist\nmcontrol\_MEI\tk\images /s /q
rmdir dist\nmcontrol\_MEI\tcl\tzdata /s /q
rmdir dist\nmcontrol\_MEI\tcl\msgs /s /q

del dist\*.pyc /s /q
