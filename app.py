import os
import json
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
DATA_FILE = "data.json"

# تابع کمکی برای خواندن اطلاعات از فایل JSON
def load_data():
    if not os.path.exists(DATA_FILE):
        # اگر فایل وجود نداشت، یک ساختار اولیه خالی برمی‌گردانیم
        return {"forms": [], "users": []}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

# تابع کمکی برای ذخیره اطلاعات در فایل JSON
def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

@app.route("/")
def home():
    return render_template("index.html")

# روت جدید برای دریافت اطلاعات فرم
@app.route("/submit-form", methods=["POST"])
def submit_form():
    # دریافت اطلاعات از فیلدهای فرم
    name = request.form.get("name")
    email = request.form.get("email")
    message = request.form.get("message")

    # خواندن داده‌های قبلی
    data = load_data()
    
    # اضافه کردن فرم جدید به لیست
    data["forms"].append({
        "name": name,
        "email": email,
        "message": message
    })
    
    # ذخیره در فایل
    save_data(data)

    # بعد از ارسال موفق، کاربر را به صفحه اصلی برمی‌گردانیم
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=False)