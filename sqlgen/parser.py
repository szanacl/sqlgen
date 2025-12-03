import re
import json
from datetime import date
from typing import Tuple, List, Dict, Any

# Carrega o catálogo (whitelist)
with open(__file__.replace("parser.py", "schema.json"), "r", encoding="utf-8") as f:
    SCHEMA: Dict[str, Any] = json.load(f)

MONTHS = {
    "janeiro":1,"fevereiro":2,"marco":3,"março":3,"abril":4,"maio":5,"junho":6,
    "julho":7,"agosto":8,"setembro":9,"outubro":10,"novembro":11,"dezembro":12
}

def detect_table(q: str):
    ql = q.lower()
    for t, meta in SCHEMA.items():
        keys = [t] + meta.get("synonyms", [])
        if any(k in ql for k in keys):
            return t
    return None

def extract_limit(q: str, default=100, maxlim=1000):
    m = re.search(r"(?:limite|max(?:imo)?|top|máximo)\s*(\d{1,4})", q.lower())
    if not m:
        return default
    n = int(m.group(1))
    return min(n, maxlim)

def extract_order(q: str, table: str):
    cols = list(SCHEMA[table]["columns"].keys())
    m = re.search(r"ordenar por ([a-zA-Z_]+)\s*(asc|desc)?", q.lower())
    if m and m.group(1) in cols:
        return m.group(1), (m.group(2) or "asc").upper()
    # heurística comum
    for cand in ["data_estorno", "data", "id", "valor"]:
        if cand in cols:
            return cand, "DESC"
    return None, None

def month_to_range(q: str) -> Tuple[date, date] | Tuple[None, None]:
    ql = q.lower()
    for name, idx in MONTHS.items():
        if name in ql:
            import re as _re
            year = date.today().year
            myear = _re.search(rf"{name}\s*(\d{{4}})", ql)
            if myear:
                year = int(myear.group(1))
            if idx == 12:
                start = date(year, 12, 1)
                end = date(year+1, 1, 1)
            else:
                start = date(year, idx, 1)
                end = date(year, idx+1, 1)
            return start, end
    return None, None

def extract_filters(q: str, table: str):
    cols = SCHEMA[table]["columns"]
    filters = []
    ql = q.lower()

    # valor > N
    m = re.search(r"(?:maior que|acima de|>\s*)\s*(\d+[.,]?\d*)", ql)
    if m and "valor" in cols:
        val = m.group(1).replace(",", ".")
        filters.append(("valor", ">", float(val)))

    # valor < N
    m = re.search(r"(?:menor que|abaixo de|<\s*)\s*(\d+[.,]?\d*)", ql)
    if m and "valor" in cols:
        val = m.group(1).replace(",", ".")
        filters.append(("valor", "<", float(val)))

    # mês por extenso
    s, e = month_to_range(q)
    if s and e and "data_estorno" in cols:
        filters.append(("data_estorno", ">=", f"DATE '{s.isoformat()}'"))
        filters.append(("data_estorno", "<",  f"DATE '{e.isoformat()}'"))

    return filters

def pick_projection(q: str, table: str):
    cols = list(SCHEMA[table]["columns"].keys())
    asked = []
    for c in cols:
        if re.search(rf"\b{c}\b", q.lower()):
            asked.append(c)
    if not asked:
        asked = ["*"]
    else:
        if "data_estorno" in cols and "data_estorno" not in asked:
            # se houve filtro de data, é útil mostrar a coluna
            asked.append("data_estorno")
    return asked