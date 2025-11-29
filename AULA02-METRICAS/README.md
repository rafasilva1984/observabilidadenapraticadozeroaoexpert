# LAB 02 — Métricas: A Linguagem Secreta da Performance  
### Observabilidade na Prática — By Rafa Silva

Este LAB foi criado para demonstrar métricas como comportamento — seguindo exatamente o raciocínio da Aula 02.

Inclui:
- Elasticsearch + Kibana em Docker
- Dataset real de **100.000 documentos (Nov/2025)**
- Bulk API otimizado (data stream)
- Script real-time
- Dashboard pronto em NDJSON

---

## 1. Suba o ambiente

```
docker-compose up -d
```

---

## 2. Crie o template do data stream

```
curl -k -X PUT "http://localhost:9200/_index_template/metricas-template"   -H "Content-Type: application/json"   -d @metricas-template.json
```

---

## 3. Importe os 100 mil documentos

```
chmod +x import_bulk.sh
./import_bulk.sh
```

Valide:

```
curl -k "http://localhost:9200/metricas-lab/_count?pretty"
```

---

## 4. Rode o tráfego real-time

```
chmod +x gerar_metricas.sh
./gerar_metricas.sh
```

---

## 5. Configure o Data View

- Pattern: metricas-lab*
- Timefield: @timestamp

---

## 6. Queries úteis

```
endpoint: "/ok"
endpoint: "/slow"
endpoint: "/error"
```

---

## 7. Dashboard pronto

Importe via:
Stack Management → Saved Objects → Import

Arquivo:
```
dash_metricas_lab.ndjson
```

---

## 8. Encerrar

```
docker-compose down
```
