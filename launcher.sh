#!/bin/bash

CAMINHO="$HOME/.scripts/hypr/"
# Caminho do arquivo config.py e do ambiente virtual
CONFIG_PATH="${CAMINHO}/config.py"

# Verifica se o processo já está em execução
if pgrep -f "${CONFIG_PATH}" > /dev/null; then
    # Se o processo estiver em execução, finaliza o processo
    echo "O processo já está em execução. Finalizando..."
    pkill -f "${CONFIG_PATH}"
else
    # Se o processo não estiver em execução, inicia o processo
    echo "O processo não está em execução. Iniciando..."
    ${CONFIG_PATH}   # O "&" não faz o menor sentido aqui, e vai atrapalhar o usuário
fi
