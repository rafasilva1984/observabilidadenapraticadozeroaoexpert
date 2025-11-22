#!/bin/bash
curl -k -X POST "http://localhost:9200/observa-logs-aula01/_bulk?pipeline=normaliza-logs"   -H "Content-Type: application/x-ndjson"   --data-binary "@../data/logs_bulk_nov2025.ndjson"
