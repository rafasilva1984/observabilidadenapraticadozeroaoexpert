#!/usr/bin/env bash
set -euo pipefail

# URL do Elasticsearch (sem HTTPS, sem usuário/senha)
ES_URL=${ES_URL:-http://localhost:9200}

# Arquivo NDJSON gerado pelo script Python
NDJSON_FILE=${1:-../data/logs_bulk_nov2025.ndjson}

if [ ! -f "$NDJSON_FILE" ]; then
  echo "Arquivo NDJSON não encontrado: $NDJSON_FILE"
  echo "Caminho esperado: $NDJSON_FILE"
  exit 1
fi

echo "Enviando bulk para $ES_URL a partir de $NDJSON_FILE..."

curl \
  -H "Content-Type: application/x-ndjson" \
  -XPOST "$ES_URL/_bulk?pretty&refresh=true" \
  --data-binary @"$NDJSON_FILE"
