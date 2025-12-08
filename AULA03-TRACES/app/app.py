
from fastapi import FastAPI
from fastapi import Query
import time
import random

from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry import trace

# === OpenTelemetry base config ===
resource = Resource(attributes={
    "service.name": "lab-traces-app",
    "service.environment": "lab-aula-03",
})

provider = TracerProvider(resource=resource)
processor = BatchSpanProcessor(
    OTLPSpanExporter(endpoint="http://otel-collector:4318/v1/traces")
)
provider.add_span_processor(processor)

trace.set_tracer_provider(provider)
tracer = trace.get_tracer(__name__)

app = FastAPI(title="Lab Traces – Observabilidade na Prática")
FastAPIInstrumentor.instrument_app(app)

# === Simulação de cenários de jornada ===
# normal        -> latência baixa e estável
# pico          -> muita concorrência, latência mediana
# batch_lento   -> etapa específica muito lenta (reconciliação / extrato)
# externo_lento -> dependência externa lenta (webhook / parceiro)

def _simulate_downstream_call(name: str, base: float, jitter: float):
    """Cria um span filho simulando uma chamada downstream."""
    with tracer.start_as_current_span(name) as span:
        duration = random.uniform(base, base + jitter)
        # registra a duração planejada como atributo
        span.set_attribute("lab.simulated_duration_ms", int(duration * 1000))
        time.sleep(duration)


@app.get("/checkout")
def checkout(scenario: str = Query("normal", description="normal|pico|batch_lento|externo_lento")):
    """Endpoint principal usado no LAB.

    Cada cenário altera a jornada e os tempos dos spans,
    facilitando a visualização no mapa de traces.
    """
    with tracer.start_as_current_span(" fluxo_checkout ") as span:
        span.set_attribute("lab.scenario", scenario)

        # etapa 1 – recebendo requisição / validação básica
        _simulate_downstream_call("validar_requisicao", 0.02, 0.05)

        # etapa 2 – orquestração principal (depende do cenário)
        if scenario == "normal":
            _simulate_downstream_call("servico_pagamento", 0.05, 0.15)
            _simulate_downstream_call("atualizar_extrato", 0.03, 0.05)

        elif scenario == "pico":
            # mesma jornada, mas com tempos um pouco maiores
            _simulate_downstream_call("servico_pagamento", 0.15, 0.25)
            _simulate_downstream_call("atualizar_extrato", 0.08, 0.15)

        elif scenario == "batch_lento":
            _simulate_downstream_call("servico_pagamento", 0.05, 0.10)
            # extrato preso em reconciliação / batch lento
            _simulate_downstream_call("reconciliar_extrato_batch", 0.7, 1.3)

        elif scenario == "externo_lento":
            _simulate_downstream_call("servico_pagamento", 0.05, 0.1)
            _simulate_downstream_call("webhook_parceiro_externo", 0.4, 0.9)
            _simulate_downstream_call("atualizar_extrato", 0.05, 0.08)

        else:
            # fallback para garantir que nunca quebra
            _simulate_downstream_call("servico_pagamento", 0.05, 0.10)
            _simulate_downstream_call("atualizar_extrato", 0.03, 0.05)

        # etapa 3 – finalização / resposta
        _simulate_downstream_call("publicar_evento_fila", 0.01, 0.03)

        return {
            "status": "ok",
            "scenario": scenario,
        }


@app.get("/health")
def health():
    return {"ok": True}
