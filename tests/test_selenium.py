import pytest
import threading
import time
import uvicorn
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from backend.database import engine
from backend.models import Base

# Setup and teardown the database for UI tests
@pytest.fixture(scope="module", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    # Be careful with dropping in a real scenario, but for isolation we clear it
    # We will just drop tables after selenium tests to keep it clean
    Base.metadata.drop_all(bind=engine)

class ServerThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        from backend.main import app
        self.config = uvicorn.Config(app, host="127.0.0.1", port=8001, log_level="error")
        self.server = uvicorn.Server(self.config)

    def run(self):
        self.server.run()

    def stop(self):
        self.server.should_exit = True

@pytest.fixture(scope="module")
def live_server():
    server = ServerThread()
    server.start()
    time.sleep(2) # Wait for server to start
    yield "http://127.0.0.1:8001"
    server.stop()
    server.join()

@pytest.fixture(scope="module")
def browser():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(5)
    yield driver
    driver.quit()

def test_registration_and_login_flow(live_server, browser):
    # 1. Go to the login page
    browser.get(live_server)
    assert "Web-LAN-Chat" in browser.title

    # 2. Toggle to registration
    toggle_btn = WebDriverWait(browser, 5).until(
        EC.element_to_be_clickable((By.ID, "toggle-auth"))
    )
    toggle_btn.click()
    
    # Wait for register form to be visible and interactable
    reg_student_id = WebDriverWait(browser, 5).until(
        EC.element_to_be_clickable((By.ID, "reg_student_id"))
    )
    time.sleep(0.5) # allow any layout shift to settle

    # 3. Fill registration form
    reg_student_id.send_keys("SELENIUM_USER")
    browser.find_element(By.ID, "reg_name").send_keys("Selenium Test")
    browser.find_element(By.ID, "reg_password").send_keys("testpassword")
    
    # 4. Submit Registration
    btn_register = WebDriverWait(browser, 5).until(
        EC.element_to_be_clickable((By.ID, "btn-register"))
    )
    btn_register.click()
    
    # Wait for success message
    success_div = WebDriverWait(browser, 5).until(
        EC.visibility_of_element_located((By.ID, "register-success"))
    )
    assert "Registration successful" in success_div.text

    # 5. Wait for auto-redirect to login (2 seconds timeout in JS)
    # The timeout switches the forms, making password visible again
    time.sleep(2.5) # Wait for the 2000ms JS timeout + 500ms buffer
    password_input = WebDriverWait(browser, 5).until(
        EC.element_to_be_clickable((By.ID, "password"))
    )
    
    # 6. Fill login form
    password_input.send_keys("testpassword")
    btn_login = WebDriverWait(browser, 5).until(
        EC.element_to_be_clickable((By.ID, "btn-login"))
    )
    btn_login.click()
    
    # 7. Check redirection to dashboard (which doesn't exist yet, but the URL will change)
    WebDriverWait(browser, 5).until(
        EC.url_contains("/static/dashboard.html")
    )
    assert "/static/dashboard.html" in browser.current_url
