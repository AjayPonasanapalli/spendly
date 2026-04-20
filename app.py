import os
import json
import sqlite3
from collections import defaultdict
from datetime import date, timedelta
from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import check_password_hash
from database.db import get_db, init_db, seed_db, create_user, get_user_by_email

app = Flask(__name__)
app.secret_key = os.urandom(24)

with app.app_context():
    init_db()
    seed_db()


# ------------------------------------------------------------------ #
# Routes                                                              #
# ------------------------------------------------------------------ #

@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")
    confirm_password = request.form.get("confirm_password", "")

    if not name:
        return render_template("register.html", error="Name is required.", name=name, email=email)
    if len(password) < 8:
        return render_template("register.html", error="Password must be at least 8 characters.", name=name, email=email)
    if password != confirm_password:
        return render_template("register.html", error="Passwords do not match.", name=name, email=email)

    try:
        create_user(name, email, password)
    except sqlite3.IntegrityError:
        return render_template("register.html", error="An account with that email already exists.", name=name, email=email)

    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")

    user = get_user_by_email(email)
    if user is None or not check_password_hash(user["password_hash"], password):
        return render_template("login.html", error="Invalid email or password.", email=email)

    session["user_id"] = user["id"]
    session["user_name"] = user["name"]
    return redirect(url_for("dashboard"))


@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


# ------------------------------------------------------------------ #
# Placeholder routes — students will implement these                  #
# ------------------------------------------------------------------ #

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("landing"))


@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = get_db()
    expenses = conn.execute(
        "SELECT * FROM expenses WHERE user_id = ? ORDER BY date DESC",
        (session["user_id"],)
    ).fetchall()
    conn.close()

    # ---- Stats ----
    today = date.today()
    month_start = today.replace(day=1).isoformat()
    total_all   = sum(e["amount"] for e in expenses)
    total_month = sum(e["amount"] for e in expenses if e["date"] >= month_start)

    # Category breakdown (all time)
    cat_totals = defaultdict(float)
    for e in expenses:
        cat_totals[e["category"]] += e["amount"]
    cat_labels = list(cat_totals.keys())
    cat_values = [round(cat_totals[k], 2) for k in cat_labels]

    # Monthly totals — last 6 months
    monthly = {}
    for i in range(5, -1, -1):
        d = (today.replace(day=1) - timedelta(days=i * 28))
        key = d.strftime("%b %Y")
        monthly[key] = 0.0
    for e in expenses:
        d = date.fromisoformat(e["date"])
        key = d.strftime("%b %Y")
        if key in monthly:
            monthly[key] = round(monthly[key] + e["amount"], 2)
    month_labels = list(monthly.keys())
    month_values = list(monthly.values())

    top_category = max(cat_totals, key=cat_totals.get) if cat_totals else "—"

    return render_template(
        "dashboard.html",
        expenses=expenses,
        total_all=total_all,
        total_month=total_month,
        top_category=top_category,
        cat_labels=json.dumps(cat_labels),
        cat_values=json.dumps(cat_values),
        month_labels=json.dumps(month_labels),
        month_values=json.dumps(month_values),
    )


@app.route("/profile")
def profile():
    return "Profile page — coming in Step 4"


@app.route("/expenses/add")
def add_expense():
    return "Add expense — coming in Step 7"


@app.route("/expenses/<int:id>/edit")
def edit_expense(id):
    return "Edit expense — coming in Step 8"


@app.route("/expenses/<int:id>/delete")
def delete_expense(id):
    return "Delete expense — coming in Step 9"


if __name__ == "__main__":
    app.run(debug=True, port=5001)
