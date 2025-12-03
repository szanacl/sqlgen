from pydantic import BaseModel

class GenerateRequest(BaseModel):
    query: str

class GenerateResponse(BaseModel):
    sql: str