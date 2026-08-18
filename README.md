# 🎾 tennisgirls

[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/framework-Flask-green.svg)](https://flask.palletsprojects.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Welcome to **tennisgirls** — an all-in-one web application built with Python & Flask designed for single tennis enthusiasts to meet on the court, get feedback on their swing, calculate string tension, and trade gear.

---

## ✨ Core Features

1. **❤️ Court Dating ($1 VIP Access)**
   - Connect with verified single tennis players nearby for 1:1 court dates and 2:2 mixed doubles matches.
   - Protected by a $1.00 USD verification paywall to maintain high-quality, high-intent profiles.

2. **📹 Swing Analysis & Community Feedback**
   - Upload video clips of your serve, forehand, or backhand (.mp4, .mov).
   - Get posture, timing, and footwork critiques from community members and coaches.

3. **⚙️ DIY Racquet String & Tension Advisor**
   - Receive custom string setup recommendations (tension in lbs/kg & string material) based on your playstyle and arm health (e.g., Tennis Elbow protection).

4. **🛍️ Second-Hand Racquet Marketplace**
   - Buy and sell pre-owned tennis racquets and accessories with local players in your city.

---

## 🛠️ Tech Stack

- **Backend:** Python 3.9+, Flask
- **Frontend:** HTML5, CSS3, Bootstrap 5
- **File Processing:** Werkzeug (Secure Uploads)
- **Deployment:** Render / Gunicorn

---

## 📂 Project Directory Structure

```text
tennisgirls/
├── app.py                  # Main Flask backend routes & logic
├── requirements.txt        # Python dependencies
├── Procfile                # Deployment configuration for Render
├── README.md               # Project documentation
├── static/
│   └── uploads/            # Temporary storage for swing videos
└── templates/
    ├── base.html           # Main navigation layout
    ├── index.html          # Landing homepage
    ├── string_advisor.html # Tension calculator & DIY tips
    ├── marketplace.html    # Second-hand gear marketplace
    ├── gesture_community.html # Video upload & swing feedback
    └── dating_paywall.html # Protected court dating page
