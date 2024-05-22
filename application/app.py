import pymysql
pymysql.install_as_MySQLdb()

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_bcrypt import Bcrypt
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Regexp
from flask_wtf.csrf import CSRFProtect
import logging
from db_connection import db, User, get_db_connection
from search import search_bp
from item_submission import item_bp
from dashboard import dashboard_bp
from compose import compose
from recent_items import recent_items
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from forms import ComposeForm

# Set up logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__, static_folder='./public', template_folder='./public/html')

# Configuration settings
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:newpassword@localhost/FromHereToThere'
app.config['WTF_CSRF_ENABLED'] = True
db.init_app(app)

# Initialize extensions
bcrypt = Bcrypt(app)
csrf = CSRFProtect(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Define the signup form
class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[
        DataRequired(), Email(), Regexp(r'.*@(mail\.sfsu\.edu|sfsu\.edu)$', message="Must be a valid SFSU email")
    ])
    password = PasswordField('Password', validators=[
        DataRequired(), Length(min=8, message="Password must be at least 8 characters long")
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(), EqualTo('password', message="Passwords must match")
    ])
    agree_tos = BooleanField('I agree to the Terms of Service', validators=[DataRequired()])
    submit = SubmitField('Signup')

# Define the login form
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

# Register Blueprints
app.register_blueprint(search_bp, url_prefix="")
app.register_blueprint(item_bp, url_prefix="")
app.register_blueprint(recent_items, url_prefix="")
app.register_blueprint(compose, url_prefix="")
app.register_blueprint(dashboard_bp, url_prefix="")

# Define routes
@app.route('/Index.html')
@app.route('/')
def index():
    return render_template('Index.html')

@app.route('/about')
def about():
    return render_template('about/About.html')

@app.route('/about/Justin.html')
def justin():
    return render_template('about/Justin.html')

@app.route('/about/Douglas.html')
def douglas():
    return render_template('about/Douglas.html')

@app.route('/about/GioJung.html')
def giojung():
    return render_template('about/GioJung.html')

@app.route('/about/Gurpreet.html')
def gurpreet():
    return render_template('about/Gurpreet.html')

@app.route('/about/Gursimran.html')
def gursimran():
    return render_template('about/Gursimran.html')

@app.route('/about/Omar.html')
def omar():
    return render_template('about/Omar.html')

@app.route('/SellRent.html')
@login_required
def sell():
    return render_template('SellRent.html')

@app.route('/Search.html')
def search_page():
    return render_template('Search.html')

@app.route('/Signup.html', methods=['GET', 'POST'])
def signup_page():
    form = SignupForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data

        # Ensure the password is hashed
        hashed_password = generate_password_hash(password)
        logging.debug(f"Hashed password: {hashed_password}")

        try:
            conn = get_db_connection()
            if conn:
                cursor = conn.cursor()
                try:
                    # Check if the email or username already exists
                    cursor.execute("SELECT * FROM User WHERE Email = %s OR UserName = %s", (email, username))
                    existing_user = cursor.fetchone()

                    if existing_user:
                        flash('An account with this email or username already exists.', 'danger')
                    else:
                        cursor.execute(
                            "INSERT INTO User (UserName, Email, Password) VALUES (%s, %s, %s)",
                            (username, email, hashed_password)
                        )
                        conn.commit()
                        flash('Your account has been created!', 'success')
                        return redirect(url_for('login'))
                except Exception as err:
                    logging.error(f"Database error: {err}")
                    flash(f"Database error: {err}", 'danger')
                finally:
                    cursor.fetchall()  # Ensure all results are read
                    cursor.close()
                    conn.close()
            else:
                flash('Database connection failed', 'danger')
        except Exception as e:
            logging.error(f"Error: {e}")
            flash(f"Error: {e}", 'danger')
    else:
        # Debugging: Print form validation errors
        for fieldName, errorMessages in form.errors.items():
            for err in errorMessages:
                logging.debug(f"Error in {fieldName}: {err}")
                flash(f"Error in {fieldName}: {err}", 'danger')
    return render_template('Signup.html', form=form)


