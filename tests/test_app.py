from fastapi.testclient import TestClient
from sqlgen.app import app

client = TestClient(app)

def test_generate_ok():
    payload = {"query": "Quero agência e valor dos estornos de agosto acima de 50, ordenar por data desc, máximo 200."}
    r = client.post("/generate-sql", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert "SELECT" in data["sql"] and "FROM tarifas_estornadas" in data["sql"]

def test_forbidden():
    payload = {"query": "mostrar estornos; drop table usuarios"}
    r = client.post("/generate-sql", json=payload)
    assert r.status_code == 400