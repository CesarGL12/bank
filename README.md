# 🏦 Secure Banking Web Application

This project is a secure, full-stack banking web application built with Python (Flask), SQLite, and modern security practices. It supports user authentication, account management, and fund transfers while defending against common web vulnerabilities such as XSS, CSRF, SQL Injection, and user enumeration.

## 🚀 Features

- 🔐 Secure user registration and login with PBKDF2 salted password hashing
- 🍪 JWT-based authentication stored in secure HTTP-only cookies
- 💸 Transfer functionality between user accounts with atomic transactions
- 🛡️ Protection against XSS, CSRF, SQL Injection, and user enumeration
- 👁️‍🗨️ Input validation and error handling with generic error messages
- 🧪 Fully commented source code to explain security defenses

## 📁 Project Structure

```
bank/
├── bin/
│   ├── createdb.py          # Initializes the SQLite database
│   └── makeaccounts         # Script to create test accounts
├── templates/
│   ├── dashboard.html
│   ├── details.html
│   ├── login.html
│   └── transfer.html
├── account_service.py       # Business logic for account and transaction handling
├── app.py                   # Flask application routes and authentication logic
├── user_service.py          # User registration and login services
├── bank.db                  # SQLite database
├── .env                     # Environment variables (e.g., secret keys)
├── .gitignore
├── .pylintrc
└── README.md                # You’re reading it!
```

## 🔒 Security Practices

This application demonstrates how to implement and **explain** common security measures in web development:

| Threat                | Defense Strategy |
|-----------------------|------------------|
| Password Theft        | PBKDF2 salted hashing using `hashlib.pbkdf2_hmac` |
| XSS                   | Auto-escaped HTML templates (Jinja2), no raw HTML output |
| CSRF                  | CSRF tokens embedded in forms and verified on POST |
| SQL Injection         | Use of parameterized queries (`?` placeholders with DB APIs) |
| User Enumeration      | Generic login error messages and uniform response times |
| Session Hijacking     | JWT stored in secure HTTP-only cookies |

All major security points are extensively documented in comments throughout the source code.

## 🧰 Technologies Used

- **Flask** (Python Web Framework)
- **SQLite** (Lightweight embedded database)
- **JWT** (Authentication tokens)
- **Python dotenv** (Environment variable handling)

## 🧪 Getting Started

### Prerequisites

- Python 3.8+
- `pip install -r requirements.txt` (Flask, python-dotenv, etc.)

### Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/CesarGL12/bank.git
   cd bank/bank
   ```

2. Create and initialize the database:
   ```bash
   python bin/createdb.py
   python bin/makeaccounts
   ```

3. Set up your environment variables in `.env`:
   ```
   SECRET_KEY=your_flask_secret_key
   JWT_SECRET=your_jwt_secret
   ```

4. Run the app:
   ```bash
   flask run
   ```

5. Navigate to `http://localhost:5000` in your browser.

## 👨‍💻 Developer Notes

This project is for educational use and demonstrates real-world security practices in a simplified environment. For production-grade applications, consider using:
- HTTPS (with Flask-Talisman or a proper WSGI server like Gunicorn + Nginx)
- A production-grade database (e.g., PostgreSQL)
- Logging and monitoring tools
- Automated testing

## 📚 Learning Objectives

This project helped reinforce understanding of:
- Secure authentication flows
- Practical defenses against common web threats
- Proper error handling and input validation
- Thoughtful documentation of security measures
