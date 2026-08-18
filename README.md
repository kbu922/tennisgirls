# 🎾 tennisgirls

[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/framework-Flask-green.svg)](https://flask.palletsprojects.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Welcome to **tennisgirls** — an all-in-one platform designed for single tennis enthusiasts to meet on the court, get feedback on their swing, calculate string tension, and trade gear.

---

## ✨ Key Features

1. **❤️ Court Dating ($1 VIP Access)**
   - Find single tennis players nearby for 1:1 court dates and 2:2 mixed doubles matches.
   - Gated with a $1.00 USD paywall to ensure high-intent, verified profiles.

2. **📹 Swing Analysis & Gesture Feedback**
   - Upload video clips of your serve, forehand, or backhand.
   - Receive technique critiques and advice on posture/timing from the community.

3. **🎾 DIY Racquet String & Tension Advisor**
   - Get personalized string setup recommendations (tension in lbs / string material) based on playstyle and arm health (e.g., tennis elbow).

4. **🛍️ Second-Hand Racquet Marketplace**
   - Buy and sell used tennis racquets, stringing machines, and accessories directly with other players.

---

## 🛠️ Tech Stack

- **Backend:** Python 3.9+, Flask
- **Frontend:** HTML5, CSS3, Bootstrap 5
- **File Processing:** Werkzeug (Secure Uploads)
- **Deployment:** Render / Gunicorn

---

## 📂 Project Structure

```text
tennisgirls/
├── app.py                  # Main Flask application entry point
├── requirements.txt        # Python dependencies
├── Procfile                # Render deployment configuration
├── README.md               # Project documentation
├── static/
│   ├── css/
│   │   └── style.css       # Custom styles
│   └── uploads/            # Temporary directory for video uploads
└── templates/
    ├── base.html           # Main navigation and base layout
    ├── index.html          # Landing page
    ├── string_advisor.html # String tension calculator
    ├── marketplace.html    # Second-hand gear market
    ├── gesture_community.html # Video upload & swing feedback
    └── dating_paywall.html # Protected court dating page
