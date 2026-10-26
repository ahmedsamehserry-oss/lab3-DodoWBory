"""Lab 3 — Lab 2 login/to-dos extended with a books & authors library."""
import os
from decimal import Decimal, InvalidOperation
from functools import wraps
from io import BytesIO
from pathlib import Path
from uuid import uuid4

import bcrypt
import pymysql
from dotenv import load_dotenv
from PIL import Image, UnidentifiedImageError
from flask import Flask, flash, redirect, render_template, request, session, url_for
from pymysql.cursors import DictCursor

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "")
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    MAX_CONTENT_LENGTH=4 * 1024 * 1024,  # 4 MB request cap for photos
)
UPLOAD_ROOT = Path(app.static_folder) / "uploads"


def connection(database=None):
    return pymysql.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=database or os.getenv("DB_NAME", "registration"),
        charset="utf8mb4",
        cursorclass=DictCursor,
        autocommit=True,
    )


def query(sql, values=(), one=False, all_rows=False, database=None):
    # Values are always supplied separately, never interpolated into SQL.
    with connection(database=database) as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, values)
            if one:
                return cursor.fetchone()
            if all_rows:
                return cursor.fetchall()
            return cursor.rowcount


def library_query(sql, values=(), one=False, all_rows=False):
    return query(sql, values, one=one, all_rows=all_rows,
                 database=os.getenv("LIBRARY_DB_NAME", "library"))


def login_required(fn):
    @wraps(fn)
    def inner(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))
        return fn(*args, **kwargs)
    return inner


@app.context_processor
def csrf_context():
    # All mutations require a unique CSRF token stored in the session.
    import secrets
    if "csrf_token" not in session:
        session["csrf_token"] = secrets.token_urlsafe(32)
    return {"csrf_token": session["csrf_token"]}


@app.before_request
def protect_post():
    if request.method == "POST":
        import hmac
        expected = session.get("csrf_token", "")
        supplied = request.form.get("csrf_token", "")
        if not expected or not hmac.compare_digest(expected, supplied):
            return "Invalid form token. Refresh the page and try again.", 400


