#!/usr/bin/env bash
set -e

ELASTIC_URL=${ELASTIC_URL:-http://localhost:9200}

echo "Criando index template metricas-lab-template..."

curl -k -X PUT "${ELASTIC_URL}/_index_template/metricas-lab-template"   -H "Content-Type: application/json"   -d '{
    "index_patterns": ["metricas-lab*"],
    "data_stream": {},
    "template": {
      "mappings": {
        "properties": {
          "@timestamp": { "type": "date" },
          "endpoint":   { "type": "keyword" },
          "latencia_ms":{ "type": "float" },
          "throughput": { "type": "integer" },
          "status_code":{ "type": "integer" }
        }
      }
    }
  }'

echo
echo "Criando data stream metricas-lab..."
curl -k -X PUT "${ELASTIC_URL}/_data_stream/metricas-lab"
echo
echo "Pronto."
