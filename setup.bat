@echo off
echo ============================================
echo   YouTube Downloader - Setup
echo ============================================
echo.

:: Verifica se Python esta instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Python nao encontrado! Por favor, instale o Python 3.8+
    echo Download: https://www.python.org/downloads/
    pause
    exit /b 1
)

:: Cria ambiente virtual se nao existir
if not exist ".venv" (
    echo [INFO] Criando ambiente virtual...
    python -m venv .venv
    echo [OK] Ambiente virtual criado!
) else (
    echo [INFO] Ambiente virtual ja existe.
)

:: Ativa o ambiente virtual e instala dependencias
echo [INFO] Instalando dependencias...
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt

echo.
echo ============================================
echo   Setup concluido com sucesso!
echo ============================================
echo.
echo Para usar o programa:
echo   1. Adicione links do YouTube ao arquivo 'links.txt'
echo   2. Execute 'run.bat' para iniciar os downloads
echo.
pause
