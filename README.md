# 🚀 Python Live Chat App

A modern, real-time chat application built with Flask and WebSockets. This app allows users to create or join chat rooms with instant messaging, live user tracking, and a mobile-responsive UI.

## ✨ Features

- **Real-time Messaging**: Instant communication using Flask-SocketIO.
- **Room System**: Create unique 4-letter room codes or join existing ones.
- **Live User Sidebar**: See who is currently online in the room.
- **Modern UI**: Styled with Tailwind CSS for a sleek look.
- **Mobile Responsive**: Optimized for all devices, including mobile viewports.
- **Smart Notifications**: System alerts when users enter or leave the room.

## 🛠️ Tech Stack

- **Backend**: Python, Flask
- **Real-time**: Flask-SocketIO (with Eventlet worker)
- **Frontend**: HTML5, Tailwind CSS, JavaScript
- **Deployment**: Heroku

## 🚀 Quick Start

### 1. Clone and Install
```bash
git clone https://github.com/Mkaify/Python_Live_Chat_App.git
cd Python_Live_Chat_App
pip install -r requirements.txt
```

### 2. Environment Setup
Create a .env file in the root directory:

```bash
SECRET_KEY=your_random_secret_key
```

### 3. Run Locally
```bash
python main.py
Visit http://127.0.0.1:5000 in your browser.
```
### 4. ☁️ Deployment (Heroku)
This app is configured to run on Heroku using the eventlet worker for WebSocket support.

#### Set Python Version: 
Ensure .python-version is set to 3.11.

#### Set Config Vars:

```bash
heroku config:set SECRET_KEY=your_secret_key
```
#### Deploy:
```bash
git push heroku main
```

### 📝 License
- MIT License. Feel free to use and modify!