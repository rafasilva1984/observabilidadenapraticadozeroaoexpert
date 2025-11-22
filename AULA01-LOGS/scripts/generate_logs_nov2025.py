#!/usr/bin/env python3
import json
import random
from datetime import datetime, timedelta
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR.parent / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = DATA_DIR / "logs_bulk_nov2025.ndjson"
INDEX_NAME = "logs-aula01"

services = [
    "checkout-api",
    "pagamentos-service",
    "auth-service",
    "catalogo-api",
    "notificacoes-service",
]

levels = ["INFO", "WARN", "ERROR"]

status_codes = [200, 200, 201, 204, 400, 401, 403, 404, 500, 502]

paths = [
    "/api/checkout",
    "/api/pagamentos",
    "/api/login",
    "/api/produtos",
    "/api/notificacoes",
]

messages_by_level = {
    "INFO": [
        "Requisição processada com sucesso",
        "Operação concluída",
        "Serviço respondeu dentro da latência esperada",
        "Requisição autenticada",
    ],
    "WARN": [
        "Latência acima do esperado",
        "Timeout na chamada ao serviço externo, tentativa será refeita",
        "Número de tentativas de login acima da média",
        "Fila de mensagens crescendo além do normal",
    ],
    "ERROR": [
        "Falha ao processar pagamento",
        "Erro inesperado na camada de persistência",
        "Exceção não tratada no fluxo de checkout",
        "Timeout definitivo ao chamar provedor externo",
    ],
}

def gerar_periodo_inteiro():
    return datetime(2025, 11, 1, 0, 0, 0)

def gerar_documento_normal(ts):
    service = random.choice(services)
    level = random.choice(levels)
    status = random.choice(status_codes)
    
    return {
        "@timestamp": ts.isoformat(timespec="seconds") + "Z",
        "service": service,
        "level": level,
        "http_status": status,
        "path": random.choice(paths),
        "order_id": random.randint(100000, 999999),
        "customer_id": random.randint(1000, 9999),
        "latency_ms": random.randint(20, 900),
        "message": random.choice(messages_by_level[level]),
        "env": random.choice(["dev", "hml", "prod"]),
    }

# --------------------------
# INCIDENTES AJUSTADOS
# --------------------------

def incidente_checkout(ts):
    return {
        "@timestamp": ts.isoformat(timespec="seconds") + "Z",
        "service": "checkout-api",
        "level": random.choice(["WARN", "ERROR"]),
        "http_status": random.choice([500, 502]),
        "path": "/api/checkout",
        "order_id": random.randint(100000, 999999),
        "customer_id": random.randint(1000, 9999),
        "latency_ms": random.randint(1500, 4000),
        "message": "Exceção não tratada no fluxo de checkout",
        "env": "prod",
    }

def incidente_auth(ts):
    return {
        "@timestamp": ts.isoformat(timespec="seconds") + "Z",
        "service": "auth-service",
        "level": random.choice(["WARN", "ERROR"]),
        "http_status": random.choice([401, 403]),
        "path": "/api/login",
        "order_id": None,
        "customer_id": random.randint(1000, 9999),
        "latency_ms": random.randint(10, 90),
        "message": "Número de tentativas de login acima da média",
        "env": "prod",
    }

def incidente_pagamento(ts):
    return {
        "@timestamp": ts.isoformat(timespec="seconds") + "Z",
        "service": "pagamentos-service",
        "level": "ERROR",
        "http_status": random.choice([500, 502, 504]),
        "path": "/api/pagamentos",
        "order_id": random.randint(100000, 999999),
        "customer_id": random.randint(1000, 9999),
        "latency_ms": random.randint(1200, 4500),
        "message": "Timeout definitivo ao chamar provedor externo",
        "env": "prod",
    }

def main():
    total_logs = 100000
    inicio = gerar_periodo_inteiro()

    incidentes_checkout = []
    incidentes_auth = []
    incidentes_pag = []

    # INCIDENTE 1 — checkout-api (20/11, 08h até 20h)
    start = datetime(2025, 11, 20, 8, 0, 0)
    end = datetime(2025, 11, 20, 20, 0, 0)
    for i in range(2500):
        ts = start + timedelta(minutes=random.randint(0, int((end - start).total_seconds()/60)))
        incidentes_checkout.append(incidente_checkout(ts))

    # INCIDENTE 2 — auth-service (21/11, 09h às 11h)
    start = datetime(2025, 11, 21, 9, 0, 0)
    end = datetime(2025, 11, 21, 11, 0, 0)
    for i in range(1500):
        ts = start + timedelta(minutes=random.randint(0, int((end - start).total_seconds()/60)))
        incidentes_auth.append(incidente_auth(ts))

    # INCIDENTE 3 — pagamentos-service (21/11, 14h às 18h)
    start = datetime(2025, 11, 21, 14, 0, 0)
    end = datetime(2025, 11, 21, 18, 0, 0)
    for i in range(2000):
        ts = start + timedelta(minutes=random.randint(0, int((end - start).total_seconds()/60)))
        incidentes_pag.append(incidente_pagamento(ts))

    docs_incidentes = (
        incidentes_checkout +
        incidentes_auth +
        incidentes_pag
    )

    qtd_incidentes = len(docs_incidentes)
    qtd_normais = total_logs - qtd_incidentes

    with OUTPUT_FILE.open("w", encoding="utf-8") as f:
        # logs normais
        for _ in range(qtd_normais):
            ts = inicio + timedelta(minutes=random.randint(0, 30*24*60))
            f.write(json.dumps({"index": {"_index": INDEX_NAME}}) + "\n")
            f.write(json.dumps(gerar_documento_normal(ts)) + "\n")

        # logs de incidente
        for doc in docs_incidentes:
            f.write(json.dumps({"index": {"_index": INDEX_NAME}}) + "\n")
            f.write(json.dumps(doc) + "\n")

    print(f"NDJSON gerado com {total_logs} documentos e incidentes nos dias 20 e 21/11!")
    print(f"Caminho: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
