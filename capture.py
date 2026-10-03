import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

def capture_screenshots():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1280,800")
    
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(5)
    
    try:
        # 1. Login Page
        driver.get("http://localhost:8000")
        time.sleep(2)
        driver.save_screenshot("screenshot_login.png")
        
        # 2. Register
        toggle_btn = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "toggle-auth")))
        toggle_btn.click()
        
        reg_student_id = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "reg_student_id")))
        time.sleep(0.5)
        reg_student_id.send_keys("USER_01")
        driver.find_element(By.ID, "reg_name").send_keys("Test User")
        driver.find_element(By.ID, "reg_password").send_keys("password123")
        
        btn_register = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "btn-register")))
        btn_register.click()
        time.sleep(3) # Wait for redirect
        
        # 3. Login
        password_input = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "password")))
        password_input.send_keys("password123")
        btn_login = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "btn-login")))
        btn_login.click()
        
        # Wait for dashboard
        WebDriverWait(driver, 5).until(EC.url_contains("/static/dashboard.html"))
        time.sleep(2)
        
        # Send a message
        msg_input = driver.find_element(By.ID, "chat-input")
        if msg_input:
            msg_input.send_keys("Hello everyone! This UI looks amazing! 🚀" + Keys.RETURN)
            time.sleep(2)
                
        driver.save_screenshot("screenshot_chat.png")
        print("Screenshots captured successfully.")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    capture_screenshots()
