# LAB02 – Métricas: A Linguagem Secreta da Performance
Versão Completa – Observabilidade na Prática

## 📌 Visão Geral
Este laboratório acompanha a Aula 02 da trilha **Observabilidade na Prática** e tem como objetivo ensinar, na prática, como métricas contam histórias — e como identificar padrões de degradação antes que o incidente estoure.

Você vai aprender:
- A subir um ambiente **Elasticsearch + Kibana 8.x**
- Criar um **Data Stream realista**
- Gerar **massa histórica com 100.000 documentos**
- Simular **3 fases operacionais**:
  - 🟢 Normal
  - 🟡 Degradação lenta
  - 🔴 Sistema sofrendo
- Criar dashboards no Kibana replicando o que usamos na aula
- Interpretar cada visualização como um verdadeiro Eng. de Confiabilidade

---

## 🧱 1. Estrutura do Projeto
```
lab02-metricas/
├── docker-compose.yml
├── scripts/
│   ├── generate_historical.sh
│   ├── generate_realtime.sh
│   └── helpers/
│       └── random_gen.py
├── data/
│   └── metricas-lab-historical.ndjson
├── dashboards/
│   ├── latencia_por_endpoint.ndjson
│   ├── throughput_por_endpoint.ndjson
│   ├── degradacao_lenta.ndjson
│   ├── latencia_vs_throughput.ndjson
└── README.md
```

---

## 🚀 2. Subindo Ambiente com Docker
```bash
docker-compose up -d
```

Aguarde 40s–60s até o cluster inicializar.

Acesse:
- **Elasticsearch:** http://localhost:9200
- **Kibana:** http://localhost:5601

Usuário padrão (lab):
```
elastic / changeme
```

---

## 📡 3. Criando o Data Stream
```bash
curl -k -u elastic:changeme   -X PUT http://localhost:9200/_index_template/metricas-lab   -H 'Content-Type: application/json'   -d '{
    "index_patterns": ["metricas-lab*"],
    "data_stream": {},
    "template": {
      "mappings": {
        "properties": {
          "@timestamp": {"type": "date"},
          "endpoint": {"type": "keyword"},
          "latencia_ms": {"type": "integer"},
          "status_code": {"type": "keyword"},
          "throughput": {"type": "integer"}
        }
      }
    }
  }'
```

Criar o Data Stream:
```bash
curl -k -u elastic:changeme   -X PUT "http://localhost:9200/metricas-lab"
```

---

## 🗂️ 4. Massa de Dados — A Estratégia
Para este laboratório, criamos **100.000 documentos** simulando 3 movimentos reais:

| Fase | Período | Comportamento | Descrição |
|------|---------|----------------|-----------|
| 🟢 Normal | início do mês | 300–340ms | Sistema estável |
| 🟡 Degradação lenta | meio do mês | 340–370ms | Lentidão crescente |
| 🔴 Sistema sofrendo | fim do mês | 370–420ms | Piora clara e constante |

Essas três fases permitem que os dashboards mostrem de forma clara:

- A curva “entortando”
- O throughput oscilando
- O sistema começando a sofrer antes de explodir

---

## ⚙️ 5. Ingestão — Bulk Histórico (Rápido)
```bash
curl -k -u elastic:changeme   -H "Content-Type: application/x-ndjson"   -X POST "http://localhost:9200/metricas-lab/_bulk"   --data-binary @data/metricas-lab-historical.ndjson
```

---

## 🔄 6. Ingestão Contínua em Tempo Real
```bash
bash scripts/generate_realtime.sh
```

Esse script envia novos documentos a cada 1 segundo simulando tráfego real.

---

## 📊 7. Criando os Dashboards no Kibana

### **Dashboard 1 — Latência Média por Endpoint**
Gráfico: **Barra vertical empilhada**  
Eixo X: `@timestamp` (12h)  
Eixo Y: `median(latencia_ms)`  
Breakdown: `endpoint`

**Insight para gravação:**
> “Repara como o /slow começa a subir devagarzinho… estável, mas subindo. Isso é o rastro do problema antes dele acontecer.”

---

### **Dashboard 2 — Throughput por Endpoint**
Gráfico: **Barra vertical empilhada**  
Eixo Y: `median(throughput)`  
Breakdown: `endpoint`

**Insight:**
> “Nenhum sistema sofre sozinho. Se a latência sobe e o throughput cai… tem algo segurando a fila.”

---

### **Dashboard 3 — Degradação Lenta do /slow**
Gráfico: **Linha**  
Filtro: `endpoint : "/slow"`  
Y: `median(latencia_ms)`  
Intervalo: 3h  
Adicione nova série:  
- **Moving Average – window 12**

**Insight poderoso:**
> “Olha a tendência. Às vezes o que você não vê num ponto individual… aparece quando conecta os pontos.”

---

### **Dashboard 4 — Latência vs Throughput**
Gráfico: **Linha dupla ou área + linha**  
Série 1: `latencia_ms`  
Série 2: `throughput`

**Insight:**
> “Essas duas curvas são irmãos gêmeos brigados. Quando uma sobe, a outra cai.”

---

## 🧠 8. Leitura Avançada – O que você deve perceber
### ✔ Mudança de forma da curva  
Mesmo que a média seja parecida, você vai notar que a curva perde estabilidade.

### ✔ Oscilação maior  
Quanto mais o sistema sofre, mais a latência “respira pesado”.

### ✔ Throughput irregular  
Antes da queda, ele começa a “engasgar”.

### ✔ Padrões de rastro  
Nenhum incidente surge do nada — a métrica avisa antes.

---

## 🎤 9. Falas Prontas para o LAB (para gravação)
Inclui falas naturais que você pode usar no vídeo:

### Ao abrir o Kibana:
> “Sempre começo olhando latência. Ela é o batimento cardíaco do sistema.”

### Ao mostrar o /slow:
> “Olha essa curva… parece normal, mas não é. Ela está cansando.”

### Ao mostrar moving average:
> “Aqui fica impossível ignorar. A tendência denuncia tudo.”

### Ao comparar throughput:
> “Isso aqui é clássico: fila aumentando, serviço não respondendo, downstream sofrendo.”

---

## 🏁 10. Conclusão do LAB
Você aprendeu:

- A gerar métricas reais e comportamentais
- A identificar padrões antes do incidente
- A interpretar dashboards como um SRE profissional
- A enxergar a métrica não como número… mas como **comportamento**

---

## 📎 Créditos do Projeto
Criado para a trilha **Observabilidade na Prática**  
Por: **Rafa Silva**

