import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Security & Environment Configurations
app.secret_key = os.environ.get('SECRET_KEY', '1234567')
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB upload limit

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# In-Memory Databases (Simulated storage for demo)
users_db = {}  # Format: { 'email': {'name': 'Name', 'password': 'password', 'ntrp': '3.5'} }

marketplace_listings = [
    {
        "title": "Babolat Pure Aero 2023",
        "price": "$140",
        "condition": "Like New (9/10)",
        "specs": "Grip 2 (4 1/4), 300g",
        "location": "Seoul (Olympic Park)"
    }
]

user_vip_status = {"is_paid": False}


# -------------------------------------------------------------------
# AUTHENTICATION ROUTES (REGISTER / LOGIN / LOGOUT)
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

        # Save user to dictionary
        users_db[email] = {
            'name': name,
            'password': password,
            'ntrp': ntrp
        }
        
        # Log user in automatically after registration
        session['user'] = {'name': name, 'email': email, 'ntrp': ntrp}
        flash(f"Account created successfully! Welcome, {name} 🎾", "success")
        return redirect(url_for('home'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = users_db.get(email)

        if user and user['password'] == password:
            session['user'] = {'name': user['name'], 'email': email, 'ntrp': user['ntrp']}
            flash(f"Welcome back, {user['name']}!", "success")
            return redirect(url_for('home'))
        else:
            flash("Invalid email or password. Please try again.", "danger")

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user', None)
    flash("You have been logged out.", "info")
    return redirect(url_for('home'))


# -------------------------------------------------------------------
# APP ROUTES
# -------------------------------------------------------------------

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/string-advisor', methods=['GET', 'POST'])
def string_advisor():
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
        advice = f"{base_tension} lbs ({tension_kg} kg) using " \
                 f"{'Soft Multifilament / Nylon' if arm_pain == 'yes' else string_type.title() + ' strings'}."

    return render_template('string_advisor.html', advice=advice)


@app.route('/marketplace', methods=['GET', 'POST'])
def marketplace():
    if request.method == 'POST':
        title = request.form.get('title')
        price = request.form.get('price')
        condition = request.form.get('condition')
        specs = request.form.get('specs')
        location = request.form.get('location')

        if title and price and location:
            marketplace_listings.insert(0, {
                "title": title,
                "price": price if price.startswith('$') else f"${price}",
                "condition": condition,
                "specs": specs,
                "location": location
            })
            flash("Racquet listing successfully posted!", "success")
            return redirect(url_for('marketplace'))

    return render_template('marketplace.html', listings=marketplace_listings)


@app.route('/gesture-community', methods=['GET', 'POST'])
def gesture_community():
    if request.method == 'POST':
        shot_type = request.form.get('shot_type')
        caption = request.form.get('caption')
        file = request.files.get('video')

        if file and file.filename != '':
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            flash(f"Video for {shot_type} uploaded successfully!", "success")
        else:
            flash("No video selected or invalid format.", "warning")

        return redirect(url_for('gesture_community'))

    return render_template('gesture_community.html')


@app.route('/dating')
def dating():
    return render_template('dating_paywall.html', is_paid=user_vip_status["is_paid"])


@app.route('/process-payment', methods=['POST'])
def process_payment():
    user_vip_status["is_paid"] = True
    flash("Payment successful! Welcome to VIP Court Matching.", "success")
    return redirect(url_for('dating'))


@app.route('/healthz')
def healthz():
    return {"status": "healthy", "app": "tennisgirls"}, 200


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
