set PYTHONOPTIMIZE=2

pyinstaller --noconfirm ^
    --log-level=INFO ^
    --upx-dir="upx-3.95-win64" ^
    --upx-exclude="vcruntime140.dll" ^
    --upx-exclude="msvcp140.dll" ^
    --upx-exclude="qwindows.dll" ^
    --upx-exclude="qwindowsvistastyle.dll" ^
    --add-binary="./rrrocket.exe;." ^
    --add-data="./settings.ini;." ^
    --add-data="./calculated_logo_flair_resized.png;." ^
    --add-data="./README;." ^
    --icon="calculated_circle.ico" ^
    run.py
