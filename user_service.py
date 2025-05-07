import os
from functools import wraps
import sqlite3
import datetime
import jwt
from passlib.hash import pbkdf2_sha256
from flask import request, g, render_template
from dotenv import load_dotenv


load_dotenv()
SECRET = os.getenv('SECRET')


def login_required(func):
    """
    Flask decorator to enforce authentication on protected routes.
    If the JWT cookie is invalid or missing, shows the login page.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not logged_in():
            return render_template("login.html")
        return func(*args, **kwargs)
    return wrapper


def get_user_with_credentials(email, password):
    """
    Authenticates a user by checking their email and password.
    
    Security Defenses:
    - Passwords are verified using PBKDF2 (slow hashing, salted).
    - SQL Injection prevented via parameterized query.
    - User Enumeration defense: Returns None both if email is wrong or password fails.
    """
    try:
        con = sqlite3.connect('bank.db')
        cur = con.cursor()
        cur.execute('''
            SELECT email, name, password FROM users where email=?''',
            (email,))
        row = cur.fetchone()
        if row is None:
            return None
        email, name, hash = row
        if not pbkdf2_sha256.verify(password, hash):
            return None
        return {"email": email, "name": name, "token": create_token(email)}
    finally:
        con.close()

def logged_in():
    """
    Checks for a valid JWT cookie and sets the user info in `g.user`.

    Security Defenses:
    - Tokens signed using HS256 and stored in HTTP-only cookies.
    - Expired or tampered tokens are silently rejected.
    """
    token = request.cookies.get('auth_token')
    try:
        data = jwt.decode(token, SECRET, algorithms=['HS256'])
        g.user = data['sub']
        return True
    except jwt.InvalidTokenError:
        return False

def create_token(email):
    """
    Creates a signed JWT token with an expiration time.

    Security:
    - Tokens expire after 60 minutes (defense against token replay).
    """
    now = datetime.datetime.now(datetime.timezone.utc)
    payload = {'sub': email, 'iat': now, 
               'exp': now + datetime.timedelta(minutes=60)}
    token = jwt.encode(payload, SECRET, algorithm='HS256')
    return token