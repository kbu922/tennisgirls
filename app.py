import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Security & Upload Configuration
app.secret_key = os.environ.get('SECRET_KEY', '1234567')
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB limit

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# In-Memory Storage
users_db = {}
marketplace_listings = [
    {
        "id": 1,
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

item_id_counter = 2  # Counter for unique listing IDs


# -------------------------------------------------------------------
# AUTHENTICATION & DASHBOARD
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

        users_db[email] = {
            'name': name,
            'email': email,
            'password': password,
            'ntrp': ntrp,
            'photo': 'default-avatar.png',
            'phone': ''
        }
        
        session['user_email'] = email
        flash(f"Account created! Welcome, {name} 🎾", "success")
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


@app.route('/dashboard')
def dashboard():
    email = session.get('user_email')
    if not email or email not in users_db:
        flash("Please log in to access your dashboard.", "warning")
        return redirect(url_for('login'))

    user = users_db[email]
    my_racquets = [item for item in marketplace_listings if item.get('seller_email') == email]
    return render_template('dashboard.html', user=user, my_racquets=my_racquets)


@app.route('/update-profile', methods=['POST'])
def update_profile():
    email = session.get('user_email')
    if not email or email not in users_db:
        return redirect(url_for('login'))

    user = users_db[email]
    user['phone'] = request.form.get('phone', '')

    file = request.files.get('profile_photo')
    if file and file.filename != '':
        filename = f"user_{email.replace('@', '_')}_{secure_filename(file.filename)}"
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        user['photo'] = filename
        flash("Profile picture updated successfully!", "success")

    return redirect(url_for('dashboard'))


@app.route('/create-listing', methods=['POST'])
def create_listing():
    global item_id_counter
    email = session.get('user_email')
    if not email or email not in users_db:
        return redirect(url_for('login'))

    title = request.form.get('title')
    price = request.form.get('price')
    condition = request.form.get('condition')
    specs = request.form.get('specs')
    location = request.form.get('location')

    racquet_img = 'default-racquet.jpg'
    file = request.files.get('racquet_photo')
    if file and file.filename != '':
        filename = f"racquet_{secure_filename(file.filename)}"
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        racquet_img = filename

    if title and price:
        new_item = {
            'id': item_id_counter,
            'seller_email': email,
            'seller_name': users_db[email]['name'],
            'seller_phone': users_db[email].get('phone', 'Not provided'),
            'title': title,
            'price': price if price.startswith('$') else f"${price}",
            'condition': condition,
            'specs': specs,
            'location': location,
            'image': racquet_img
        }
        marketplace_listings.insert(0, new_item)
        item_id_counter += 1
        flash("Your racquet listing is now live in the marketplace!", "success")

    return redirect(url_for('dashboard'))

# -------------------------------------------------------------------
# SWING FEEDBACK ROUTE
# -------------------------------------------------------------------

@app.route('/swing-feedback', methods=['GET', 'POST'])
def swing_feedback():
    email = session.get('user_email')
    if not email:
        flash("Please log in to use AI Swing Feedback.", "warning")
        return redirect(url_for('login'))

    analysis_result = None

    if request.method == 'POST':
        racquet_brand = request.form.get('racquet_brand', 'Generic Racquet')
        shot_type = request.form.get('shot_type', 'Forehand')
        
        # Simulate motion tracking & biomechanics processing
        analysis_result = {
            "racket_speed_mph": 68,
            "kinetic_chain_score": 88,
            "hip_shoulder_separation": "34° (Optimal)",
            "impact_consistency": "Sweetspot 82%",
            "rec_tension_lbs": 48,
            "tension_range": "46 - 50 lbs",
            "string_type": "17G Co-Polyester / Synthetic Gut Hybrid",
            "diy_tips": [
                "String Mains with Co-Poly at 48 lbs for control and durability.",
                "String Crosses with Soft Synthetic Gut at 50 lbs (+2 lbs) to soften ball impact on off-center hits.",
                "Tie off mains using Parnell knot at grommets 6T and 6B for minimal tension loss."
            ]
        }
        flash("Swing analysis complete!", "success")

    return render_template('swing_feedback.html', result=analysis_result)
# -------------------------------------------------------------------
# MARKETPLACE & INDIVIDUAL LISTING ROUTES
# -------------------------------------------------------------------

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/marketplace')
def marketplace():
    """Marketplace Grid displaying all posted racquets"""
    return render_template('marketplace.html', listings=marketplace_listings)


@app.route('/listing/<int:item_id>')
def view_listing(item_id):
    """Dedicated Public Listing Page for a specific racquet"""
    # Search for item by ID
    item = next((item for item in marketplace_listings if item['id'] == item_id), None)
    if not item:
        flash("Listing not found or has been removed.", "warning")
        return redirect(url_for('marketplace'))

    return render_template('listing_detail.html', item=item)


@app.route('/healthz')
def healthz():
    return {"status": "healthy"}, 200


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
