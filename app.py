import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from model import caption_image
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
from helpers import login_required, get_db_connection, allowed_file

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure upload folder and allowed extensions for uploaded images
UPLOAD_FOLDER = os.path.join('static', 'images')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Load the model
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large")
    
@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
def index():
    """Show index page"""

    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted

        username = request.form.get("username")
        password = request.form.get("password")

        # Enusre username and password were submitted
        if not username or not password:
            flash("Must provide username and password", "warning")
            return render_template("login.html")
        
        # Query database for username
        conn = get_db_connection("users.db")
        user = conn.execute("SELECT * FROM users WHERE username = ?", (request.form.get("username"),)).fetchone()
        conn.close()

        # Ensure username exists and password is correct
        if user is None or not check_password_hash(user["password"], request.form.get("password")):
            flash("Invalid username and/or password")
            return render_template("login.html")
        
        # Remember which user has logged in
        session["user_id"] = user["id"]
        session["username"] = user["username"]

        # Redirect user to home page
        flash("You have successfully logged in")
        return redirect("/upload")
    else:
        return render_template("login.html")
    
@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to home page
    flash("You have successfully logged out")
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username and password were submitted
        if not request.form.get("username") or not request.form.get("password"):
            flash("Must provide username and password", "warning")
            return render_template("register.html")
        
        # Ensure password and confirmation match
        if request.form.get("password") != request.form.get("confirmation"):
            flash("Password and confirmation must match", "warning")
            return render_template("register.html")
        
        # Query database for username
        conn = get_db_connection("users.db")
        username = conn.execute("SELECT * FROM users WHERE username = ?", (request.form.get("username"),)).fetchone()
        conn.close()

        # Ensure username does not already exist
        if username:
            flash("Username already exists", "warning")
            return render_template("register.html")
        
        # Insert new user into database
        conn = get_db_connection("users.db")
        conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", (request.form.get("username"), generate_password_hash(request.form.get("password"))))
        conn.commit()
        conn.close()

        # Redirect user to login page
        flash("You have successfully registered")
        return redirect("/login")
    else:
        return render_template("register.html")
    
@app.route("/usage")
def usage():
    """Show usage page"""
    return render_template("usage.html")

@app.route("/contact")
def contact():
    """Show contact page"""
    return render_template("contact.html")

@app.route("/history")
@login_required
def history():
    """Show history page"""

    # Query database for captions
    conn = get_db_connection("users.db")
    captions = conn.execute("SELECT * FROM captions WHERE user_id = ?", (session["user_id"],)).fetchall()
    conn.close()

    return render_template("history.html", captions=captions)

# Route to handle image uploads
@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_image():

    # Handle POST request
    if request.method == 'POST':

        # Check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url) # redirect to the same url
        
        file = request.files['file']

        # If user does not select file, browser also submits an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url) # redirect to the same url
        
        # If file is valid, save it to the upload folder
        if file and allowed_file(file.filename, ALLOWED_EXTENSIONS):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            # Generate caption for the image
            caption = caption_image(file_path) # defined in model.py

            # Store the image path and caption in the database
            user_id = session['user_id']  # Assuming you have user authentication set up
            conn = get_db_connection("users.db")
            conn.execute('INSERT INTO captions (user_id, image_path, caption_text) VALUES (?, ?, ?)',
                         (user_id, file_path, caption))
            conn.commit()
            conn.close()

            # Provide the caption to the template for display
            return render_template('upload.html', caption=caption, image_url=file_path)

    return render_template('upload.html')

@app.route("/clear_history", methods=["POST"])
@login_required
def clear_history():
    """Clear the user's history"""

    user_id = session['user_id']

    # Open a new database connection and delete the user's history
    conn = get_db_connection('users.db')
    conn.execute("DELETE FROM captions WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()

    flash("History cleared successfully", "info")
    return redirect(url_for('history'))


if __name__ == '__main__':
    app.run(debug=True)