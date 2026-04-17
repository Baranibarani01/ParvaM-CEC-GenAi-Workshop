import os
import re
import sqlite3
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, flash, session, g
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "replace_this_with_a_random_secret_key"

DATABASE = os.path.join(app.root_path, "users.db")

EMAIL_REGEX = re.compile(r"^[\w\.-]+@[\w\.-]+\.\w+$")
PASSWORD_REGEX = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*\W).{8,14}$")
PHONE_REGEX = re.compile(r"^\d{10,14}$")


def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()


def init_db():
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            phone TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            phone TEXT NOT NULL UNIQUE,
            course TEXT NOT NULL,
            year TEXT NOT NULL,
            address TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    db.commit()
    db.close()


def validate_password(password: str) -> bool:
    return bool(PASSWORD_REGEX.match(password))


def validate_email(email: str) -> bool:
    return bool(EMAIL_REGEX.match(email))


def validate_phone(phone: str) -> bool:
    return bool(PHONE_REGEX.match(phone))


def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if not session.get("user_id"):
            flash("Please log in to access this page.", "danger")
            return redirect(url_for("login"))
        return view(**kwargs)
    return wrapped_view


def get_student(student_id: int):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM students WHERE id = ?", (student_id,))
    return cursor.fetchone()


def get_user(user_id: int):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()


@app.route("/")
def index():
    if session.get("user_id"):
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))


