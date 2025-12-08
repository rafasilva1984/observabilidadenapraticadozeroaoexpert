from fastapi import FastAPI
import time
import random

from elasticapm.contrib.starlette import make_apm_client, ElasticAPM

apm_config = {
    "SERVICE_NAME": "lab-traces-app",
    "SERVER_URL": "http://apm-server:8200",
    "ENVIRONMENT": "lab-traces",
}
apm_client = make_apm_client(apm_config)

app = FastAPI()
app.add_middleware(ElasticAPM, client=apm_client)


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/checkout")
async def checkout():
    with apm_client.capture_span("validar_carrinho", "custom"):
        time.sleep(random.uniform(0.05, 0.2))

    with apm_client.capture_span("calcular_frete", "custom"):
        time.sleep(random.uniform(0.05, 0.4))

    # span que às vezes é lento (simulando serviço externo)
    with apm_client.capture_span("aprovar_pagamento_gateway", "external"):
        delay = random.choice([0.1, 0.2, 0.3, 0.8, 1.2])
        time.sleep(delay)

    with apm_client.capture_span("atualizar_extrato", "db"):
        time.sleep(random.uniform(0.05, 0.15))

    return {"status": "ok", "delay_gateway": delay}
