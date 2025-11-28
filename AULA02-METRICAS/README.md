
# LAB — Métricas: A Linguagem Secreta da Performance

Este LAB foi criado para acompanhar a Aula 02 da trilha **Observabilidade na Prática**.

Ele foi pensado para ser **o mais realista possível**, com:
- Ambiente completo em Docker (Elasticsearch 8.14 + Kibana)
- Dataset com **100.000 documentos** de métricas simuladas
- Script de carga em tempo real
- Passo a passo para criar os gráficos no Kibana
- Arquivo NDJSON com objetos salvos (dashboard + visualizações) como referência

> Importante: este LAB é para **uso educacional/local**. A segurança (auth/SSL) está desabilitada para simplificar o uso em ambiente de estudo.

---

## 1. Pré-requisitos

- Docker e Docker Compose instalados
- `curl` instalado
- Porta **9200** livre (Elasticsearch)
- Porta **5601** livre (Kibana)

---

## 2. Subindo o ambiente

Na pasta onde o arquivo `docker-compose.yml` está:

```bash
docker-compose up -d
```

Verifique se o Elasticsearch está de pé:

```bash
curl -k http://localhost:9200
```

Você deve ver um JSON com informações do cluster.

---

## 3. Configurando o template de métricas

Aplicar o template:

```bash
curl -k -X PUT "http://localhost:9200/_index_template/metricas-template" \
  -H "Content-Type: application/json" \
  -d @metricas-template.json
```

Isso garante:
- Campo `@timestamp` como `date`
- Campos de métricas numéricos (`latencia_ms`, `throughput`)
- Campo `endpoint` como `keyword`

---

## 4. Carregando os 100.000 documentos históricos

O arquivo `metricas_dataset.jsonl` contém **100.000 documentos**, com timestamps começando em:

- `2025-01-01T09:00:00` em diante, 1 segundo por documento

Para carregar esse dataset, use:

```bash
chmod +x import_dataset.sh
./import_dataset.sh
```

O script irá:
- Ler linha a linha o arquivo `metricas_dataset.jsonl`
- Enviar cada documento para o índice `metricas-lab`
- Simular um histórico consistente de métricas para análise

> Obs: Isso pode levar alguns minutos dependendo da máquina, mas deixa o ambiente rico para exploração.

---

## 5. Gerando carga em tempo real (opcional, para usar no vídeo)

Depois de importar o histórico, você pode simular tráfego em tempo real:

```bash
chmod +x gerar_metricas.sh
./gerar_metricas.sh
```

O script vai:
- Sortear entre `/ok`, `/slow` e `/error`
- Gerar métricas coerentes para cada endpoint:
  - `/ok`: latência baixa, throughput alto, HTTP 200
  - `/slow`: latência alta, throughput baixo, HTTP 200
  - `/error`: latência intermediária, throughput muito baixo, HTTP 500
- Escrever continuamente em `metricas-lab`

Isso é perfeito para mostrar no vídeo:
- a curva mudando ao vivo
- o impacto no gráfico
- o comportamento antes do incidente

Para parar o script, basta `CTRL + C`.

---

## 6. Configurando o Kibana

Acesse:

```text
http://localhost:5601
```

Crie um **Data View** chamado, por exemplo: `metricas-lab*`

- Pattern: `metricas-lab*`
- Campo de tempo: `@timestamp`

Salve.

---

## 7. Explorando no Discover

Algumas queries para usar em aula:

### 7.1 Ver todas as métricas

Sem filtro, apenas ordene por `@timestamp` desc.

### 7.2 Filtrar por endpoint

```kql
endpoint: "/slow"
```

Mostra claramente:
- latência mais alta
- throughput menor
- padrão de degradação

```kql
endpoint: "/error"
```

Mostra:
- concentração de `status_code: 500`
- throughput baixíssimo
- padrão de erro sistemático

```kql
endpoint: "/ok"
```

Mostra:
- baseline saudável
- latência baixa
- throughput estável

---

## 8. Criando os gráficos no Lens (passo a passo)

### 8.1 Gráfico de latência por endpoint

1. No Kibana, vá em **Visualize Library > Create visualization > Lens**
2. Selecione o data view `metricas-lab*`
3. Configure:
   - **Y-axis**: `Average` de `latencia_ms`
   - **X-axis**: `@timestamp`
   - **Break down by**: `endpoint`
4. Tipo de visualização: **Line**

> Interpretação:
> - `/ok` deve se manter com linhas baixas
> - `/slow` deve se destacar com latências bem mais altas
> - `/error` pode ficar intermediário, mas com menos pontos

---

### 8.2 Gráfico de throughput por endpoint

1. Novo gráfico Lens
2. Configure:
   - **Y-axis**: `Sum` de `throughput`
   - **X-axis**: `@timestamp`
   - **Break down by**: `endpoint`
3. Tipo: **Area** ou **Line**

> Interpretação:
> - `/ok` domina o throughput (mais requisições)
> - `/slow` aparece com volume menor
> - `/error` quase sempre abaixo de todos

---

### 8.3 Heatmap de status HTTP

1. Novo gráfico Lens
2. Eixos:
   - **X-axis**: `@timestamp`
   - **Y-axis**: `status_code`
   - **Value**: `Count`
3. Tipo: **Heatmap**

> Interpretação:
> - `200` será predominante
> - `500` mostrará faixas específicas de problema

---

## 9. Dashboard pronto (via NDJSON)

O arquivo `dash_metricas_lab.ndjson` contém:

- 1 data view de referência
- 2 visualizações principais (latência x tempo, throughput x tempo)
- 1 dashboard montado com essas visualizações

> Atenção: as versões do Kibana podem mudar alguns campos internos.  
> Se o import falhar, use o NDJSON como **referência de estrutura** e crie os gráficos na mão seguindo a seção 8.

### Importando o NDJSON

No Kibana:

1. Vá em **Stack Management > Saved Objects**
2. Clique em **Import**
3. Selecione o arquivo `dash_metricas_lab.ndjson`
4. Marque para criar novos objetos

---

## 10. Encerrando o LAB

Para encerrar o ambiente:

```bash
docker-compose down
```

---

## 11. Ideias de extensão

- Adicionar novos endpoints, como `/cache`, `/db`, `/auth`
- Introduzir variação por `service_name`
- Incluir campo de `cluster` ou `host` para múltiplas instâncias
- Usar esse mesmo dataset para introduzir **traces** na próxima aula

---

Qualquer ajuste fino de versão (8.x) costuma ser simples:
- mudar o data view
- refazer uma visualização
- reorganizar o dashboard

A estrutura principal de raciocínio sobre **métricas como comportamento** permanece a mesma.
