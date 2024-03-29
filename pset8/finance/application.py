import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    # look up the current user
    users = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=session["user_id"])
    stocks = db.execute(
        "SELECT symbol, SUM(shares) as total_shares FROM transactions WHERE user_id = :user_id GROUP BY symbol HAVING total_shares > 0", user_id=session["user_id"])
    quotes = {}
    current_share_value = 0

    for stock in stocks:
        quotes[stock["symbol"]] = lookup(stock["symbol"])
        current_share_value = current_share_value + stock["total_shares"] * quotes[stock["symbol"]]["price"]


    cash_remaining = users[0]["cash"]
    total = cash_remaining + current_share_value

    return render_template("portfolio.html", quotes=quotes, stocks=stocks, total=total, cash_remaining=cash_remaining)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        quote = lookup(request.form.get("symbol"))

        # Check if the symbol exists
        if quote == None:
            return apology("invalid symbol", 400)

        # Check if number of shares is a positive number
        try:
            shares = int(request.form.get("shares"))
        except:
            return apology("must be positive integer", 400)

        if shares <= 0:
            return apology("must be greater than 0", 400)

        # Query database for username
        rows = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=session["user_id"])

        # How much money left in account
        cash_remaining = rows[0]["cash"]

        # Check the total purchase price
        purchase_price = quote["price"] * shares

        if purchase_price > cash_remaining:
            return apology("not enough funds", 400)

        db.execute("UPDATE users SET cash = cash - :price WHERE id = :user_id", price=purchase_price, user_id=session["user_id"])

        db.execute("INSERT INTO transactions (user_id, symbol, shares, price_per_share) VALUES(:user_id, :symbol, :shares, :price)",
           user_id=session["user_id"],
           symbol=request.form.get("symbol").upper(),
           shares=shares,
           price=quote["price"])

        flash("Bought!")

        return redirect("/")

    else:
        return render_template("buy.html")


@app.route("/check", methods=["GET"])
def check():
    """Return true if username available, else false, in JSON format"""
    return jsonify("TODO")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    # look up the current user transactions
    transactions = db.execute("SELECT symbol, shares, price_per_share, created_at FROM transactions WHERE user_id = :user_id ORDER BY created_at DESC", user_id=session["user_id"])

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
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

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

    if request.method == "POST":
        if not request.form.get("symbol"):
            return apology("missing symbol", 400)
        else:
            quote = lookup(request.form.get("symbol"))

        return render_template("quoted.html", quote=quote)

    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """User register"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        if not request.form.get("username"):
            return apology("must provide username", 400)
        else:
            username = request.form.get("username")

        # Ensure password was submitted
        if not request.form.get("password"):
            return apology("must provide password", 400)
        else:
            password = request.form.get("password")

        if not request.form.get("confirmation") == password:
            return apology("must provide the same password", 400)

        # Hash password
        hash = generate_password_hash(password)

        # Save user profile in database
        new_user_id = db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)", username = username, hash = hash)

        # Must be unique username:
        if not new_user_id:
            return apology("sorry, the username taken", 400)


        # Remember which user has logged in
        session["user_id"] = new_user_id

        # Redirect user to home page
        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":
        quote = lookup(request.form.get("symbol"))

        # Check if the symbol exists
        if quote == None:
            return apology("invalid symbol", 400)

        # Check if number of shares is a positive number
        try:
            shares = int(request.form.get("shares"))
        except:
            return apology("must be positive integer", 400)

        if shares <= 0:
            return apology("must be greater than 0", 400)

        # Query database for number of shares per symbol
        stock = db.execute("SELECT SUM(shares) total_shares FROM transactions WHERE user_id = :user_id AND symbol = :symbol GROUP BY symbol HAVING total_shares > 0", user_id=session["user_id"], symbol=request.form.get("symbol"))

        if len(stock) != 1 or stock[0]["total_shares"] <= 0 or stock[0]["total_shares"] < shares:
            return apology("you can't sell less than 0 or more than you own", 400)

        # Query database for username
        rows = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=session["user_id"])

        # How much money left in account
        cash_remaining = rows[0]["cash"]

        # Check the total selling price
        selling_price = quote["price"] * shares

        db.execute("UPDATE users SET cash = cash + :price WHERE id = :user_id", price=selling_price, user_id=session["user_id"])

        db.execute("INSERT INTO transactions (user_id, symbol, shares, price_per_share) VALUES(:user_id, :symbol, :shares, :price)",
           user_id=session["user_id"],
           symbol=request.form.get("symbol").upper(),
           shares=-shares,
           price=quote["price"])

        flash("Sold!")

        return redirect("/")

    else:
        stocks = db.execute("SELECT symbol, SUM(shares) as total_shares FROM transactions WHERE user_id = :user_id GROUP BY symbol HAVING total_shares > 0", user_id=session["user_id"])
        return render_template("sell.html", stocks=stocks)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
