import random
from datetime import datetime, timedelta

OUTPUT_FILE = "logs_bulk_nov2025.ndjson"
INDEX_NAME = "logs-aula01"

# Quantidade alvo de documentos
BACKGROUND_DOCS = 105_000  # logs "normais"
# o script ainda gera mais alguns milhares nos incidentes

random.seed(42)  # para ter comportamento reproduzível

services = [
    {
        "name": "auth-service",
        "endpoints": ["/api/v1/login", "/api/v1/refresh", "/api/v1/logout"],
        "latency_base": 40,
    },
    {
        "name": "checkout-api",
        "endpoints": ["/api/v1/checkout", "/api/v1/cart", "/api/v1/payment"],
        "latency_base": 80,
    },
    {
        "name": "order-service",
        "endpoints": ["/api/v1/orders", "/api/v1/orders/status"],
        "latency_base": 60,
    },
    {
        "name": "payment-gateway",
        "endpoints": ["/api/v1/pay", "/api/v1/refund"],
        "latency_base": 120,
    },
    {
        "name": "search-api",
        "endpoints": ["/api/v1/search", "/api/v1/suggest"],
        "latency_base": 50,
    },
]

hosts = ["app-01", "app-02", "app-03", "app-04", "app-05"]

levels = ["INFO", "WARN", "ERROR"]


def random_timestamp_november_2025():
    """Gera um timestamp aleatório entre 2025-11-01 e 2025-11-30."""
    start = datetime(2025, 11, 1, 0, 0, 0)
    end = datetime(2025, 11, 30, 23, 59, 59)
    delta = end - start
    # segundos aleatórios dentro do range
    random_seconds = random.randint(0, int(delta.total_seconds()))
    ts = start + timedelta(seconds=random_seconds)
    # formato ISO8601 com Z
    return ts.strftime("%Y-%m-%dT%H:%M:%SZ")


def make_message(level, service_name, endpoint):
    if level == "INFO":
        return f"{service_name} handled request to {endpoint} successfully"
    elif level == "WARN":
        return f"{service_name} slow response detected on {endpoint}, retry may be required"
    else:
        return f"{service_name} error processing request on {endpoint}, upstream dependency failure"


def random_latency(base):
    # pequena variação em torno de um valor médio
    return max(1, int(random.gauss(base, base * 0.3)))


def write_doc(f, ts, level, service_name, endpoint, host, message, latency):
    meta = {"index": {"_index": INDEX_NAME}}
    doc = {
        "@timestamp": ts,
        "level": level,
        "service": {"name": service_name},
        "host": {"name": host},
        "endpoint": endpoint,
        "latency_ms": latency,
        "message": message,
    }
    import json
    f.write(json.dumps(meta) + "\n")
    f.write(json.dumps(doc) + "\n")


def generate_background_logs(f):
    for _ in range(BACKGROUND_DOCS):
        ts = random_timestamp_november_2025()
        svc = random.choice(services)
        service_name = svc["name"]
        endpoint = random.choice(svc["endpoints"])
        host = random.choice(hosts)

        # Probabilidades gerais por nível
        r = random.random()
        if r < 0.8:
            level = "INFO"
        elif r < 0.95:
            level = "WARN"
        else:
            level = "ERROR"

        latency = random_latency(svc["latency_base"])
        message = make_message(level, service_name, endpoint)
        write_doc(f, ts, level, service_name, endpoint, host, message, latency)


def generate_incident_sequence(
    f, start_ts, service_name, endpoint, host_base, base_latency
):
    """
    Gera uma sequência clara de incidente:
    - 10 min antes: INFO
    - 10 min de WARN crescendo
    - 5 min de ERROR com alta latência
    """
    # Janela de tempo do incidente
    start = start_ts              # início "oficial" (WARN)
    pre_start = start - timedelta(minutes=10)
    error_start = start + timedelta(minutes=10)
    end = error_start + timedelta(minutes=5)

    # 1) 10 min antes – baseline INFO
    current = pre_start
    while current < start:
        for host in hosts[:3]:
            ts = current.strftime("%Y-%m-%dT%H:%M:%SZ")
            level = "INFO"
            latency = random_latency(base_latency)
            msg = f"{service_name} normal operation on {endpoint}"
            write_doc(f, ts, level, service_name, endpoint, host, msg, latency)
        current += timedelta(seconds=30)  # a cada 30s

    # 2) WARN – 10 minutos a partir do start
    current = start
    while current < error_start:
        for host in hosts[:3]:
            ts = current.strftime("%Y-%m-%dT%H:%M:%SZ")
            level = "WARN"
            latency = random_latency(base_latency * 2)
            msg = f"{service_name} high latency and retries on {endpoint}"
            write_doc(f, ts, level, service_name, endpoint, host, msg, latency)
        current += timedelta(seconds=20)  # mais frequente

    # 3) ERROR – 5 minutos
    current = error_start
    while current < end:
        for host in hosts[:3]:
            ts = current.strftime("%Y-%m-%dT%H:%M:%SZ")
            level = "ERROR"
            latency = random_latency(base_latency * 3)
            msg = f"{service_name} failing calls on {endpoint}, circuit breaker open"
            write_doc(f, ts, level, service_name, endpoint, host, msg, latency)
        current += timedelta(seconds=15)


def main():
    # Incidentes planejados (horários fixos que você pode usar na live)
    incidentes = [
        {
            "start": datetime(2025, 11, 5, 10, 0, 0),
            "service_name": "checkout-api",
            "endpoint": "/api/v1/checkout",
            "base_latency": 120,
        },
        {
            "start": datetime(2025, 11, 12, 21, 30, 0),
            "service_name": "payment-gateway",
            "endpoint": "/api/v1/pay",
            "base_latency": 160,
        },
        {
            "start": datetime(2025, 11, 23, 3, 0, 0),
            "service_name": "order-service",
            "endpoint": "/api/v1/orders",
            "base_latency": 100,
        },
    ]

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        # 1) Logs "normais" espalhados entre 01 e 30/11
        generate_background_logs(f)

        # 2) Sequências de incidente bem marcadas
        for inc in incidentes:
            generate_incident_sequence(
                f,
                inc["start"],
                inc["service_name"],
                inc["endpoint"],
                "app-01",
                inc["base_latency"],
            )

    print(f"Arquivo NDJSON gerado: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
