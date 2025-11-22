#!/bin/bash
curl -X PUT "http://localhost:9200/_index_template/observa-logs-template" -H 'Content-Type: application/json' -d @template.json
