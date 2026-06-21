# Web-LAN-Chat (SQA Edition) 🚀

Web-LAN-Chat is a modernized, browser-based chat application specifically designed for local area networks (LAN) like university labs. It functions completely offline (without internet) and features a beautiful Glassmorphism UI built with Tailwind CSS.

This project was built with a strong focus on **Software Quality Assurance (SQA)**, implementing isolated unit tests, integration tests, and automated UI tests using Selenium.

## 🛠️ Tech Stack
- **Backend:** Python, FastAPI, SQLAlchemy
- **Frontend:** HTML5, Vanilla JavaScript, Tailwind CSS
- **Database:** SQLite (Local, serverless storage)
- **Real-Time:** WebSockets
- **SQA Testing:** `pytest`, `pytest-asyncio`, `selenium`

## 🚀 How to Run the Application

This application is designed to be easily runnable on Windows.

1. **Start the Server:**
   Simply double-click the `run_server.bat` file in the project folder. This will automatically install any missing dependencies and start the FastAPI server.
   
2. **Access the Chat:**
   Open your browser and navigate to `http://localhost:8000`. 
   *(To access it from your phone on the same Wi-Fi, find your computer's IP address by running `ipconfig` in cmd, and go to `http://<YOUR_IP>:8000`)*

## 🧪 How to Run SQA Tests

The project is heavily tested. Tests are run against a temporary, in-memory SQLite database (`sqlite:///:memory:`) so your real chat data is never affected.

1. **Run the Test Suite:**
   Double-click the `run_tests.bat` file.
   
This will execute:
- **Unit Tests:** Validates backend security functions like password hashing (`bcrypt`).
- **Integration Tests:** Validates FastAPI API endpoints for registration and login.
- **Automated UI Tests:** Launches a headless Chrome browser via Selenium, clicks the register button, fills out the form, submits, waits for the redirect, and successfully logs in.

## ✨ Features
- **Global Chat Room:** Real-time messaging using WebSockets.
- **Secure Authentication:** `bcrypt` password hashing and secure token management.
- **Glassmorphism UI:** Stunning dynamic animations and gradients.
- **Persistent History:** Automatically loads recent chat history upon joining.
