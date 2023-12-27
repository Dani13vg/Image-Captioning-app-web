import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from model import caption_image
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
from helpers import login_required

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

# function to get database connection
def get_db_connection():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row  # to access columns by name
    return conn

# Function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    
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

    # Forget any user_id
    session.clear()

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
        conn = get_db_connection()
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
        conn = get_db_connection()
        username = conn.execute("SELECT * FROM users WHERE username = ?", (request.form.get("username"),)).fetchone()
        conn.close()

        # Ensure username does not already exist
        if username:
            flash("Username already exists", "warning")
            return render_template("register.html")
        
        # Insert new user into database
        conn = get_db_connection()
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

# Route to handle image uploads
@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_image():

    # Handle POST request
    if request.method == 'POST':

        # Check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        file = request.files['file']

        # If user does not select file, browser also submits an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            # Process image for captioning
            raw_image = Image.open(file_path).convert('RGB')
            inputs = processor(raw_image, return_tensors="pt")
            outputs = model.generate(**inputs)
            caption = processor.decode(outputs[0], skip_special_tokens=True)

            # Store the image path and caption in the database
            user_id = session['user_id']  # Assuming you have user authentication set up
            conn = get_db_connection()
            conn.execute('INSERT INTO captions (user_id, image_path, caption_text) VALUES (?, ?, ?)',
                         (user_id, file_path, caption))
            conn.commit()
            conn.close()

            # Provide the caption to the template for display
            return render_template('upload.html', caption=caption, image_url=file_path)

    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)