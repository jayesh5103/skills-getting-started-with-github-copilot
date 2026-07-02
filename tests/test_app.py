import copy

import pytest
from fastapi.testclient import TestClient

import src.app as app_module


@pytest.fixture(autouse=True)
def reset_state():
    original = copy.deepcopy(app_module.activities)
    app_module.activities = copy.deepcopy(original)
    yield
    app_module.activities = copy.deepcopy(original)


client = TestClient(app_module.app)


def test_unregister_participant_removes_from_activity():
    response = client.delete(
        "/activities/Chess%20Club/participants/michael%40mergington.edu"
    )

    assert response.status_code == 200
    assert response.json()["message"] == (
        "Unregistered michael@mergington.edu from Chess Club"
    )

    activities = client.get("/activities").json()
    assert "michael@mergington.edu" not in activities["Chess Club"]["participants"]
