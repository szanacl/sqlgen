# sqlgen-py — Gerador de SQL por linguagem natural (MVP)

MVP em **Python + FastAPI** para converter linguagem natural em **SQL segura** usando catálogo de esquema (whitelist) + regras.

## Rodar local

```bash
python -m venv .venv
source venv/bin/activate
pip install -r requirements.txt

uvicorn sqlgen.app:app --reload
```

Acesse: http://127.0.0.1:8000/docs

## Exemplo de uso

```bash
curl -X POST http://127.0.0.1:8000/generate-sql   -H "Content-Type: application/json"   -d '{"query":"Quero agência e valor dos estornos de agosto acima de 50, ordenar por data desc, máximo 200."}'
```

Resposta:
```json
{
  "sql": "SELECT agencia, valor, data_estorno\nFROM tarifas_estornadas\nWHERE valor > 50 AND data_estorno >= DATE '2025-08-01' AND data_estorno < DATE '2025-09-01'\nORDER BY data_estorno DESC\nFETCH FIRST 200 ROWS ONLY;"
}
```

## Estrutura

```
sqlgen-py/
  ├─ sqlgen/
  │   ├─ app.py         # FastAPI e endpoint /generate-sql
  │   ├─ models.py      # Pydantic models
  │   ├─ guardrails.py  # Regras de segurança
  │   ├─ parser.py      # Regras simples (regex + dicionários)
  │   ├─ sqlbuilder.py  # Montagem da SQL segura
  │   └─ schema.json    # Catálogo de tabelas/colunas/sinônimos
  ├─ tests/
  │   └─ test_app.py
  ├─ requirements.txt
  └─ README.md
```

## Notas de segurança
- Apenas `SELECT`.
- Colunas e tabelas restritas ao `schema.json`.
- Limite padrão (100) e teto (1000).
- Bloqueio de padrões perigosos (e.g., `;`, `--`, DML).