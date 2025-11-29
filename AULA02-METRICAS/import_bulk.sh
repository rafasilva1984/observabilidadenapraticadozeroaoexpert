#!/bin/bash
FILE="metricas_bulk.jsonl"
INDEX="metricas-lab"
echo "Importando via BULK API..."
curl -k -X POST "http://localhost:9200/_bulk" -H "Content-Type: application/x-ndjson" --data-binary "@${FILE}"
echo "Importação finalizada."
