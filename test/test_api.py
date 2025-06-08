import pytest
import requests

base_url = 'http://127.0.0.1:5000/events/'
HEADERS = {
    "content-type": "application/json",
    "TransactionId": "transaction1",
    "ISOCountry": "INDIA"
}

event_payload = {
    "payload": {
        "name": "Arjit Singh",
        "location": "Pune",
        "start_time": "2025-06-20 15:30",
        "end_time": "2025-06-20 18:30",
        "max_capacity": 1
    }
}

attendee_payload = {
    "payload": {
        "name": "Rohit Sandanshiv",
        "email": "rssandanshiv782000@gmail.com"
    }
}
attendee_payload2 = {
    "payload": {
        "name": "Mohit Sandanshiv",
        "email": "rss@gmail.com"
    }
}


@pytest.fixture(scope="module")
def event_id():
    response = requests.post(base_url, json=event_payload, headers=HEADERS)
    assert response.status_code == 201
    eid = response.json().get('event')
    return eid


def test_insert_event():
    assert event_id is not None


def test_get_event():
    response = requests.get(base_url, headers=HEADERS)
    assert response.status_code == 200
    assert "sections" in response.json()


def test_insert_attendee(event_id):
    url = f"{base_url}{event_id}/register"
    response = requests.post(url, json=attendee_payload, headers=HEADERS)
    assert response.status_code == 201
    assert "Registration Successful" in response.json()['message']


def test_get_attendee(event_id):
    url = f"{base_url}{event_id}/attendee"
    response = requests.get(url, headers=HEADERS)
    assert response.status_code == 200
    assert "sections" in response.json()


def test_insert_duplicate_attendee(event_id):
    url = f"{base_url}{event_id}/register"
    response = requests.post(url, json=attendee_payload, headers=HEADERS)
    assert "only 1 registration per user" in response.json()['message']


def test_event_full(event_id):
    url = f"{base_url}{event_id}/register"
    response = requests.post(url, json=attendee_payload2, headers=HEADERS)
    assert "Seats full! Come again for next show" in response.json()['message']

