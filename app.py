import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from model import apology, login_required, lookup, usd
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

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
@login_required
def index():
    """Show portfolio of stocks"""

    # Get user's portfolio and cash
    portfolio = db.execute("SELECT symbol, SUM(shares) as total_shares FROM transactions WHERE user_id = ? GROUP BY symbol HAVING total_shares > 0", session["user_id"])
    cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]

    # Add current price and total value to each stock
    for item in portfolio:
        stock = lookup(item["symbol"])
        item["current_price"] = stock["price"]
        item["total_value"] = stock["price"] * item["total_shares"]

    return render_template("index.html", portfolio=portfolio, cash=cash)



@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        symbol = request.form.get("symbol").upper()
        shares = request.form.get("shares")

        # Ensure symbol was submitted
        if not symbol:
            return apology("must provide symbol", 400)

        # Ensure shares was submitted
        if not shares or not shares.isdigit() or int(shares) <= 0:
            return apology("must provide a positive integer for shares", 400)

        # Ensure symbol is valid
        shares = int(shares)
        stock = lookup(symbol)
        if stock is None:
            return apology("invalid symbol", 400)

        # Ensure user has enough cash
        cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]
        total_cost = stock["price"] * shares
        if total_cost > cash:
            return apology("not enough cash", 400)

        # Buy shares
        db.execute("""INSERT INTO transactions (user_id, symbol, name, shares, price, type)VALUES (?, ?, ?, ?, ?, ?)""",
                    session["user_id"], symbol, stock["name"], shares, stock["price"], 'BUY')

        # Update user's cash
        db.execute("UPDATE users SET cash = cash - ? WHERE id = ?", total_cost, session["user_id"])

        return redirect("/")

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    # Get user's transactions history from database
    transactions = db.execute("""
                            SELECT type, symbol, name, shares, price, transacted
                            FROM transactions
                            WHERE user_id = ?
                            ORDER BY transacted DESC""",
                            session["user_id"])

    return render_template("history.html", transactions=transactions)



@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        symbol = request.form.get("symbol")

        # Ensure symbol was submitted
        if not symbol:
            return apology("must provide symbol", 400)

        # Ensure symbol is valid
        stock = lookup(symbol)
        if stock is None:
            return apology("invalid symbol", 400)

        return render_template("quoted.html", stock=stock)

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Ensure username was submitted
        if not username:
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not password or not confirmation:
            return apology("must provide password and confirmation", 400)

        # Ensure password and confirmation match
        elif password != confirmation:
            return apology("passwords do not match", 400)

        # Ensure username is not already taken
        hash = generate_password_hash(password)
        result = db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hash)
        if not result:
            return apology("username already exists", 400)

        return redirect("/login")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        # Ensure symbol was submitted
        if not symbol:
            return apology("must select a stock", 400)

        # Ensure shares was submitted
        if not shares or not shares.isdigit() or int(shares) <= 0:
            return apology("must provide a positive integer for shares", 400)

        # Ensure user has enough shares
        shares = int(shares)
        user_shares = db.execute("SELECT shares FROM transactions WHERE user_id = ? AND symbol = ? GROUP BY symbol", session["user_id"], symbol)[0]["shares"]
        if shares > user_shares:
            return apology("not enough shares", 400)

        # Sell shares
        stock = lookup(symbol)
        db.execute("INSERT INTO transactions (user_id, symbol, shares, price) VALUES (?, ?, ?, ?)", session["user_id"], symbol, -shares, stock["price"])
        db.execute("UPDATE users SET cash = cash + ? WHERE id = ?", stock["price"] * shares, session["user_id"])

        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        owned_stocks = db.execute("SELECT symbol FROM transactions WHERE user_id = ? GROUP BY symbol HAVING SUM(shares) > 0", session["user_id"])
        return render_template("sell.html", stocks=owned_stocks)


# Personal Touch: Change Password Functionality
@app.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure current password was submitted
        if not request.form.get("current_password"):
            return apology("must provide current password", 403)

        # Ensure new password was submitted
        elif not request.form.get("new_password"):
            return apology("must provide new password", 403)

        # Ensure confirmation of new password was submitted
        elif not request.form.get("confirmation"):
            return apology("must provide new password confirmation", 403)

        # Query database for user
        user_id = session["user_id"]
        rows = db.execute("SELECT * FROM users WHERE id = ?", user_id)

        # Check if the current password is correct
        if not check_password_hash(rows[0]["hash"], request.form.get("current_password")):
            return apology("invalid current password", 403)

        # Check if new password and confirmation match
        if request.form.get("new_password") != request.form.get("confirmation"):
            return apology("new passwords do not match", 403)

        # Update user's password
        new_hash = generate_password_hash(request.form.get("new_password"))
        db.execute("UPDATE users SET hash = ? WHERE id = ?", new_hash, user_id)

        # Redirect user to home page
        flash("Password changed!")
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("change_password.html")
