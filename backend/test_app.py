from app import app

def test_api_data():
    client = app.test_client()
    r = client.get("/api/data")
    assert r.status_code == 200
    assert "message" in r.get_json()
