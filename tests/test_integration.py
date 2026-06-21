def test_register_user(client):
    response = client.post("/api/register", json={
        "student_id": "024231",
        "name": "Test Student",
        "password": "testpassword"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["student_id"] == "024231"
    assert data["name"] == "Test Student"
    assert "id" in data

def test_register_existing_user(client):
    # Register first
    client.post("/api/register", json={
        "student_id": "123456",
        "name": "Test Student",
        "password": "testpassword"
    })
    
    # Try to register again
    response = client.post("/api/register", json={
        "student_id": "123456",
        "name": "Another Name",
        "password": "newpassword"
    })
    assert response.status_code == 400
    assert response.json()["detail"] == "Student ID already registered"

def test_login_user(client):
    # Register first
    client.post("/api/register", json={
        "student_id": "987654",
        "name": "Login Test",
        "password": "loginpassword"
    })
    
    # Login with correct credentials
    response = client.post("/api/login", json={
        "student_id": "987654",
        "password": "loginpassword"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Login successful"
    assert data["user"]["student_id"] == "987654"

def test_login_wrong_password(client):
    # Register first
    client.post("/api/register", json={
        "student_id": "111222",
        "name": "Wrong Pass Test",
        "password": "correctpassword"
    })
    
    # Login with incorrect credentials
    response = client.post("/api/login", json={
        "student_id": "111222",
        "password": "wrongpassword"
    })
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"

def test_login_nonexistent_user(client):
    response = client.post("/api/login", json={
        "student_id": "notfound",
        "password": "password"
    })
    assert response.status_code == 401
