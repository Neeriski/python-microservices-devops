from app import app

def test_api_data():
    client = app.test_client()
    r = client.get("/api/data")
    data = r.get_json()
    assert r.status_code == 200
    assert "message" in data or "db_error" in data
