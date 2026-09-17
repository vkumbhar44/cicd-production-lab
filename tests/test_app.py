from app.main import app


def test_home():
    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200
    assert response.json["message"] == "CI/CD Production Lab"


def test_health():
    client = app.test_client()

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json["status"] == "healthy"

def test_info():
    client = app.test_client()

    response = client.get("/info")

    assert response.status_code == 200
    assert response.json["service"] == "cicd-production-lab"
    assert response.json["version"] == "1.0.0"



def test_version():
    client = app.test_client()

    response = client.get("/version")

    assert response.status_code == 200
    assert response.json["version"] == "1.0.0"