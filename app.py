import os
import json
from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
# کلید مخفی برای امنیت Sessionها (در پروژه‌های واقعی باید پیچیده و مخفی باشد)
app.secret_key = "my_super_secret_dev_key" 
DATA_FILE = "data.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return {"forms": [], "users": []}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

@app.route("/")
def home():
    # بررسی می‌کنیم که آیا کاربری در Session وجود دارد یا نه
    user_email = session.get("user_email")
    # ایمیل کاربر را به قالب HTML می‌فرستیم تا بتوانیم شرط بگذاریم
    return render_template("index.html", user=user_email)

@app.route("/submit-form", methods=["POST"])
def submit_form():
    name = request.form.get("name")
    email = request.form.get("email")
    message = request.form.get("message")
    
    data = load_data()
    data["forms"].append({"name": name, "email": email, "message": message})
    save_data(data)
    
    return redirect(url_for("home"))

@app.route("/signin", methods=["POST"])
def signin():
    email = request.form.get("email")
    password = request.form.get("password")
    action = request.form.get("action") # تشخیص اینکه کاربر می‌خواهد ثبت‌نام کند یا وارد شود

    data = load_data()
    # جستجوی کاربر در لیست کاربران
    user_exists = next((u for u in data["users"] if u["email"] == email), None)

    if action == "register":
        if user_exists:
            return "این ایمیل قبلا ثبت شده است! <a href='/'>بازگشت</a>"
        
        # هش کردن پسورد قبل از ذخیره‌سازی (بسیار مهم)
        hashed_password = generate_password_hash(password)
        data["users"].append({"email": email, "password": hashed_password})
        save_data(data)
        
        # لاگین خودکار بعد از ثبت‌نام
        session["user_email"] = email
        return redirect(url_for("home"))

    elif action == "login":
        # بررسی صحت پسورد با استفاده از تابع check_password_hash
        if user_exists and check_password_hash(user_exists["password"], password):
            session["user_email"] = email
            return redirect(url_for("home"))
        else:
            return "ایمیل یا رمز عبور اشتباه است! <a href='/'>بازگشت</a>"

@app.route("/signout")
def signout():
    # پاک کردن اطلاعات کاربر از Session
    session.pop("user_email", None)
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=False)