#!/bin/bash

echo "🔥 Enviando logs para o Elasticsearch..."

curl -k -X POST "https://localhost:9200/_bulk" \
  -H "Content-Type: application/x-ndjson" \
  --user elastic:changeme \
  --data-binary "@../data/logs-bulk.ndjson"

echo
echo "✅ Envio finalizado!"