@app.route("/")
def home():
    return redirect(url_for("todos" if "user_id" in session else "login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    errors = []
    values = {"name": "", "email": ""}
    if request.method == "POST":
        values = {"name": request.form.get("name", "").strip(),
                  "email": request.form.get("email", "").strip()}
        password = request.form.get("password", "")
        confirm = request.form.get("confirm_password", "")
        if not values["name"]:
            errors.append("Name is required")
        if not values["email"]:
            errors.append("Email is required")
        if not password:
            errors.append("Password is required")
        if not confirm:
            errors.append("Confirm password is required")
        if password and confirm and password != confirm:
            errors.append("Passwords do not match")
        if len(values["name"]) > 100 or len(values["email"]) > 255:
            errors.append("Name or email is too long")
        if not errors:
            hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
            try:
                query("INSERT INTO users (email, name, password_hash) VALUES (%s, %s, %s)",
                      (values["email"], values["name"], hashed))
            except pymysql.err.IntegrityError as exc:
                if exc.args[0] == 1062:
                    errors.append("Email Already Exists")
                else:
                    raise
            if not errors:
                # Lab 3 demo: register -> login -> to-do list
                session.clear()
                flash("Account created. Please log in.", "success")
                return redirect(url_for("login"))
    return render_template("register.html", errors=errors, values=values)


@app.route("/login", methods=["GET", "POST"])
def login():
    errors = []
    email = ""
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        if not email:
            errors.append("Email is required")
        if not password:
            errors.append("Password is required")
        if not errors:
            user = query("SELECT user_id, name, password_hash FROM users WHERE email = %s", (email,), one=True)
            if not user or not bcrypt.checkpw(password.encode("utf-8"), user["password_hash"].encode("utf-8")):
                errors.append("Invalid email or password")
            else:
                session.clear()
                session["user_id"] = user["user_id"]
                session["name"] = user["name"]
                return redirect(url_for("todos"))
    return render_template("login.html", errors=errors, email=email)


@app.post("/logout")
@login_required
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.get("/todos")
@login_required
def todos():
    items = query("SELECT todo_id, title, is_done, created_at FROM todos WHERE user_id = %s ORDER BY todo_id DESC",
                  (session["user_id"],), all_rows=True)
    done_tasks = sum(1 for item in items if item["is_done"])
    open_tasks = len(items) - done_tasks
    return render_template("todos.html", items=items, done_tasks=done_tasks,
                           open_tasks=open_tasks)


def valid_title(title):
    if not title.strip():
        return "Title is required"
    if len(title.strip()) > 200:
        return "Title is too long"
    return None


@app.post("/todos/add")
@login_required
def add_todo():
    title = request.form.get("title", "")
    error = valid_title(title)
    if error:
        flash(error, "error")
    else:
        query("INSERT INTO todos (user_id, title) VALUES (%s, %s)", (session["user_id"], title.strip()))
        flash("Task added", "success")
    return redirect(url_for("todos"))


@app.post("/todos/<int:todo_id>/edit")
@login_required
def edit_todo(todo_id):
    title = request.form.get("title", "")
    error = valid_title(title)
    if error:
        flash(error, "error")
    else:
        query("UPDATE todos SET title = %s WHERE todo_id = %s AND user_id = %s",
              (title.strip(), todo_id, session["user_id"]))
        flash("Task updated", "success")
    return redirect(url_for("todos"))


@app.post("/todos/<int:todo_id>/toggle")
@login_required
def toggle_todo(todo_id):
    done = request.form.get("is_done", "0")
    if done not in ("0", "1"):
        return "Invalid status", 400
    query("UPDATE todos SET is_done = %s WHERE todo_id = %s AND user_id = %s",
          (int(done), todo_id, session["user_id"]))
    return redirect(url_for("todos"))


@app.post("/todos/<int:todo_id>/delete")
@login_required
def delete_todo(todo_id):
    query("DELETE FROM todos WHERE todo_id = %s AND user_id = %s", (todo_id, session["user_id"]))
    flash("Task deleted", "success")
    return redirect(url_for("todos"))


# ---------- Lab 3: Author / Book CRUD + bonus image uploads ----------

def save_optional_image(field_name, folder):
    """Validate and re-encode an uploaded image; store only a generated filename.

    Returns None when no new image was selected. ValueError for invalid uploads.
    """
    upload = request.files.get(field_name)
    if upload is None or not upload.filename:
        return None
    raw = upload.read()
    if not raw or len(raw) > 3 * 1024 * 1024:
        raise ValueError("Image must be nonempty and no larger than 3 MB")
    try:
        with Image.open(BytesIO(raw)) as image:
            if image.format not in ("JPEG", "PNG", "WEBP", "GIF"):
                raise ValueError("Use a JPG, PNG, WEBP, or GIF image")
            if image.width > 5000 or image.height > 5000:
                raise ValueError("Image dimensions are too large")
            image.load()
            image = image.convert("RGB")
            image.thumbnail((1200, 1200))
            filename = uuid4().hex + ".webp"
            target = UPLOAD_ROOT / folder
            target.mkdir(parents=True, exist_ok=True)
            image.save(target / filename, format="WEBP", quality=85)
            return filename
    except (UnidentifiedImageError, OSError, ValueError, Image.DecompressionBombError) as exc:
        raise ValueError("Please upload a valid JPG, PNG, WEBP, or GIF image") from exc


def delete_uploaded_image(filename, folder):
    """Delete only our own generated filenames from the expected upload folder."""
    import re
    if filename and re.fullmatch(r"[0-9a-f]{32}\.webp", filename):
        (UPLOAD_ROOT / folder / filename).unlink(missing_ok=True)


def author_inputs():
    name = request.form.get("name", "").strip()
    country = request.form.get("country", "").strip()
    if not name or not country or len(name) > 100 or len(country) > 80:
        raise ValueError("Author name and country are required (max 100/80 characters)")
    return name, country


def book_inputs():
    title = request.form.get("title", "").strip()
    value = request.form.get("price", "").strip()
    if not title or len(title) > 150:
        raise ValueError("Book title is required (max 150 characters)")
    try:
        price = Decimal(value)
        if not price.is_finite() or price < 0 or price > Decimal("99999999.99") or price != price.quantize(Decimal("0.01")):
            raise ValueError()
    except (InvalidOperation, ValueError):
        raise ValueError("Enter a valid price with up to 2 decimal places") from None
    try:
        author_id = int(request.form.get("author_id", ""))
    except ValueError:
        raise ValueError("Choose an author") from None
    if not library_query("SELECT author_id FROM AUTHOR WHERE author_id = %s", (author_id,), one=True):
        raise ValueError("The selected author does not exist")
    return title, price, author_id


@app.get("/library")
@login_required
def library():
    authors = library_query("SELECT author_id, name, country, photo_filename FROM AUTHOR ORDER BY author_id", all_rows=True)
    books = library_query("SELECT book_id, title, price, author_id, cover_filename FROM BOOK ORDER BY book_id", all_rows=True)
    author_map = {author["author_id"]: author["name"] for author in authors}
    return render_template("library.html", authors=authors, books=books, author_map=author_map)


@app.post("/library/authors/add")
@login_required
def add_author():
    image = None
    try:
        name, country = author_inputs()
        image = save_optional_image("photo", "authors")
        library_query("INSERT INTO AUTHOR (name, country, photo_filename) VALUES (%s, %s, %s)",
                      (name, country, image))
        flash("Author added", "success")
    except (ValueError, pymysql.MySQLError) as exc:
        delete_uploaded_image(image, "authors")
        flash(f"Could not add author: {exc}", "error")
    return redirect(url_for("library"))


@app.post("/library/authors/<int:author_id>/edit")
@login_required
def edit_author(author_id):
    old = library_query("SELECT photo_filename FROM AUTHOR WHERE author_id = %s", (author_id,), one=True)
    if not old:
        flash("Author not found", "error")
        return redirect(url_for("library"))
    image = None
    try:
        name, country = author_inputs()
        image = save_optional_image("photo", "authors")
        new_image = image if image else old["photo_filename"]
        library_query("UPDATE AUTHOR SET name = %s, country = %s, photo_filename = %s WHERE author_id = %s",
                      (name, country, new_image, author_id))
        if image:
            delete_uploaded_image(old["photo_filename"], "authors")
        flash("Author updated", "success")
    except (ValueError, pymysql.MySQLError) as exc:
        delete_uploaded_image(image, "authors")
        flash(f"Could not edit author: {exc}", "error")
    return redirect(url_for("library"))


@app.post("/library/authors/<int:author_id>/delete")
@login_required
def delete_author(author_id):
    author = library_query("SELECT photo_filename FROM AUTHOR WHERE author_id = %s", (author_id,), one=True)
    if not author:
        flash("Author not found", "error")
        return redirect(url_for("library"))
    # Collect images of books that ON DELETE CASCADE will remove.
    books = library_query("SELECT cover_filename FROM BOOK WHERE author_id = %s", (author_id,), all_rows=True)
    library_query("DELETE FROM AUTHOR WHERE author_id = %s", (author_id,))
    delete_uploaded_image(author["photo_filename"], "authors")
    for book in books:
        delete_uploaded_image(book["cover_filename"], "books")
    flash("Author and their books deleted (ON DELETE CASCADE)", "success")
    return redirect(url_for("library"))


@app.post("/library/books/add")
@login_required
def add_book():
    image = None
    try:
        title, price, author_id = book_inputs()
        image = save_optional_image("cover", "books")
        library_query("INSERT INTO BOOK (title, price, author_id, cover_filename) VALUES (%s, %s, %s, %s)",
                      (title, price, author_id, image))
        flash("Book added", "success")
    except (ValueError, pymysql.MySQLError) as exc:
        delete_uploaded_image(image, "books")
        flash(f"Could not add book: {exc}", "error")
    return redirect(url_for("library"))


@app.post("/library/books/<int:book_id>/edit")
@login_required
def edit_book(book_id):
    old = library_query("SELECT cover_filename FROM BOOK WHERE book_id = %s", (book_id,), one=True)
    if not old:
        flash("Book not found", "error")
        return redirect(url_for("library"))
    image = None
    try:
        title, price, author_id = book_inputs()
        image = save_optional_image("cover", "books")
        new_image = image if image else old["cover_filename"]
        library_query("UPDATE BOOK SET title = %s, price = %s, author_id = %s, cover_filename = %s WHERE book_id = %s",
                      (title, price, author_id, new_image, book_id))
        if image:
            delete_uploaded_image(old["cover_filename"], "books")
        flash("Book updated", "success")
    except (ValueError, pymysql.MySQLError) as exc:
        delete_uploaded_image(image, "books")
        flash(f"Could not edit book: {exc}", "error")
    return redirect(url_for("library"))


@app.post("/library/books/<int:book_id>/delete")
@login_required
def delete_book(book_id):
    book = library_query("SELECT cover_filename FROM BOOK WHERE book_id = %s", (book_id,), one=True)
    if not book:
        flash("Book not found", "error")
        return redirect(url_for("library"))
    library_query("DELETE FROM BOOK WHERE book_id = %s", (book_id,))
    delete_uploaded_image(book["cover_filename"], "books")
    flash("Book deleted", "success")
    return redirect(url_for("library"))


@app.errorhandler(413)
def image_too_large(_):
    flash("Image upload is too large (max 3 MB per image)", "error")
    return redirect(url_for("library" if "user_id" in session else "login"))


if __name__ == "__main__":
    if not app.secret_key:
        raise RuntimeError("Set SECRET_KEY in your .env file before running the server")
    app.run(debug=False)
