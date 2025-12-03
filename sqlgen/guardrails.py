from fastapi import HTTPException

FORBIDDEN = [
    ";", "--", "/*", "*/",
    " drop ", " delete ", " update ", " insert ",
    " alter ", " grant ", " revoke ", " truncate ",
    " create ", " execute ", " call ", " merge ", " union "
]

def guardrails(user_text: str):
    low = user_text.lower()
    for bad in FORBIDDEN:
        if bad in low:
            raise HTTPException(400, f"Entrada contém padrão proibido: {bad.strip()}")