@echo off

:: Verifica se o ambiente virtual existe
if not exist ".venv" (
    echo [ERRO] Ambiente virtual nao encontrado!
    echo Execute 'setup.bat' primeiro para configurar o projeto.
    pause
    exit /b 1
)

:: Ativa o ambiente virtual e executa o script
call .venv\Scripts\activate.bat
python downloader.py

echo.
pause
