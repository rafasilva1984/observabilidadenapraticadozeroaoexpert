#!/bin/bash

echo "🔥 Enviando logs para o Elasticsearch..."

curl --X POST "http://localhost:9200/_bulk" \
  -H "Content-Type: application/x-ndjson" \
  --data-binary "@../data/logs-bulk.ndjson"

echo
echo "✅ Envio finalizado!"