@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = {"name": "", "email": "", "phone": ""}
    if request.method == "POST":
        form["name"] = request.form.get("name", "").strip()
        form["email"] = request.form.get("email", "").strip().lower()
        form["phone"] = request.form.get("phone", "").strip()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        if not form["name"] or not form["email"] or not form["phone"] or not password or not confirm_password:
            flash("All fields are required. Please complete the form.", "danger")
            return render_template("signup.html", form=form)

        if not validate_email(form["email"]):
            flash("Enter a valid email address.", "danger")
            return render_template("signup.html", form=form)

        if not validate_phone(form["phone"]):
            flash("Phone must be 10 to 14 digits without spaces or symbols.", "danger")
            return render_template("signup.html", form=form)

        if password != confirm_password:
            flash("Password and confirmation do not match.", "danger")
            return render_template("signup.html", form=form)

        if not validate_password(password):
            flash(
                "Password must be 8-14 chars and include uppercase, lowercase, number, and special character.",
                "danger",
            )
            return render_template("signup.html", form=form)

        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT id FROM users WHERE email = ? OR phone = ?", (form["email"], form["phone"]))
        existing = cursor.fetchone()
        if existing:
            cursor.execute("SELECT id FROM users WHERE email = ?", (form["email"],))
            if cursor.fetchone():
                flash("This email is already registered. Please log in or use another email.", "danger")
            else:
                flash("This phone number is already registered. Please use another phone number.", "danger")
            return render_template("signup.html", form=form)

        hashed_password = generate_password_hash(password)
        cursor.execute(
            "INSERT INTO users (name, email, phone, password) VALUES (?, ?, ?, ?)",
            (form["name"], form["email"], form["phone"], hashed_password),
        )
        db.commit()
        flash("Signup successful! You can now log in.", "success")
        return redirect(url_for("login"))

    return render_template("signup.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if not email or not password:
            flash("Enter both email and password.", "danger")
            return render_template("login.html", email=email)

        if not validate_email(email):
            flash("Enter a valid email address.", "danger")
            return render_template("login.html", email=email)

        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()

        if not user or not check_password_hash(user["password"], password):
            flash("Invalid email or password. Please try again.", "danger")
            return render_template("login.html", email=email)

        session["user_id"] = user["id"]
        session["user_name"] = user["name"]
        flash(f"Welcome back, {user['name']}!", "success")
        return redirect(url_for("dashboard"))

    return render_template("login.html")


@app.route("/students")
@login_required
def student_list():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM students ORDER BY created_at DESC")
    students = cursor.fetchall()
    return render_template("student_list.html", students=students)


@app.route("/students/new", methods=["GET", "POST"])
@login_required
def student_create():
    form = {"full_name": "", "email": "", "phone": "", "course": "", "year": "", "address": ""}
    if request.method == "POST":
        form["full_name"] = request.form.get("full_name", "").strip()
        form["email"] = request.form.get("email", "").strip().lower()
        form["phone"] = request.form.get("phone", "").strip()
        form["course"] = request.form.get("course", "").strip()
        form["year"] = request.form.get("year", "").strip()
        form["address"] = request.form.get("address", "").strip()

        if not form["full_name"] or not form["email"] or not form["phone"] or not form["course"] or not form["year"]:
            flash("All required fields must be completed.", "danger")
            return render_template("student_form.html", form=form, action="Create Student", submit_label="Register Student")

        if not validate_email(form["email"]):
            flash("Enter a valid email address for the student.", "danger")
            return render_template("student_form.html", form=form, action="Create Student", submit_label="Register Student")

        if not validate_phone(form["phone"]):
            flash("Student phone must be 10 to 14 digits without spaces or symbols.", "danger")
            return render_template("student_form.html", form=form, action="Create Student", submit_label="Register Student")

        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT id FROM students WHERE email = ? OR phone = ?", (form["email"], form["phone"]))
        existing = cursor.fetchone()
        if existing:
            cursor.execute("SELECT id FROM students WHERE email = ?", (form["email"],))
            if cursor.fetchone():
                flash("A student with this email already exists.", "danger")
            else:
                flash("A student with this phone number already exists.", "danger")
            return render_template("student_form.html", form=form, action="Create Student", submit_label="Register Student")

        cursor.execute(
            "INSERT INTO students (full_name, email, phone, course, year, address) VALUES (?, ?, ?, ?, ?, ?)",
            (form["full_name"], form["email"], form["phone"], form["course"], form["year"], form["address"]),
        )
        db.commit()
        flash("Student registered successfully.", "success")
        return redirect(url_for("student_list"))

    return render_template("student_form.html", form=form, action="Create Student", submit_label="Register Student")


@app.route("/students/<int:student_id>")
@login_required
def student_view(student_id):
    student = get_student(student_id)
    if not student:
        flash("Student not found.", "danger")
        return redirect(url_for("student_list"))
    return render_template("student_view.html", student=student)


@app.route("/students/<int:student_id>/edit", methods=["GET", "POST"])
@login_required
def student_edit(student_id):
    student = get_student(student_id)
    if not student:
        flash("Student not found.", "danger")
        return redirect(url_for("student_list"))

    form = {
        "full_name": student["full_name"],
        "email": student["email"],
        "phone": student["phone"],
        "course": student["course"],
        "year": student["year"],
        "address": student["address"] or "",
    }

    if request.method == "POST":
        form["full_name"] = request.form.get("full_name", "").strip()
        form["email"] = request.form.get("email", "").strip().lower()
        form["phone"] = request.form.get("phone", "").strip()
        form["course"] = request.form.get("course", "").strip()
        form["year"] = request.form.get("year", "").strip()
        form["address"] = request.form.get("address", "").strip()

        if not form["full_name"] or not form["email"] or not form["phone"] or not form["course"] or not form["year"]:
            flash("All required fields must be completed.", "danger")
            return render_template("student_form.html", form=form, action="Edit Student", submit_label="Update Student")

        if not validate_email(form["email"]):
            flash("Enter a valid email address for the student.", "danger")
            return render_template("student_form.html", form=form, action="Edit Student", submit_label="Update Student")

        if not validate_phone(form["phone"]):
            flash("Student phone must be 10 to 14 digits without spaces or symbols.", "danger")
            return render_template("student_form.html", form=form, action="Edit Student", submit_label="Update Student")

        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            "SELECT id FROM students WHERE (email = ? OR phone = ?) AND id != ?",
            (form["email"], form["phone"], student_id),
        )
        existing = cursor.fetchone()
        if existing:
            cursor.execute("SELECT id FROM students WHERE email = ? AND id != ?", (form["email"], student_id))
            if cursor.fetchone():
                flash("A student with this email already exists.", "danger")
            else:
                flash("A student with this phone number already exists.", "danger")
            return render_template("student_form.html", form=form, action="Edit Student", submit_label="Update Student")

        cursor.execute(
            "UPDATE students SET full_name = ?, email = ?, phone = ?, course = ?, year = ?, address = ? WHERE id = ?",
            (form["full_name"], form["email"], form["phone"], form["course"], form["year"], form["address"], student_id),
        )
        db.commit()
        flash("Student details updated successfully.", "success")
        return redirect(url_for("student_view", student_id=student_id))

    return render_template("student_form.html", form=form, action="Edit Student", submit_label="Update Student")


@app.route("/students/<int:student_id>/delete", methods=["POST"])
@login_required
def student_delete(student_id):
    student = get_student(student_id)
    if not student:
        flash("Student not found.", "danger")
        return redirect(url_for("student_list"))

    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
    db.commit()
    flash("Student record deleted successfully.", "success")
    return redirect(url_for("student_list"))


@app.route("/dashboard")
@login_required
def dashboard():
    user = get_user(session["user_id"])
    if not user:
        session.clear()
        flash("Session expired. Please log in again.", "danger")
        return redirect(url_for("login"))
    return render_template("dashboard.html", user=user)


@app.route("/logout")
@login_required
def logout():
    session.clear()
    flash("You have been logged out successfully.", "success")
    return redirect(url_for("login"))


# Initialize database when app starts
with app.app_context():
    init_db()

if __name__ == "__main__":
    host = os.environ.get("FLASK_RUN_HOST", "127.0.0.1")
    port = int(os.environ.get("FLASK_RUN_PORT", 5001))
    app.run(host=host, port=port, debug=True)
