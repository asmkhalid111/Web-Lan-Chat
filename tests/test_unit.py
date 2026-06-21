from backend.auth import get_password_hash, verify_password

def test_password_hashing():
    password = "supersecretpassword"
    hashed = get_password_hash(password)
    
    assert password != hashed
    assert verify_password(password, hashed) is True
    assert verify_password("wrongpassword", hashed) is False
