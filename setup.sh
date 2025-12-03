#!/bin/bash

echo "============================================"
echo "  YouTube Downloader - Setup"
echo "============================================"
echo ""

# Verifica se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "[ERRO] Python3 não encontrado! Por favor, instale o Python 3.8+"
    exit 1
fi

# Cria ambiente virtual se não existir
if [ ! -d ".venv" ]; then
    echo "[INFO] Criando ambiente virtual..."
    python3 -m venv .venv
    echo "[OK] Ambiente virtual criado!"
else
    echo "[INFO] Ambiente virtual já existe."
fi

# Ativa o ambiente virtual e instala dependências
echo "[INFO] Instalando dependências..."
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "============================================"
echo "  Setup concluído com sucesso!"
echo "============================================"
echo ""
echo "Para usar o programa:"
echo "  1. Adicione links do YouTube ao arquivo 'links.txt'"
echo "  2. Execute './run.sh' para iniciar os downloads"
echo ""
