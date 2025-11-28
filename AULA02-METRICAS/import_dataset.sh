#!/bin/bash
FILE="metricas_dataset.jsonl"
INDEX="metricas-lab"

if [ ! -f "$FILE" ]; then
  echo "Arquivo $FILE não encontrado na pasta atual."
  exit 1
fi

echo "Iniciando importação de dados para o índice $INDEX ..."
count=0
while IFS= read -r line; do
  curl -s -k -X POST "http://localhost:9200/${INDEX}/_doc" \
    -H "Content-Type: application/json" \
    -d "$line" > /dev/null
  count=$((count+1))
  if (( $count % 10000 == 0 )); then
    echo "$count documentos enviados..."
  fi
done < "$FILE"

echo "Importação concluída. Total de documentos enviados: $count"
