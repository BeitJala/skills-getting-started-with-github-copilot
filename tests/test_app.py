from urllib.parse import quote

import pytest
from fastapi.testclient import TestClient

from src import app as app_module


@pytest.fixture(autouse=True)
def reset_activity_state():
    app_module.activities["Chess Club"]["participants"] = [
        "michael@mergington.edu",
        "daniel@mergington.edu",
    ]
    yield


client = TestClient(app_module.app)


def test_unregister_participant_removes_email_from_activity():
    email = "michael@mergington.edu"
    response = client.delete(
        f"/activities/Chess Club/participants/{quote(email, safe='')}"
    )

    assert response.status_code == 200
    assert email not in app_module.activities["Chess Club"]["participants"]
    assert "daniel@mergington.edu" in app_module.activities["Chess Club"]["participants"]
