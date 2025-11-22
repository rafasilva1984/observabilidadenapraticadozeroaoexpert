#!/usr/bin/env python3
import json
import random
from datetime import datetime, timedelta
from pathlib import Path

# Caminhos
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

status_codes = [200, 200, 200, 201, 204, 400, 401, 403, 404, 500, 502]

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
        "Timeout definitivo ao chamar serviço externo",
    ],
}

def gerar_timestamp_base():
    # Gerar logs ao longo de novembro de 2025
    inicio = datetime(2025, 11, 1, 0, 0, 0)
    return inicio

def gerar_documentos(qtd=500):
    base = gerar_timestamp_base()
    for i in range(qtd):
        # Espalhar os logs ao longo do mês
        ts = base + timedelta(minutes=random.randint(0, 30*24*60))

        service = random.choice(services)
        level = random.choice(levels)
        status = random.choice(status_codes)
        path = random.choice(paths)

        msg = random.choice(messages_by_level[level])

        doc = {
            "@timestamp": ts.isoformat(timespec="seconds") + "Z",
            "service": service,
            "level": level,
            "http_status": status,
            "path": path,
            "order_id": random.randint(100000, 999999),
            "customer_id": random.randint(1000, 9999),
            "latency_ms": random.randint(20, 3500),
            "message": msg,
            "env": random.choice(["dev", "hml", "prod"]),
        }

        yield doc

def main():
    with OUTPUT_FILE.open("w", encoding="utf-8") as f:
        for doc in gerar_documentos(qtd=1000):
            # Linha de metadados do bulk
            meta = {"index": {"_index": INDEX_NAME}}
            f.write(json.dumps(meta) + "\n")
            # Linha do documento
            f.write(json.dumps(doc, ensure_ascii=False) + "\n")

    print(f"Arquivo NDJSON gerado: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
