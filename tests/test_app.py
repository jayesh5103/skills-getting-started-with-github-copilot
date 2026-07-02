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
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    encoded_path = "/activities/Chess%20Club/participants/michael%40mergington.edu"
    expected_message = "Unregistered michael@mergington.edu from Chess Club"

    # Act
    response = client.delete(encoded_path)

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == expected_message

    activities = client.get("/activities").json()
    assert email not in activities[activity_name]["participants"]
