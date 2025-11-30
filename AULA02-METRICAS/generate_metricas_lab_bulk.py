#!/usr/bin/env python3
import json
import random
from datetime import datetime, timedelta

DATA_STREAM = "metricas-lab"
OUTPUT_FILE = "bulk_metricas_lab_novembro.ndjson"

start = datetime(2025, 11, 23, 0, 0, 0)
end   = datetime(2025, 11, 30, 23, 0, 0)

# ~100k docs: 200 docs/hora por endpoint
DOCS_PER_HOUR_PER_ENDPOINT = 200
endpoints = ["/ok", "/slow", "/error"]

def fase_slow(ts):
    """
    Retorna (lat_min, lat_max, thr_min, thr_max) para o /slow
    dependendo do período do mês.
    """
    if ts < datetime(2025, 11, 25):
        # Fase 1 - normal
        return (300, 340, 60, 80)
    elif ts < datetime(2025, 11, 28):
        # Fase 2 - degradação lenta
        return (350, 430, 70, 90)
    else:
        # Fase 3 - sistema sofrendo
        return (430, 520, 30, 50)

def generate_documents():
    current = start
    while current <= end:
        for ep in endpoints:
            for _ in range(DOCS_PER_HOUR_PER_ENDPOINT):
                if ep == "/ok":
                    lat = random.randint(200, 260)
                    thr = random.randint(80, 110)
                    status = 200
                elif ep == "/slow":
                    lat_min, lat_max, thr_min, thr_max = fase_slow(current)
                    lat = random.randint(lat_min, lat_max)
                    thr = random.randint(thr_min, thr_max)
                    status = 200
                else:  # /error
                    lat = random.randint(500, 650)
                    thr = random.randint(5, 15)
                    status = random.choice([500, 502, 504])

                doc = {
                    "@timestamp": current.isoformat() + "Z",
                    "endpoint": ep,
                    "latencia_ms": lat,
                    "throughput": thr,
                    "status_code": status
                }
                yield doc
        current += timedelta(hours=1)

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    for doc in generate_documents():
        # data stream -> op_type create
        meta = {"create": {"_index": DATA_STREAM}}
        f.write(json.dumps(meta) + "\n")
        f.write(json.dumps(doc) + "\n")

print(f"Arquivo gerado: {OUTPUT_FILE}")
