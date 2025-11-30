# LAB02 – Métricas: A Linguagem Secreta da Performance

Este lab acompanha a Aula 02 da trilha **Observabilidade na Prática**  
> _“Métricas: A Linguagem Secreta da Performance”_

Aqui você vai:

- Subir um ambiente **Elasticsearch + Kibana 8.x** via Docker (sem autenticação, focado em LAB).
- Criar um **data stream de métricas** (`metricas-lab`).
- Gerar uma **massa histórica de ~100.000 documentos** simulando 3 fases de comportamento do endpoint `/slow`:
  1. Fase normal
  2. Degradação lenta
  3. Sistema sofrendo
- Construir os dashboards que aparecem na aula.
- Interpretar as métricas com olhar de **Engenharia de Confiabilidade / SRE**.

> ⚠️ **Importante (Lab / Educação)**  
> - Ambiente SEM segurança, SEM TLS e SEM autenticação.  
> - Use apenas em ambiente local / estudo.  
> - Em produção, sempre habilite TLS, autenticação e usuários mínimos.

---

## 1. Estrutura do projeto

```text
lab02-metricas-linguagem-secreta-performance/
├─ docker-compose.yml
├─ README.md
├─ scripts/
│  ├─ create_template_and_datastream.sh
│  ├─ generate_metricas_lab_bulk.py
│  └─ load_bulk_metricas_lab.sh
└─ extras/
   └─ LAB02_dashboards_e_falas.html
```

---

## 2. Subindo Elasticsearch e Kibana

1. Na raiz do projeto, execute:

```bash
docker-compose up -d
```

2. Aguarde 40–60 segundos e teste o Elasticsearch:

```bash
curl -k http://localhost:9200
```

Você deve ver um JSON com `tagline` parecido com:

```json
{
  "name" : "lab02-elasticsearch",
  "cluster_name" : "docker-cluster",
  ...
  "tagline" : "You Know, for Search"
}
```

3. Acesse o Kibana em:  
   **http://localhost:5601**

Não há autenticação neste lab.

---

## 3. Criando o data stream `metricas-lab`

Vamos criar um **index template** com mapeamento básico e, em seguida, o **data stream**.

Na pasta `scripts`, execute:

```bash
cd scripts
./create_template_and_datastream.sh
```

Esse script faz dois `curl`:

1. Cria o template `metricas-lab-template`.
2. Cria o data stream `metricas-lab`.

Você pode conferir o resultado com:

```bash
curl -k http://localhost:9200/_data_stream/metricas-lab?pretty
```

---

## 4. Gerando a massa histórica de dados (novembro/2025)

Agora vamos gerar uma massa **realista** com ~100.000 documentos, simulando 3 fases para o endpoint `/slow`.

### 4.1. Estratégia de comportamento

- **Período total:** 23/11/2025 até 30/11/2025 (UTC).
- **Endpoints simulados:** `/ok`, `/slow`, `/error`.
- **Por hora, para cada endpoint:** 200 documentos.

#### `/ok` – endpoint saudável

- Latência: 200–260 ms  
- Throughput: 80–110  
- Status: 200

#### `/slow` – protagonista da aula

| Fase | Período (nov/2025) | Latência (ms) | Throughput | Comportamento |
|------|--------------------|---------------|------------|---------------|
| 🟢 Normal           | 23–24           | 300–340     | 60–80     | Sistema estável |
| 🟡 Degradação lenta | 25–27           | 350–430     | 70–90     | Lentidão crescente |
| 🔴 Sofrendo         | 28–30           | 430–520     | 30–50     | Sistema saturado |

#### `/error` – baixa frequência, alta latência

- Latência: 500–650 ms  
- Throughput: 5–15  
- Status: 500 / 502 / 504

### 4.2. Gerando o arquivo NDJSON de bulk

Na pasta `scripts`, execute:

```bash
cd scripts
./generate_metricas_lab_bulk.py
# ou
python3 generate_metricas_lab_bulk.py
```

Isso irá gerar o arquivo:

```text
bulk_metricas_lab_novembro.ndjson
```

---

## 5. Carregando o bulk no Elasticsearch

Ainda na pasta `scripts`, rode:

```bash
./load_bulk_metricas_lab.sh bulk_metricas_lab_novembro.ndjson
```

Esse script irá:

1. Enviar o bulk para o data stream `metricas-lab`.
2. Exibir a contagem de documentos:

```json
{
  "count" : 100000,
  "_shards" : { ... }
}
```

(Valor exato pode variar um pouco, mas estará nessa ordem de grandeza.)

---

## 6. Criando o Data View no Kibana

1. No Kibana, vá em **Stack Management → Data Views → Create data view**.
2. Configure:

   - **Name:** `metricas-lab`
   - **Index pattern:** `metricas-lab*`
   - **Timestamp field:** `@timestamp`

3. Salve.

A partir daqui você já consegue usar **Discover** e **Lens** com esses dados.

---

## 7. Dashboards do LAB02

Os dashboards principais que usamos na aula são:

### 7.1. [LAB02] Latência Média por Endpoint

**Objetivo:** ver a “personalidade” de latência de cada endpoint ao longo do tempo.

