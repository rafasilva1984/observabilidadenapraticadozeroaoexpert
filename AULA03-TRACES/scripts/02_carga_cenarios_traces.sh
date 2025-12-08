#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${BASE_URL:-http://localhost:8000}"
ENDPOINT="${BASE_URL}/checkout"

CONCURRENCY=${CONCURRENCY:-20}      # número de requisições em paralelo
WARMUP_REQS=50                      # aquecimento rápido
PEAK_REQS=400                       # pico principal
BURST_REQS=200                      # burst final

echo "=== [TRACES LAB] Carga rápida de cenários ==="
echo "Endpoint: ${ENDPOINT}"
echo "Concorrência: ${CONCURRENCY}"
echo

fire_batch() {
  local label="$1"
  local count="$2"

  echo ">> Cenário: ${label} | Requisições: ${count}"

  seq 1 "${count}" | xargs -n1 -P "${CONCURRENCY}" -I{} \
    curl -s -o /dev/null "${ENDPOINT}" || true

  echo "   Cenário '${label}' concluído."
  echo
}

SECONDS=0

# 1) Aquecimento rápido – poucas requisições só pra garantir serviço/trace
fire_batch "Aquecimento (tráfego leve)" "${WARMUP_REQS}"

# 2) Pico principal – tráfego intenso para encher o APM
fire_batch "Pico de tráfego (checkout em massa)" "${PEAK_REQS}"

# 3) Burst final – mais algumas requisições para fechar o desenho
fire_batch "Burst final (variação rápida)" "${BURST_REQS}"

echo "=== Carga rápida concluída em ${SECONDS}s ==="
echo "Agora abra o Kibana em: Observability → APM → Services"
echo "Confira o serviço da aplicação e visualize:"
echo "- Transactions (pico claro de volume)"
echo "- Waterfall (spans com diferentes tempos)"
echo "- Traces (jornada completa das requisições)"
