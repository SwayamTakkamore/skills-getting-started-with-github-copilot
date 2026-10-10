def test_get_activities_returns_activity_data(client):
    response = client.get("/activities")

    assert response.status_code == 200
    activities = response.json()
    assert "Chess Club" in activities
    assert "participants" in activities["Chess Club"]


def test_signup_adds_participant(client):
    email = "new.student@mergington.edu"

    response = client.post("/activities/Soccer Club/signup", params={"email": email})

    assert response.status_code == 200
    assert response.json() == {
        "message": f"Signed up {email} for Soccer Club"
    }
    assert email in client.get("/activities").json()["Soccer Club"]["participants"]


def test_duplicate_signup_is_rejected(client):
    email = "new.student@mergington.edu"
    client.post("/activities/Soccer Club/signup", params={"email": email})

    response = client.post("/activities/Soccer Club/signup", params={"email": email})

    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"
    participants = client.get("/activities").json()["Soccer Club"]["participants"]
    assert participants.count(email) == 1


def test_signup_for_unknown_activity_returns_not_found(client):
    response = client.post(
        "/activities/Unknown Club/signup",
        params={"email": "new.student@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_delete_removes_participant(client):
    email = "new.student@mergington.edu"
    client.post("/activities/Soccer Club/signup", params={"email": email})

    response = client.delete(f"/activities/Soccer Club/participants/{email}")

    assert response.status_code == 200
    assert response.json() == {
        "message": f"Removed {email} from Soccer Club"
    }
    assert email not in client.get("/activities").json()["Soccer Club"]["participants"]


def test_delete_missing_participant_returns_not_found(client):
    response = client.delete(
        "/activities/Soccer Club/participants/missing.student@mergington.edu"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"


def test_delete_from_unknown_activity_returns_not_found(client):
    response = client.delete(
        "/activities/Unknown Club/participants/student@mergington.edu"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
