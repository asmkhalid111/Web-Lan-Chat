from fastapi.testclient import TestClient
from backend.main import app
import pytest

client = TestClient(app)

def test_create_and_get_note():
    # 1. Register a user
    student_id = "NOTE_USER"
    client.post("/api/register", json={
        "student_id": student_id,
        "name": "Note Tester",
        "password": "pass"
    })
    
    # 2. Create Note
    response = client.post(f"/api/notes/{student_id}", json={
        "title": "My First Note",
        "content": "This is a private note"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "My First Note"
    assert "id" in data
    
    # 3. Get Notes
    response = client.get(f"/api/notes/{student_id}")
    assert response.status_code == 200
    notes = response.json()
    assert len(notes) >= 1
    assert notes[-1]["title"] == "My First Note"

def test_create_and_get_announcement():
    # 1. Create Announcement
    response = client.post("/api/announcements?author=Admin", json={
        "title": "Lab Closure",
        "content": "The lab will close at 8PM today."
    })
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Lab Closure"
    assert data["author"] == "Admin"
    
    # 2. Get Announcements
    response = client.get("/api/announcements")
    assert response.status_code == 200
    anns = response.json()
    assert len(anns) >= 1
    assert anns[0]["title"] == "Lab Closure" # Order is descending so it should be first
