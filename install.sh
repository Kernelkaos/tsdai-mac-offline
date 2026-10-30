#!/bin/bash
set -e

# Script de instalação universal para qualquer Mac (Apple Silicon / macOS)
PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$PROJECT_DIR"

echo "=== Instalador AI Image Transformer (Mac Offline) ==="

# 1. Verifica arquitetura Apple Silicon
ARCH=$(uname -m)
if [ "$ARCH" != "arm64" ]; then
    echo "AVISO: Este pacote foi otimizado para chips Apple Silicon (M1/M2/M3/M4)."
    echo "Arquitetura detectada: $ARCH. A execução via CPU pode ser extremamente lenta."
fi

# 2. Localiza um Python 3 compatível (3.10 até 3.13)
PYTHON_CMD=""
for cmd in python3.13 python3.12 python3.11 python3.10 python3; do
    if command -v "$cmd" >/dev/null 2>&1; then
        VER=$("$cmd" -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
        MAJOR=$("$cmd" -c 'import sys; print(sys.version_info.major)')
        MINOR=$("$cmd" -c 'import sys; print(sys.version_info.minor)')
        if [ "$MAJOR" -eq 3 ] && [ "$MINOR" -ge 10 ] && [ "$MINOR" -le 13 ]; then
            PYTHON_CMD="$cmd"
            echo "Python compatível encontrado: $PYTHON_CMD (versão $VER)"
            break
        fi
    fi
done

# Se não encontrar Python 3.10-3.13 nativo, tenta usar o uv se disponível
if [ -z "$PYTHON_CMD" ]; then
    if command -v uv >/dev/null 2>&1 || [ -f "$HOME/Library/Python/3.15/bin/uv" ]; then
        UV_BIN=$(command -v uv || echo "$HOME/Library/Python/3.15/bin/uv")
        echo "Criando ambiente virtual com Python 3.13 via uv..."
        "$UV_BIN" venv --python 3.13 .venv
        PYTHON_CMD=".venv/bin/python"
    else
        echo "ERRO: Nenhum Python 3.10 a 3.13 encontrado neste Mac."
        echo "Instale o Python 3.11/3.12/3.13 ou uv antes de continuar."
        exit 1
    fi
fi

# 3. Cria venv se ainda não existir
if [ ! -d ".venv" ]; then
    echo "Criando ambiente virtual .venv..."
    "$PYTHON_CMD" -m venv .venv
fi

# 4. Instala dependências
echo "Instalando dependências do requirements.txt..."
.venv/bin/pip install --upgrade pip
.venv/bin/pip install -r requirements.txt

# 5. Verifica se os modelos já estão baixados
echo "Verificando modelos locais..."
if .venv/bin/python -c "from src.core.engine import ImageTransformerEngine; ImageTransformerEngine().check_models()" 2>/dev/null; then
    echo "✓ Todos os modelos necessários estão presentes na pasta models/."
else
    echo "! Modelos não encontrados ou incompletos."
    echo "Para baixar uma única vez (necessário internet), execute:"
    echo "  .venv/bin/python scripts/download_models.py"
fi

echo ""
echo "=== Instalação concluída com sucesso! ==="
echo "Para iniciar o programa:"
echo "  ./scripts/run.sh"
