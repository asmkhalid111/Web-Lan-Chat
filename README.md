# Web-LAN-Chat (SQA Edition) 🚀

Web-LAN-Chat is a modernized, browser-based chat application specifically designed for local area networks (LAN) like university labs. It functions completely offline (without internet) and features a beautiful Glassmorphism UI built with Tailwind CSS.

This project was built with a strong focus on **Software Quality Assurance (SQA)**, implementing isolated unit tests, integration tests, and automated UI tests using Selenium.

## 🛠️ Tech Stack
- **Backend:** Python, FastAPI, SQLAlchemy
- **Frontend:** HTML5, Vanilla JavaScript, Tailwind CSS
- **Database:** SQLite (Local, serverless storage)
- **Real-Time:** WebSockets
- **SQA Testing:** `pytest`, `pytest-asyncio`, `selenium`

## 🚀 How to Run the Application (From Scratch)

This application is designed to be extremely easy to set up on a brand new Windows PC. You do not need to manually configure environments or install packages.

### Step 1: Prerequisites
Ensure you have the following installed on your computer:
1. **Python (3.9 or higher):** Download from [python.org](https://www.python.org/downloads/). *(CRITICAL: During installation, make sure you check the box that says "Add Python.exe to PATH")*.
2. **Git (Optional):** Download from [git-scm.com](https://git-scm.com/downloads) if you want to clone the repository. Alternatively, you can just download the ZIP file from GitHub.

### Step 2: Download the Project
- **Option A (Git):** Open your terminal and run:
  `git clone https://github.com/asmkhalid111/Web-Lan-Chat.git`
- **Option B (ZIP):** Click the green "Code" button at the top right of this GitHub page and select "Download ZIP". Extract the folder to your computer.

### Step 3: Start the Server (One-Click Setup)
1. Open the `Web-Lan-Chat` folder you just downloaded.
2. Double-click the **`run_server.bat`** file.
   - *What this does:* This script automatically detects your Python installation, creates an isolated virtual environment (`venv`), installs all required libraries from `requirements.txt`, and boots up the FastAPI backend server.
   - *Note:* The very first time you run this, it might take a minute to download the packages. Subsequent runs will be instant!

### Step 4: Start Chatting!
1. **On your computer:** Open any web browser (Chrome, Edge, Firefox) and navigate to:
   👉 **`http://localhost:8000`**
2. **On your phone or another laptop in the same lab/Wi-Fi:** 
   - First, find your computer's local IP address by opening Command Prompt (`cmd`) and typing `ipconfig`. Look for the "IPv4 Address" under your Wi-Fi or Ethernet adapter (e.g., `192.168.0.106`).
   - On the phone's browser, navigate to that exact IP and port: 👉 **`http://192.168.0.106:8000`**
   - *(If the page doesn't load on your phone, you may need to allow port 8000 through your Windows Defender Firewall).*

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
