from api.api_client import APIClient

def test_get():
    client = APIClient("https://try.satorixr.com")
    response = client.get("/manifest.json")
    assert response.status_code == 200