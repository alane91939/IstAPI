
import pytest
from API_Server  import app as flask_app

@pytest.fixture
def app():
    yield flask_app

@pytest.fixture
def requests(app):
    return app.test_client()

def test_points_added(requests):
    response = requests.post('http://127.0.0.1:5000/points_added',
    json = {"Brand":"DANNON","points":300,"timestamp":"10/31 10AM"})
    assert response.status_code == 200

    response = requests.post('http://127.0.0.1:5000/points_added',
    json = {"Brand":"UNILEVER","points":200,"timestamp":"10/31 11AM"})
    assert response.status_code == 200

    response = requests.post('http://127.0.0.1:5000/points_added',
    json = {"Brand":"DANNON","points":-200,"timestamp":"10/31 3PM"})
    assert response.status_code == 200

    response = requests.post('http://127.0.0.1:5000/points_added',
    json = {"Brand":"MILLER COORS","points":10000,"timestamp":"11/1 2PM"})
    assert response.status_code == 200

    response = requests.post('http://127.0.0.1:5000/points_added',
    json = {"Brand":"DANNON","points":1000,"timestamp":"11/2 2PM"})
    assert response.status_code == 200

def test_remove_points(requests):
    response = requests.delete('http://127.0.0.1:5000/remove_points',json={"points_lost":5000})
    print(response.data)
    assert response.status_code == 200

def test_balance(requests):
    response = requests.get('http://127.0.0.1:5000/balance')
    print(response.data)


    assert response.status_code == 200