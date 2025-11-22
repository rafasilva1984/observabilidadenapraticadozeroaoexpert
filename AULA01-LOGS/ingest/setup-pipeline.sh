#!/bin/bash
curl -X PUT "http://localhost:9200/_ingest/pipeline/pipeline-logs" -H 'Content-Type: application/json' -d @pipeline-logs.json