@app.route('/Login.html', methods=['GET', 'POST'])
def login():
    logging.debug("Login route accessed")

    if current_user.is_authenticated:
        logging.debug("User is already authenticated, redirecting to dashboard")
        return redirect(url_for('dashboard_page'))
    
    form = LoginForm()
    logging.debug(f"Form created: {form}")

    if form.validate_on_submit():
        logging.debug("Form is validated")
        email = form.email.data
        password = form.password.data
        logging.debug(f"Form data: email={email}, password=*****")

        user = User.query.filter_by(Email=email).first()
        if user:
            logging.debug(f"User found: {user.UserName}")
            logging.debug(f"User password hash: {user.Password}")
            try:
                if check_password_hash(user.Password, password):
                    logging.debug("Password check passed")
                    login_user(user)
                    flash('Logged in successfully!', 'success')
                    return redirect(url_for('dashboard_page'))
                else:
                    logging.debug("Password check failed")
                    flash('Invalid email or password', 'danger')
            except ValueError as e:
                logging.error(f"Error in password hash check: {e}")
                flash('Invalid email or password', 'danger')
        else:
            logging.debug("User not found")
            flash('Invalid email or password', 'danger')
    else:
        logging.debug("Form validation failed")
        for fieldName, errorMessages in form.errors.items():
            for err in errorMessages:
                logging.debug(f"Validation error in {fieldName}: {err}")

    logging.debug("Rendering login template")
    return render_template('Login.html', form=form)

@app.route('/Dashboard.html')
@login_required
def dashboard_page():
    return render_template('Dashboard.html', user=current_user)

@app.route('/fetch_messages')
@login_required
def fetch_messages():
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500

    cursor = conn.cursor(pymysql.cursors.DictCursor)
    try:
        cursor.execute("""
            SELECT 
                m.MessageTitle, 
                m.MessageText, 
                m.MessageDateTime, 
                u.UserName 
            FROM 
                Message m 
            JOIN 
                User u 
            ON 
                m.SenderUserID = u.UserID 
            WHERE 
                m.ReceiverUserID = %s 
            ORDER BY 
                m.MessageDateTime DESC
        """, (current_user.UserID,))
        messages = cursor.fetchall()
        logging.debug(f"Messages fetched: {messages}")
        return jsonify(messages)
    finally:
        cursor.close()
        conn.close()

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

@app.route('/send_message', methods=['POST'])
@login_required
def send_message():
    form = ComposeForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        subject = form.subject.data
        message = form.message.data
        receiver_id = form.receiver_id.data
        listing_id = form.listing_id.data

        try:
            conn = get_db_connection()
            if conn:
                cursor = conn.cursor()
                try:
                    cursor.execute(
                        "INSERT INTO Message (SenderUserID, ReceiverUserID, ListingID, SenderName, SenderEmail, MessageTitle, MessageText, MessageDateTime) VALUES (%s, %s, %s, %s, %s, %s, %s, NOW())",
                        (current_user.UserID, receiver_id, listing_id, name, email, subject, message)
                    )
                    conn.commit()
                    flash('Message sent successfully!', 'success')
                    return redirect(url_for('dashboard_page'))
                except Exception as err:
                    logging.error(f"Database error: {err}")
                    flash(f"Database error: {err}", 'danger')
                finally:
                    cursor.close()
                    conn.close()
            else:
                flash('Database connection failed', 'danger')
        except Exception as e:
            logging.error(f"Error: {e}")
            flash(f"Error: {e}", 'danger')
    else:
        flash('Form validation failed. Please check your input.', 'danger')

    return redirect(url_for('compose.compose_page'))

@app.route('/item_details')
def item_details():
    listing_id = request.args.get('listing_id')

    if not listing_id:
        flash('Listing ID is missing.', 'danger')
        return redirect(url_for('index'))

    try:
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT Listing.*, Category.CategoryName, User.UserName 
                FROM Listing 
                JOIN Category ON Listing.CategoryID = Category.CategoryID 
                JOIN User ON Listing.UserID = User.UserID 
                WHERE ListingID = %s
            """, (listing_id,))
            item = cursor.fetchone()
            cursor.close()
            conn.close()

            if not item:
                flash('Item not found.', 'danger')
                return redirect(url_for('index'))

            logging.info(f"Item fetched: {item}")

            return render_template('ItemPage.html', item=item)
        else:
            flash('Database connection failed.', 'danger')
            return redirect(url_for('index'))
    except Exception as e:
        logging.error(f"Error fetching item details: {e}")
        flash(f"Error fetching item details: {e}", 'danger')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
