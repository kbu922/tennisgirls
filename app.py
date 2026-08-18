import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'super-secret-tennis-key'  # Replace with a secure random key
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50 MB limit

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# 1. Home / Landing Page
@app.route('/')
def home():
    return render_template('index.html')

# 2. Page 1: String Tension Analysis & DIY Advice
@app.route('/string-advisor', methods=['GET', 'POST'])
def string_advisor():
    advice = None
    if request.method == 'POST':
        player_style = request.form.get('style')
        arm_pain = request.form.get('arm_pain')
        
        # Tension calculation logic
        if arm_pain == 'yes':
            advice = "Recommended Tension: 48-50 lbs (Multifilament string for arm comfort)."
        elif player_style == 'power':
            advice = "Recommended Tension: 53-56 lbs (Polyester string for maximum control)."
        else:
            advice = "Recommended Tension: 50-52 lbs (Synthetic Gut / Hybrid setup)."
            
    return render_template('string_advisor.html', advice=advice)

# 3. Page 2: Second-Hand Racquet Marketplace
@app.route('/marketplace')
def marketplace():
    listings = [
        {"id": 1, "title": "Babolat Pure Drive 2021", "price": "$120", "condition": "8/10", "location": "Seoul"},
        {"id": 2, "title": "Wilson Pro Staff 97 v13", "price": "$150", "condition": "9/10", "location": "Busan"},
    ]
    return render_template('marketplace.html', listings=listings)

# 4. Page 3: Technique Video Upload & Community Feedback
@app.route('/gesture-community', methods=['GET', 'POST'])
def gesture_community():
    if request.method == 'POST':
        if 'video' not in request.files:
            flash('No file uploaded')
            return redirect(request.url)
        file = request.files['video']
        if file.filename != '':
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('Video uploaded! Community members can now critique your swing.')
    return render_template('gesture_community.html')

# 5. Page 4: Court Dating ($1 Paywall Protected)
@app.route('/dating')
def dating():
    # Check if user has completed the $1 payment session
    is_paid = session.get('has_paid_dating', False)
    return render_template('dating_paywall.html', is_paid=is_paid)

@app.route('/process-payment', methods=['POST'])
def process_payment():
    # Simulate $1 Stripe / PayPal payment process
    session['has_paid_dating'] = True
    flash('Payment of $1.00 USD successful! Welcome to Court Dating.')
    return redirect(url_for('dating'))

if __name__ == '__main__':
    app.run(debug=True)
