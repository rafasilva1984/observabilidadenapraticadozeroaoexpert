import json
import random
import datetime

services = ["auth", "checkout", "search", "orders", "catalog"]
levels = ["INFO", "WARN", "ERROR"]
endpoints = ["/login", "/pay", "/cart", "/item", "/search"]

dataset = []

for i in range(10000):
    ts = datetime.datetime.utcnow().isoformat()
    latency = random.randint(10, 2000)
    level = random.choices(levels, weights=[80, 15, 5])[0]

    dataset.append({
        "timestamp": ts,
        "level": level,
        "service": random.choice(services),
        "endpoint": random.choice(endpoints),
        "latency": latency,
        "host": f"server-{random.randint(1,10)}"
    })

# grava o arquivo NDJSON na pasta ../data
output_path = "../data/logs-simulados.json"

with open(output_path, "w", encoding="utf-8") as f:
    for line in dataset:
        f.write(json.dumps(line) + "\n")

print(f"✅ Arquivo gerado com sucesso em: {output_path}")
