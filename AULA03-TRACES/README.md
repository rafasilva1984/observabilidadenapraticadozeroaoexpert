# LAB – Traces na Observabilidade (Aula 03)

Este LAB reconstrói o mapa de uma requisição usando Elastic APM + OpenTelemetry + aplicação FastAPI.

## 📌 Estrutura

```
lab_traces/
 ├── docker-compose.yml
 ├── app/
 │    ├── app.py
 │    ├── requirements.txt
 │    └── Dockerfile
 ├── collector/
 │    └── config.yml
 └── docs/
```

## 🚀 1. Subindo o ambiente

```
docker-compose up -d
```

Acesse:

- Kibana: http://localhost:5601
- Aplicação: http://localhost:8000/checkout

## 🔍 2. Onde ver os traces

1. Abra o Kibana  
2. Vá em APM → Services  
3. Clique no serviço lab-traces-app  
4. Abra Transactions → waterfall  

## 🧪 3. Gerando carga

```
watch -n1 curl -k http://localhost:8000/checkout
```

Cada chamada gera um novo trace.

## 🧩 4. Simulando lentidão

Edite `app.py`:

```
time.sleep(random.uniform(1.5,3.0))
```

Rebuild:

```
docker-compose build app
docker-compose up -d
```

Agora o mapa (trace) mostrará o trecho lento.

---


## ⚙️ 5. Scripts de carga – mais de 100.000 traces

Dentro da pasta `scripts/` você encontra dois utilitários de carga:

### 5.1. Carga básica (aquecimento)

```bash
cd lab_traces
./scripts/01_carga_basica.sh
```

Isso gera ~**1.000 requisições** no cenário `normal`, só para garantir que tudo está funcionando.

---

### 5.2. Carga completa por fases ( > 100.000 requisições )

```bash
cd lab_traces
./scripts/02_carga_cenarios_traces.sh
```

As fases são:

1. **Fase 1 – Dia normal (~30.000 req)**  
   - `scenario=normal`  
   - Latências baixas e estáveis.

2. **Fase 2 – Pico de carga (~40.000 req)**  
   - `scenario=pico`  
   - Mesma jornada, mas com tempos maiores.

3. **Fase 3 – Batch de reconciliação lento (~20.000 req)**  
   - `scenario=batch_lento`  
   - Span `reconciliar_extrato_batch` fica bem mais demorado.

4. **Fase 4 – Dependência externa lenta (~15.000 req)**  
   - `scenario=externo_lento`  
   - Span `webhook_parceiro_externo` aparece como gargalo.

> 💡 No Kibana APM, filtre por intervalos de tempo e por atributo `lab.scenario`
> para enxergar claramente cada fase no mapa de traces.

---
