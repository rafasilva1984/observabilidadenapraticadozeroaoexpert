
#!/usr/bin/env bash
# 02_carga_cenarios_traces.sh
# Gera mais de 100.000 requisições divididas em fases,
# para facilitar a visualização de padrões no mapa de traces.

set -e

URL="${1:-http://localhost:8000/checkout}"

function fase() {
  local total=$1
  local scenario=$2
  local label=$3

  echo ""
  echo ">>> Fase ${label}: ${total} req - cenário=${scenario}"

  for i in $(seq 1 ${total}); do
    curl -s -k "${URL}?scenario=${scenario}" > /dev/null &
    # a cada 200 requisições, faz uma pequena pausa
    if (( $i % 200 == 0 )); then
      sleep 1
    fi
  done
  wait
}

# Fase 1: "dia normal" ~30k
fase 30000 "normal" "1 - Dia normal"

# Fase 2: "pico" ~40k
fase 40000 "pico" "2 - Pico de carga"

# Fase 3: "batch_lento" ~20k
fase 20000 "batch_lento" "3 - Batch de reconciliação lento"

# Fase 4: "externo_lento" ~15k
fase 15000 "externo_lento" "4 - Dependência externa lenta"

echo ""
echo ">>> Carga total concluída ( >100.000 requisições )."
echo "    Agora abra o Kibana → APM → lab-traces-app"
echo "    e explore por intervalo de tempo para enxergar as fases."
