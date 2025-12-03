#!/bin/bash

# Verifica se o ambiente virtual existe
if [ ! -d ".venv" ]; then
    echo "[ERRO] Ambiente virtual não encontrado!"
    echo "Execute './setup.sh' primeiro para configurar o projeto."
    exit 1
fi

# Ativa o ambiente virtual e executa o script
source .venv/bin/activate
python downloader.py
