import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Security & Upload Configuration
app.secret_key = os.environ.get('SECRET_KEY', '1234567')
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB file upload limit

# Ensure static/uploads folder exists locally and on server
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# -------------------------------------------------------------------
# IN-MEMORY DATA STORES (Simulated Databases)
# -------------------------------------------------------------------
users_db = {}  # Format: { 'email': {'name': '...', 'password': '...', 'ntrp': '...', 'photo': '...', 'phone': '...'} }

marketplace_listings = [
    {
        "seller_email": "demo@tennisgirls.com",
        "seller_name": "Pro Staff Demo",
        "title": "Babolat Pure Aero 2023",
        "price": "$140",
        "condition": "Like New (9/10)",
        "specs": "Grip 2 (4 1/4), 300g",
        "location": "Seoul (Olympic Park)",
        "image": "default-racquet.jpg"
    }
]

user_vip_status = {"is_paid": False}


# -------------------------------------------------------------------
# AUTHENTICATION ROUTES (Register / Login / Logout)
# -------------------------------------------------------------------

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        ntrp = request.form.get('ntrp')

        if email in users_db:
            flash("Email is already registered! Please log in.", "warning")
            return redirect(url_for('login'))

        # Create new user profile record
        users_db[email] = {
            'name': name,
            'email': email,
            'password': password,
            'ntrp': ntrp,
            'photo': 'default-avatar.png',
            'phone': ''
        }
        
        # Log user in automatically after registration
        session['user_email'] = email
        flash(f"Account created! Welcome to TennisGirls, {name} 🎾", "success")
        return redirect(url_for('dashboard'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = users_db.get(email)

        if user and user['password'] == password:
            session['user_email'] = email
            flash(f"Welcome back, {user['name']}!", "success")
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid email address or password.", "danger")

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user_email', None)
    flash("You have been logged out.", "info")
    return redirect(url_for('home'))


# -------------------------------------------------------------------
# USER DASHBOARD & PROFILE MANAGEMENT
# -------------------------------------------------------------------

@app.route('/dashboard')
def dashboard():
    email = session.get('user_email')
    if not email or email not in users_db:
        flash("Please log in to access your seller dashboard.", "warning")
        return redirect(url_for('login'))

    user = users_db[email]
    # Filter marketplace items posted by this logged-in seller
    my_racquets = [item for item in marketplace_listings if item.get('seller_email') == email]
    
    return render_template('dashboard.html', user=user, my_racquets=my_racquets)


@app.route('/update-profile', methods=['POST'])
def update_profile():
    email = session.get('user_email')
    if not email or email not in users_db:
        return redirect(url_for('login'))

    user = users_db[email]
    user['phone'] = request.form.get('phone', '')

    # Profile photo upload handling
    file = request.files.get('profile_photo')
    if file and file.filename != '':
        filename = f"user_{email.replace('@', '_')}_{secure_filename(file.filename)}"
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        user['photo'] = filename
        flash("Profile picture updated successfully!", "success")

    return redirect(url_for('dashboard'))


@app.route('/create-listing', methods=['POST'])
def create_listing():
    email = session.get('user_email')
    if not email or email not in users_db:
        return redirect(url_for('login'))

    title = request.form.get('title')
    price = request.form.get('price')
    condition = request.form.get('condition')
    specs = request.form.get('specs')
    location = request.form.get('location')

    # Racquet image upload handling
    racquet_img = 'default-racquet.jpg'
    file = request.files.get('racquet_photo')
    if file and file.filename != '':
        filename = f"racquet_{secure_filename(file.filename)}"
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        racquet_img = filename

    if title and price:
        marketplace_listings.insert(0, {
            'seller_email': email,
            'seller_name': users_db[email]['name'],
            'title': title,
            'price': price if price.startswith('$') else f"${price}",
            'condition': condition,
            'specs': specs,
            'location': location,
            'image': racquet_img
        })
        flash("Your racquet listing is now published in the marketplace!", "success")

    return redirect(url_for('dashboard'))


# -------------------------------------------------------------------
# PUBLIC FEATURE ROUTES
# -------------------------------------------------------------------

@app.route('/')
def home():
    """Homepage"""
    return render_template('index.html')


@app.route('/string-advisor', methods=['GET', 'POST'])
def string_advisor():
    """Racquet String & Tension Calculator"""
    advice = None
    if request.method == 'POST':
        style = request.form.get('style')
        arm_pain = request.form.get('arm_pain')
        string_type = request.form.get('string_type')

        base_tension = 53
        if style == 'control':
            base_tension += 3
        elif style == 'power':
            base_tension -= 2

        if arm_pain == 'yes':
            base_tension -= 4

        if string_type == 'poly':
            base_tension -= 3
        elif string_type == 'multi':
            base_tension += 2

        tension_kg = round(base_tension * 0.453592, 1)
        string_rec = 'Soft Multifilament / Nylon' if arm_pain == 'yes' else string_type.title()
        advice = f"{base_tension} lbs ({tension_kg} kg) using {string_rec} strings."

    return render_template('string_advisor.html', advice=advice)


@app.route('/marketplace')
def marketplace():
    """Public Marketplace View"""
    return render_template('marketplace.html', listings=marketplace_listings)


@app.route('/gesture-community', methods=['GET', 'POST'])
def gesture_community():
    """Swing Feedback Community Uploads"""
    if request.method == 'POST':
        shot_type = request.form.get('shot_type')
        file = request.files.get('video')

        if file and file.filename != '':
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash(f"Video uploaded successfully for {shot_type}!", "success")
        else:
            flash("Please attach a valid video file.", "warning")

        return redirect(url_for('gesture_community'))

    return render_template('gesture_community.html')


@app.route('/dating')
def dating():
    """Court Matching Feature"""
    return render_template('dating_paywall.html', is_paid=user_vip_status["is_paid"])


@app.route('/process-payment', methods=['POST'])
def process_payment():
    """Simulated VIP Payment Processing"""
    user_vip_status["is_paid"] = True
    flash("Payment successful! Access granted.", "success")
    return redirect(url_for('dating'))


@app.route('/healthz')
def healthz():
    """Render Web Service Health Monitoring Check"""
    return {"status": "healthy", "service": "tennisgirls"}, 200


# -------------------------------------------------------------------
# SERVER LAUNCH
# -------------------------------------------------------------------
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
