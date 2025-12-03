from fastapi import FastAPI, HTTPException
from .models import GenerateRequest, GenerateResponse
from .guardrails import guardrails
from . import parser as P
from .sqlbuilder import build_select

app = FastAPI(title="SQL Generator (MVP)", version="0.1.0")

@app.post("/generate-sql", response_model=GenerateResponse)
def generate_sql(payload: GenerateRequest):
    q = payload.query.strip()
    if not q:
        raise HTTPException(400, "Informe 'query'.")
    guardrails(q)

    table = P.detect_table(q)
    if not table:
        raise HTTPException(400, "Não reconheci a tabela. Tente citar 'estornos' ou 'tarifas estornadas'.")

    projection = P.pick_projection(q, table)
    filters = P.extract_filters(q, table)
    order = P.extract_order(q, table)
    limit = P.extract_limit(q, default=100, maxlim=1000)

    sql = build_select(table, projection, filters, order, limit)
    return GenerateResponse(sql=sql)