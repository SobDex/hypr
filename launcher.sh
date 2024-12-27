#!/bin/bash

# Caminho do arquivo config.py e do ambiente virtual
config_path="$HOME/.scripts/hypr/config.py"
# venv_python="$HOME/.scripts/venv/bin/python"

# Verifica se o processo já está em execução
if pgrep -f "$config_path" > /dev/null; then
    # Se o processo estiver em execução, finaliza o processo
    echo "O processo já está em execução. Finalizando..."
    pkill -f "$config_path"
else
    # Se o processo não estiver em execução, inicia o processo
    echo "O processo não está em execução. Iniciando..."
    $venv_python $config_path &
fi
