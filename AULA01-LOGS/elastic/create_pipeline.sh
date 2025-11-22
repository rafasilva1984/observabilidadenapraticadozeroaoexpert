#!/bin/bash
curl -X PUT http://localhost:9200/_ingest/pipeline/normaliza-logs -H 'Content-Type: application/json' -d @ingest_pipeline.json
