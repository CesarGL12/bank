from flask import (
    Flask, request, make_response, flash,
    redirect, render_template, g, abort)
from flask_wtf.csrf import CSRFProtect
from user_service import get_user_with_credentials, login_required
from account_service import get_balance, do_transfer


app = Flask(__name__)

app.config['SECRET_KEY'] = '7250f4518bf1f333a29b239f7629ea84369d90f425a6d4130ead8687be962c'
csrf = CSRFProtect(app)


@app.route("/", methods=['GET'])
@login_required
def home():
    return redirect("/dashboard")


@app.route("/login", methods=["POST"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")
    user = get_user_with_credentials(email, password)
    if not user:
        return render_template("login.html", error="Invalid credentials")
    response = make_response(redirect("/dashboard"))
    response.set_cookie("auth_token", user["token"])
    return response, 303


@app.route("/logout", methods=['GET'])
def logout():
    response = make_response(redirect("/dashboard"))
    response.delete_cookie('auth_token')
    return response, 303


@app.route("/dashboard", methods=['GET'])
@login_required
def dashboard():
    return render_template("dashboard.html", email=g.user)


@app.route("/details", methods=['GET'])
@login_required
def details():
    account_number = request.args['account']
    return render_template(
        "details.html", 
        user=g.user,
        account_number=account_number,
        balance = get_balance(account_number, g.user))


@app.route("/transfer", methods=["GET", "POST"])
@login_required
def transfer():
    """
    Handles the funds transfer form.
    - GET: Renders transfer form.
    - POST: Validates and processes the transfer securely.
    """
    if request.method == "GET":
        return render_template("transfer.html", user=g.user)

    source = request.form.get("from")
    target = request.form.get("to")
    try:
        amount = int(request.form.get("amount"))
    except ValueError:
        abort(400, "Invalid amount, needs to be an integer")

    if amount < 0:
        abort(400, "NO STEALING")
    if amount > 1000:
        abort(400, "WOAH THERE TAKE IT EASY")

    available_balance = get_balance(source, g.user)
    if available_balance is None:
        abort(404, "Account not found")
    if amount > available_balance:
        abort(400, "You don't have that much")

    if do_transfer(source, target, amount):
        flash("Transfer successful")
    else:
        abort(400, "Something bad happened")

    response = make_response(redirect("/dashboard"))
    return response, 303