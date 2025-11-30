#!/usr/bin/env bash
set -e

ELASTIC_URL=${ELASTIC_URL:-http://localhost:9200}
BULK_FILE=${1:-bulk_metricas_lab_novembro.ndjson}

if [ ! -f "${BULK_FILE}" ]; then
  echo "Arquivo de bulk não encontrado: ${BULK_FILE}"
  exit 1
fi

echo "Carregando bulk a partir de: ${BULK_FILE}"
curl -k -X POST "${ELASTIC_URL}/metricas-lab/_bulk?refresh=true"   -H "Content-Type: application/x-ndjson"   --data-binary "@${BULK_FILE}"

echo
echo "Contagem de documentos em metricas-lab:"
curl -k "${ELASTIC_URL}/metricas-lab/_count?pretty"
echo
