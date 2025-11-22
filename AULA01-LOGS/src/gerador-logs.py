import json
import random
import datetime

services = ["auth", "checkout", "search", "orders", "catalog"]
levels = ["INFO", "WARN", "ERROR"]
endpoints = ["/login", "/pay", "/cart", "/item", "/search"]

output_path = "../data/logs-bulk.ndjson"

with open(output_path, "w", encoding="utf-8") as f:
    for i in range(10000):
        ts = datetime.datetime.utcnow().isoformat()
        latency = random.randint(10, 2000)
        level = random.choices(levels, weights=[80, 15, 5])[0]

        doc = {
            "timestamp": ts,
            "level": level,
            "service": random.choice(services),
            "endpoint": random.choice(endpoints),
            "latency": latency,
            "host": f"server-{random.randint(1,10)}"
        }

        action = { "index": { "_index": "logs-aula01" } }

        f.write(json.dumps(action) + "\n")
        f.write(json.dumps(doc) + "\n")

print(f"✅ BULK NDJSON criado em: {output_path}")
