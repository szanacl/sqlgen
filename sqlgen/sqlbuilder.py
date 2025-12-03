from typing import List, Tuple, Any

def build_select(table: str,
                 projection: List[str],
                 filters: List[Tuple[str, str, Any]],
                 order: tuple[str|None, str|None],
                 limit: int) -> str:
    cols_sql = ", ".join(projection)
    where_parts = []
    for col, op, val in filters:
        if isinstance(val, (int, float)):
            where_parts.append(f"{col} {op} {val}")
        elif isinstance(val, str) and val.startswith("DATE "):
            where_parts.append(f"{col} {op} {val}")
        else:
            sval = str(val).replace("'", "''")
            where_parts.append(f"{col} {op} '{sval}'")
    where_sql = f"WHERE {' AND '.join(where_parts)}" if where_parts else ""

    order_col, order_dir = order
    order_sql = f"ORDER BY {order_col} {order_dir}" if order_col else ""

    # Compatível com DB2/Oracle modernos (ajuste se necessário para seu ambiente)
    limit_sql = f"FETCH FIRST {limit} ROWS ONLY"

    sql = f"""SELECT {cols_sql}
FROM {table}
{where_sql}
{order_sql}
{limit_sql};"""
    # Normaliza espaços múltiplos
    return "\n".join([line.rstrip() for line in sql.splitlines() if line.strip()])