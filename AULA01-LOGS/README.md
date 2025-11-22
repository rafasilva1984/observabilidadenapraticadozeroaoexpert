# 📘 AULA 01 — LOGS  
## **Trilha: Observabilidade na Prática — Do Zero ao Expert**

### **A verdade que ninguém te contou sobre logs — e como eles revelam problemas antes do incidente acontecer.**

---

## 🔥 Visão Geral

Este repositório contém o **LAB completo da Aula 01 – LOGS**, primeira etapa da trilha **Observabilidade na Prática: Do Zero ao Expert**.

Aqui você aprenderá:

- Como funciona a anatomia real dos logs  
- Como ler WARN → INFO → ERROR de forma profissional  
- Como detectar um incidente antes dele acontecer  
- Como criar pipeline de ingestão profissional (padrão real de mercado)  
- Como simular 110.000+ logs reais com incidentes (Novembro/2025)  
- Como importar dashboards e analisar comportamento no Kibana  
- Como se posicionar como analista de Observabilidade sênior  

Este laboratório simula o comportamento de microserviços reais, variando latência, carga, frequência e padrões de falha.

---

# 🧩 Arquitetura do Diretório

AULA01-LOGS/
├── elastic/
│   ├── docker-compose.yml
│   ├── ingest_pipeline.json
│   ├── index_template.json
│   ├── create_pipeline.sh
│   ├── create_template.sh
│   ├── create_index.sh
│
├── scripts/
│   ├── generate_logs_nov2025.py
│   ├── load_bulk.sh
│
├── data/
│   ├── logs_bulk_nov2025.ndjson
│   ├── incident_timeline.md
│
├── kibana/
│   ├── aula01-logs-dashboard.ndjson
│   ├── visualizations.ndjson
│
├── docs/
│   ├── incident-diagram.png
│   ├── timeline-checkout.png
│   ├── timeline-payment.png
│   ├── timeline-order.png
│
└── README.md

---

# 🚀 1. Subindo o Ambiente — Elasticsearch + Kibana (8.12)

Dentro da pasta:

cd elastic
docker compose up -d

Após subir:

- Kibana → http://localhost:5601  
- Elasticsearch → http://localhost:9200  

---

# 🛠️ 2. Criando Template, Pipeline e Índice

cd elastic

### Criar Template
./create_template.sh

### Criar Pipeline
./create_pipeline.sh

### Criar Índice
./create_index.sh

O índice criado será:

observa-logs-aula01

Ele segue automaticamente o template:

observa-logs-*

---

# 📦 3. Gerando 110.000+ Logs (Novembro/2025)

Na pasta de scripts:

cd scripts
python generate_logs_nov2025.py

O script:

- Cria mais de 110 mil logs
- Com timestamps entre **01/11/2025 → 30/11/2025**
- Com JSON interno no campo `message` (compatível com pipeline)
- Gera 3 incidentes reais:
  - **05/11 — checkout-api**
  - **12/11 — payment-gateway**
  - **23/11 — order-service**

Saída:

data/logs_bulk_nov2025.ndjson

---

# 📤 4. Ingestão (Bulk)

cd scripts
./load_bulk.sh

Depois confira no Kibana Dev Tools:

GET observa-logs-aula01/_count

Exemplo:

{"count": 110423}

---

# 📊 5. Importando o Dashboard da Aula

No Kibana:

Stack Management → Saved Objects → Import

Importe:

kibana/aula01-logs-dashboard.ndjson

Isso criará automaticamente:

- Data View: `observa-logs-*`
- Saved Search: “Aula 01 – Todos os logs”
- Saved Search: “Aula 01 – Incidentes WARN/ERROR”
- Dashboard completo da aula

---

# 🔍 6. Explorando o Dashboard

O dashboard foi construído para ensinar o aluno a **ler logs com consciência operacional**.

### Painel 1 — Todos os Logs (fluxo normal)
### Painel 2 — WARN e ERROR (padrões do incidente)

Use esse dashboard para demonstrar:

- Como o WARN aparece **antes** do erro  
- Como o INFO muda de volume  
- Como a latência começa a oscilar  
- Como a linha do tempo revela o início da falha  

Este é o exato comportamento de ambientes reais.

---

# 🧠 7. A História Real dos Incidentes

Os incidentes incluídos foram projetados para demonstração:

| Data | Serviço | Descrição |
|------|---------|-----------|
| **05/11/2025 10:00** | checkout-api | Latência sobe → WARN sequenciais → ERROR |
| **12/11/2025 21:30** | payment-gateway | Fila congestionada → INFO sobe → WARN → ERROR |
| **23/11/2025 03:00** | order-service | Picos constantes → WARN → serviço degrada |

Imagens em:

docs/

---

# 🧪 8. Reexecutando o LAB

docker compose down -v
docker compose up -d
cd elastic
./create_template.sh
./create_pipeline.sh
./create_index.sh
cd scripts
python generate_logs_nov2025.py
./load_bulk.sh

---

# 📚 9. Objetivo Educacional

Este LAB foi construído para te transformar em alguém capaz de:

- Interpretar logs como narrativa  
- Identificar padrões antes do colapso  
- Utilizar pipelines profissionais  
- Construir ingestão escalável  
- Ler comportamento de sistemas distribuídos  
- Explicar incidentes para times, gestão ou clientes  

---

# 💬 10. Autor

Trilha criada por **Rafael Silva**  
Projeto: **Observabilidade na Prática — Do Zero ao Expert**  
LinkedIn: https://linkedin.com/in/rafael-silva-leader-coordenador  
YouTube: https://youtube.com/@observabilidadenapratica
