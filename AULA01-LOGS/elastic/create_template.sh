#!/bin/bash
curl -X PUT http://localhost:9200/_index_template/observa-template -H 'Content-Type: application/json' -d @index_template.json
