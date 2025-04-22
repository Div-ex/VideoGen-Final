# Video Generator App

A full-stack application that generates videos based on user prompts using a Flask backend and a React frontend. Users can register, log in, create AI-generated videos, and view or download their video history.

# Requirements

* Node.js: v22.14.0
* Python: v3.13.1
* pip (Python package manager)

# Installation & Running the App

## 1. Backend Setup (Flask API)

1.  Open a terminal and navigate to the project root directory.

2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3.  Start the Flask server:
    ```bash
    python server2.py
    ```
    This will run the backend on: http://localhost:5000

## 2. Frontend Setup (React App)

1.  In a new terminal, navigate to the `frontend2` directory:
    ```bash
    cd frontend2
    ```

2.  Install the React dependencies:
    ```bash
    npm install
    ```

3.  Start the React development server:
    ```bash
    npm start
    ```
    This will run the frontend on: http://localhost:3000

## Note:
All generated videos are stored in the videos/ folder on the backend.