
#!/usr/bin/env bash
# 01_carga_basica.sh
# Gera ~1.000 requisições no cenário normal, apenas para aquecer o ambiente.

set -e

URL="${1:-http://localhost:8000/checkout}"

echo ">>> Gerando ~1000 requisições (cenario=normal) em ${URL}"

for i in $(seq 1 1000); do
  curl -s -k "${URL}?scenario=normal" > /dev/null &
  # pequeno intervalo para não explodir o host local
  if (( $i % 50 == 0 )); then
    sleep 1
  fi
done

wait
echo ">>> Carga básica concluída."
