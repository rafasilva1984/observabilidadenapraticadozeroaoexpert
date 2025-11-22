import json, random, datetime
services=["auth","checkout","search","orders","catalog"]
levels=["INFO","WARN","ERROR"]
endpoints=["/login","/pay","/cart","/item","/search"]
dataset=[]
for i in range(10000):
    ts=datetime.datetime.utcnow().isoformat()
    latency=random.randint(10,2000)
    level=random.choices(levels,weights=[80,15,5])[0]
    dataset.append({
        "timestamp": ts,
        "level": level,
        "service": random.choice(services),
        "endpoint": random.choice(endpoints),
        "latency": latency,
        "host": f"server-{random.randint(1,10)}"
    })
with open("../data/logs-simulados.json","w") as f:
    for line in dataset: f.write(json.dumps(line)+"
")
