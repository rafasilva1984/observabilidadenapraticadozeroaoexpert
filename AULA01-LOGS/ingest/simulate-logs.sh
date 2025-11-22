#!/bin/bash
curl -X POST "http://localhost:9200/observa-logs-default/_bulk?pipeline=pipeline-logs" -H 'Content-Type: application/x-ndjson' --data-binary @../data/logs-simulados.json
