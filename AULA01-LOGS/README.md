# LAB 01 – Logs: A Verdade que Ninguém te Contou  
## Observabilidade na Prática — Elastic 8.12  
Este LAB simula um ambiente real de Observabilidade utilizando logs. Aqui você vai subir um ambiente Elastic 8.12 completo, criar pipelines profissionais, gerar mais de 10.000 logs realistas (INFO/WARN/ERROR), enviar logs em massa via Bulk API, visualizar padrões no Kibana, importar um dashboard completo e diagnosticar falhas reais como especialista. Este é o primeiro LAB da trilha Observabilidade na Prática: Do Zero ao Expert. 
# Arquitetura do LAB  
Gerador de Logs → Pipeline → Template → Índice → Kibana → Dashboard  
# 1. Subindo o Ambiente Elastic 8.12  
Acesse a pasta do ambiente:  
cd docker  
Suba o ambiente:  
docker-compose up -d  
Acesse o Kibana em http://localhost:5601  
# 2. Instalando o Pipeline de Ingestão  
O pipeline realiza normalização do timestamp, conversão automática do nível (INFO/WARN/ERROR), quebra do JSON e preenchimento de campos auxiliares. Instale executando:  
cd ingest  
./setup-pipeline.sh  
# 3. Instalando o Template do Índice  
O template define mapeamentos corretos, campos keyword, ajuste de shards e estrutura otimizada para logs. Execute:  
./setup-template.sh  
# 4. Gerando 10.000 Logs Realistas  
Entre no diretório do gerador:  
cd src  
Execute:  
python3 gerador-logs.py  
Isso gera o arquivo data/logs-simulados.json contendo mais de 10.000 logs realistas com níveis INFO, WARN e ERROR, latência variável, múltiplos serviços, endpoints e hosts.  
# 5. Enviando Logs para o Elasticsearch  
Dentro da pasta ingest execute:  
./simulate-logs.sh  
O script envia todos os logs massivamente via Bulk API e usa o pipeline pipeline-logs, criando o índice observa-logs-default.  
# 6. Importando o Dashboard no Kibana  
Acesse Kibana → Stack Management → Saved Objects → Import e importe o arquivo:  
kibana/dashboard-logs.ndjson  
O dashboard inclui gráficos de distribuição de níveis, serviços mais críticos, latência média, tendência temporal, heatmap de logs e eventos recentes.  
# 7. Diagnosticando o Ambiente  
Execute o script de diagnóstico:  
cd utils  
./diagnose.sh  
Ele exibe: total de logs ingeridos, distribuição INFO/WARN/ERROR, serviços com mais erros, latência média por serviço e horários de pico.  
# 8. Consultas importantes  
O arquivo utils/exemplos-de-queries.txt contém consultas úteis como top serviços, logs de erro, latência média, logs por minuto, distribuição por níveis e detecção manual de anomalias.  
# 9. O que você aprende neste LAB  
Estruturar logs profissionais, normalizar e indexar logs corretamente, identificar padrões INFO → WARN → ERROR, detectar picos e anomalias, montar dashboards úteis, diagnosticar incidentes reais e entender o fluxo completo de ingestão.  
# Conclusão  
Este LAB é o primeiro passo da trilha Observabilidade na Prática: Do Zero ao Expert. Aqui você aprendeu os fundamentos: Logs → Pipeline → Template → Dashboard → Diagnóstico. Nos próximos módulos, você evoluirá para latência avançada, tracing, OpenTelemetry, APM, FinOps, anomalias com ML e IA aplicada a Log Analytics. Prepare-se para o próximo nível. 🚀
