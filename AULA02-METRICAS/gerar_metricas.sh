#!/bin/bash
endpoints=("/ok" "/slow" "/error")
while true; do
  ep=${endpoints[$RANDOM % ${#endpoints[@]}]}
  case $ep in
    "/ok")
      lat=$((20 + RANDOM % 40))
      status=200
      th=$((50 + RANDOM % 30))
      ;;
    "/slow")
      lat=$((200 + RANDOM % 300))
      status=200
      th=$((10 + RANDOM % 5))
      ;;
    "/error")
      lat=$((80 + RANDOM % 40))
      status=500
      th=$((5 + RANDOM % 3))
      ;;
  esac
  curl -s -k -X POST http://localhost:9200/metricas-lab/_doc     -H "Content-Type: application/json"     -d "{
      \"@timestamp\": \"$(date -Is)\",
      \"endpoint\": \"$ep\",
      \"latencia_ms\": $lat,
      \"status_code\": $status,
      \"throughput\": $th
    }"
  sleep 1
done
