#!/bin/bash
FILE="metricas_bulk.jsonl"
INDEX="metricas-lab"
echo "Importando via Bulk API para data stream..."
curl -k -X POST "http://localhost:9200/${INDEX}/_bulk?pretty&refresh=true"   -H "Content-Type: application/x-ndjson"   --data-binary "@${FILE}"
