# app.py
# This is the main entry point of our Flask web application

import os
from datetime import datetime
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session, jsonify

from utils.database import initialize_database, get_all_food_items, add_food_item
from utils.food_detector import detect_food_item
from utils.date_reader import read_expiry_date
from utils.shelf_life import calculate_estimated_expiry_date
from utils.notifications import get_expiry_status
from utils.recipe_recommender import get_recipe_suggestions
from utils.freshness_score import calculate_freshness_score
from utils.statistics import calculate_statistics
from utils.auth import initialize_users_table, create_user, verify_user
from utils.chatbot import ask_assistant

app = Flask(__name__)
app.secret_key = "expiry-lens-secret-key-change-this-in-production"

UPLOAD_FOLDER = os.path.join("static", "uploads")
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

initialize_database()
initialize_users_table()


def login_required(view_function):
    @wraps(view_function)
    def wrapped_view(*args, **kwargs):
        if "username" not in session:
            return redirect(url_for("login"))
        return view_function(*args, **kwargs)
    return wrapped_view


@app.route("/login", methods=["GET", "POST"])
def login():
    error_message = None

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if verify_user(username, password):
            session["username"] = username
            return redirect(url_for("home"))
        else:
            error_message = "Invalid username or password."

    return render_template("login.html", error_message=error_message)


@app.route("/register", methods=["GET", "POST"])
def register():
    error_message = None

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if create_user(username, password):
            session["username"] = username
            return redirect(url_for("home"))
        else:
            error_message = "That username is already taken."

    return render_template("register.html", error_message=error_message)


@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("login"))


@app.route("/")
@login_required
def home():
    current_username = session.get("username")
    food_items = get_all_food_items(current_username)

    items_with_status = []
    expiring_soon_names = []

    for item in food_items:
        food_name = item[2]
        expiry_date = item[3]
        scan_date = item[4]
        storage_type = item[6]

        status = get_expiry_status(expiry_date)

        freshness_score = calculate_freshness_score(
            food_name=food_name,
            scan_date_str=scan_date,
            expiry_date_str=expiry_date,
            storage_type=storage_type
        )

        items_with_status.append({
            "id": item[0],
            "food_name": food_name,
            "expiry_date": expiry_date,
            "scan_date": scan_date,
            "image_path": item[5],
            "storage_type": storage_type,
            "status_label": status["status_label"],
            "css_class": status["css_class"],
            "freshness_score": freshness_score
        })

        if status["css_class"] in ["status-urgent", "status-warning", "status-expired"]:
            expiring_soon_names.append(food_name)

    recipe_suggestions = get_recipe_suggestions(expiring_soon_names)
    stats = calculate_statistics(items_with_status)

    return render_template(
        "dashboard.html",
        food_items=items_with_status,
        recipe_suggestions=recipe_suggestions,
        stats=stats,
        username=current_username
    )


@app.route("/settings")
@login_required
def settings():
    return render_template("settings.html", username=session.get("username"))


@app.route("/chat", methods=["POST"])
@login_required
def chat():
    data = request.get_json()
    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({"reply": "Please type a question first."})

    # Keep a short conversation history in the session so the assistant 
    # has context, without letting it grow unbounded
    history = session.get("chat_history", [])

    reply = ask_assistant(user_message, conversation_history=history)

    history.append({"role": "user", "content": user_message})
    history.append({"role": "assistant", "content": reply})
    session["chat_history"] = history[-10:]  # keep only the last 10 messages

    return jsonify({"reply": reply})


@app.route("/upload", methods=["POST"])
@login_required
def upload_image():
    current_username = session.get("username")
    uploaded_file = request.files.get("food_image")

    if uploaded_file is None or uploaded_file.filename == "":
        return "No file selected. Please go back and choose an image.", 400

    save_path = os.path.join(app.config["UPLOAD_FOLDER"], uploaded_file.filename)
    uploaded_file.save(save_path)
    print(f"Image saved successfully at: {save_path}")

    print("Running YOLOv8 food detection...")
    food_name, confidence = detect_food_item(save_path)
    print(f"YOLOv8 detected: {food_name} (confidence: {confidence:.2f})")

    print("Running EasyOCR expiry date detection...")
    ocr_expiry_date = read_expiry_date(save_path)
    print(f"EasyOCR result: {ocr_expiry_date}")

    scan_date = datetime.now().strftime("%Y-%m-%d")

    if ocr_expiry_date != "Not Found":
        final_expiry_date = ocr_expiry_date
        print(f"Using OCR-detected expiry date: {final_expiry_date}")
    else:
        final_expiry_date = calculate_estimated_expiry_date(food_name, scan_date)
        print(f"No printed date found - using ESTIMATED expiry date: {final_expiry_date}")

    add_food_item(
        username=current_username,
        food_name=food_name,
        expiry_date=final_expiry_date,
        scan_date=scan_date,
        image_path=save_path,
        storage_type="Room Temperature"
    )

    return redirect(url_for("home"))


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, use_reloader=False, host="0.0.0.0", port=port)
     