1. Abra **Visualize Library → Create visualization → Lens**.
2. Selecione o data view `metricas-lab`.
3. No tipo de gráfico, escolha **Bar vertical stacked**.
4. Arraste `@timestamp` para **Horizontal axis**.  
   - Intervalo: `12h` (ou `Auto` se preferir).
5. Arraste `latencia_ms` para **Vertical axis**.  
   - Agregação: `Median of latencia_ms`.
6. Arraste `endpoint` para **Break down by**.
7. Salve como: **[LAB02] Latência Média por Endpoint**.

**Fala sugerida para a aula:**

> “Aqui a gente começa a ver que cada endpoint tem uma ‘cara’.  
>  O `/ok` é mais estável, o `/slow` já vive num patamar mais alto, e o `/error` aparece pouco, mas sempre caro.”

---

### 7.2. [LAB02] Throughput por Endpoint

**Objetivo:** enxergar como o volume de chamadas está distribuído.

1. Crie uma nova visualização Lens.
2. Tipo: **Bar vertical stacked**.
3. `@timestamp` em **Horizontal axis** (mesmo intervalo do painel anterior).
4. `throughput` em **Vertical axis** com `Median of throughput`.
5. `endpoint` em **Break down by`**.
6. Salve como: **[LAB02] Throughput por Endpoint**.

**Fala sugerida:**

> “Esse gráfico responde a pergunta: onde está a maior parte da carga?  
>  E é importante fazer essa pergunta antes da CPU bater 100%.”

---

### 7.3. [LAB02] Degradação de Latência do `/slow` (linha + tendência)

**Objetivo:** mostrar como a latência do `/slow` muda de patamar ao longo dos dias.

1. Crie uma nova visualização Lens.
2. Tipo: **Line**.
3. Filtro KQL no topo:  
   ```
   endpoint : "/slow"
   ```
4. `@timestamp` no **Horizontal axis** com intervalo `3h`.
5. `latencia_ms` no **Vertical axis** como `Median of latencia_ms` (primeira série).
6. Duplique essa métrica para criar uma segunda série.
7. Na segunda série, configure um **intervalo mínimo maior** (por exemplo 12h ou 24h) para que a linha fique mais suave (tendência).
8. Ajuste a cor e espessura para destacar a tendência.
9. Salve como: **[LAB02] Degradação de Latência – /slow**.

**O que você deve ver:**

- Entre 23–24/11: patamar em ~310–330 ms.
- Entre 25–27/11: patamar subindo para ~360–400 ms.
- Entre 28–30/11: patamar mais alto, ~450–500 ms.

**Fala sugerida:**

> “Repara que a linha de tendência não volta mais para o nível dos primeiros dias.  
>  A métrica está te dizendo: ‘eu já não sou o mesmo de antes’. Isso é degradar sem quebrar.”

---

### 7.4. [LAB02] Latência x Throughput – `/slow`

**Objetivo:** mostrar quando o sistema está apenas sendo mais exigido vs. quando está sofrendo de verdade.

1. Crie uma nova visualização Lens.
2. Tipo: **Line**.
3. Filtro KQL:  
   ```
   endpoint : "/slow"
   ```
4. `@timestamp` no **Horizontal axis**.
5. Série 1:
   - `latencia_ms` em **Vertical axis**.
   - Agregação: `Median of latencia_ms`.
   - Nome da série: `Latência /slow (ms)`.
6. Adicione uma nova série:
   - Campo: `throughput`.
   - Agregação: `Median of throughput`.
   - Nome: `Throughput /slow`.
   - Configure essa série para usar o **Right axis**.
7. Salve como: **[LAB02] Latência x Throughput – /slow**.

**Leitura esperada:**

- Nas fases iniciais, throughput alto + latência relativamente controlada.
- Na fase final, latência alta + throughput caindo → sistema sofrendo.

**Fala sugerida:**

> “Quando o throughput aumenta e a latência sobe um pouco e depois estabiliza, o sistema só está sendo exigido.  
>  Quando o throughput começa a cair enquanto a latência dispara, aí virou sofrimento operacional.”

---

## 8. Arquivo de apoio – Dashboards e falas

No diretório `extras/` você encontrará o arquivo:

```text
LAB02_dashboards_e_falas.html
```

Abra esse arquivo no navegador.  
Ele contém:

- Objetivo de cada dashboard.
- Passo a passo em texto.
- Falas sugeridas para você usar na aula.

Use esse HTML como **guia de bastidor** na hora de gravar.

---

## 9. Limpeza do ambiente (opcional)

Para parar os containers:

```bash
docker-compose down
```

Para parar e apagar os dados:

```bash
docker-compose down -v
```

> ⚠️ Cuidado: o comando com `-v` remove todos os dados do Elasticsearch deste lab.

---

## 10. Resumo do que você aprendeu

- Subir rapidamente um ambiente Elasticsearch + Kibana para LAB.
- Criar um data stream de métricas.
- Gerar massa de dados histórica com comportamento realista.
- Construir dashboards que mostram **tendência**, não só “foto”.
- Ler métricas como **comportamento**, não apenas como números soltos.

Esse é o tipo de visão que diferencia quem só “olha dashboard” de quem realmente **conduz a operação**.

Boas métricas, boa aula e boa observabilidade na prática! 🚀
