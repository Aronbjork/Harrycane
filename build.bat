@echo off
echo =======================================
echo   Building Harrycane Game to .exe
echo =======================================
echo.

echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Building executable...
pyinstaller --onefile --windowed --name Harrycane --icon=NONE game.py

echo.
echo =======================================
echo   Build Complete!
echo =======================================
echo.
echo Your game executable is in the 'dist' folder!
echo Run: dist\Harrycane.exe
echo.
pause
