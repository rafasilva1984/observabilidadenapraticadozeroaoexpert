#!/bin/bash
INDEX="metricas-lab"
while true; do
  ENDPOINT=$(shuf -e /ok /slow /error -n1)
  if [ "$ENDPOINT" = "/ok" ]; then
    LAT=$(shuf -i 20-60 -n1)
    STATUS=200
    TH=$(shuf -i 40-90 -n1)
  elif [ "$ENDPOINT" = "/slow" ]; then
    LAT=$(shuf -i 200-500 -n1)
    STATUS=200
    TH=$(shuf -i 5-15 -n1)
  else
    LAT=$(shuf -i 80-140 -n1)
    STATUS=500
    TH=$(shuf -i 1-5 -n1)
  fi
  NOW=$(date -Iseconds)
  curl -s -k -X POST "http://localhost:9200/${INDEX}/_doc"     -H "Content-Type: application/json"     -d "{"@timestamp":"$NOW","endpoint":"$ENDPOINT","latencia_ms":$LAT,"status_code":$STATUS,"throughput":$TH}" > /dev/null
  echo "Enviado: $ENDPOINT | $LAT ms | status $STATUS | th $TH"
  sleep 1
done
