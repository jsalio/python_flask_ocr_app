@echo off
setlocal EnableDelayedExpansion

echo ============================================================
echo  ocr-cli -- Build para Windows
echo ============================================================

:: Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python no encontrado. Instala Python 3.9+ desde https://python.org
    pause & exit /b 1
)

:: Verificar Tesseract
tesseract --version >nul 2>&1
if errorlevel 1 (
    echo [AVISO] Tesseract no encontrado en PATH.
    echo         Descargalo desde: https://github.com/tesseract-ocr/tesseract
    echo         El ejecutable se compilara igual, pero necesita Tesseract en runtime.
    echo.
)

:: Instalar dependencias de build
echo [1/3] Instalando dependencias...
pip install pyinstaller pillow pytesseract pypdf click --quiet
if errorlevel 1 ( echo [ERROR] Fallo pip install & pause & exit /b 1 )

:: Limpiar build anterior
echo [2/3] Limpiando build anterior...
if exist build   rmdir /s /q build
if exist dist    rmdir /s /q dist

:: Compilar
echo [3/3] Compilando ejecutable...
pyinstaller ocr_cli.spec
if errorlevel 1 ( echo [ERROR] Fallo PyInstaller & pause & exit /b 1 )

echo.
echo ============================================================
echo  Listo! Ejecutable generado en: dist\ocr-cli.exe
echo ============================================================
echo.
echo Prueba rapida:
echo   dist\ocr-cli.exe --help
echo   dist\ocr-cli.exe convert --help
echo   dist\ocr-cli.exe langs
echo   dist\ocr-cli.exe info
echo.
pause
