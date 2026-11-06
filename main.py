# AI USTAD - KPK Abbottabad Board - Class 1 to 12
# Private + Sarkari Dono Ke Liye
from flask import Flask, request, jsonify
import json, os
from datetime import datetime

app = Flask(__name__)

# ===== DATABASE (Simple File) =====
DB_FILE = "students.json"
def load_db():
    if os.path.exists(DB_FILE):
        with open(DB_FILE) as f: return json.load(f)
    return {}
def save_db(data):
    with open(DB_FILE, "w") as f: json.dump(data, f, indent=2)

# ===== KPK ABBOTTABAD BOARD SYLLABUS - CLASS 1 TO 12 =====
SYLLABUS = {
    "1": ["Urdu", "English", "Maths", "Islamiat", "Nazra Quran"],
    "2": ["Urdu", "English", "Maths", "Islamiat", "Nazra Quran", "General Science"],
    "3": ["Urdu", "English", "Maths", "Science", "Islamiat", "Social Studies"],
    "4": ["Urdu", "English", "Maths", "Science", "Islamiat", "Social Studies", "Computer"],
    "5": ["Urdu", "English", "Maths", "Science", "Islamiat", "Social Studies", "Computer"],
    "6": ["Urdu", "English", "Maths", "Science", "Islamiat", "Pak Studies", "Computer", "Arabic"],
    "7": ["Urdu", "English", "Maths", "Science", "Islamiat", "Pak Studies", "Computer", "Arabic"],
    "8": ["Urdu", "English", "Maths", "Science", "Islamiat", "Pak Studies", "Computer", "Arabic"],
    "9": ["Urdu", "English", "Maths", "Physics", "Chemistry", "Biology / Computer Science", "Islamiat", "Pak Studies"],
    "10": ["Urdu", "English", "Maths", "Physics", "Chemistry", "Biology / Computer Science", "Islamiat", "Pak Studies"],
    "11": ["Urdu", "English", "Maths / Biology", "Physics", "Chemistry", "Islamiat", "Pak Studies"],
    "12": ["Urdu", "English", "Maths / Biology", "Physics", "Chemistry", "Islamiat", "Pak Studies"],
}

# Sarkari vs Private Fee Structure
FEE_STRUCTURE = {
    "sarkari": {"1-5": 0, "6-8": 0, "9-10": 500, "11-12": 800},
    "private": {"1-5": 1500, "6-8": 2000, "9-10": 3000, "11-12": 4000}
}

def get_fee_range(cls):
    cls = int(cls)
    if cls <= 5: return "1-5"
    if cls <= 8: return "6-8"
    if cls <= 10: return "9-10"
    return "11-12"

def ai_ustad_reply(user_id, msg):
    db = load_db()
    msg_low = msg.lower().strip()
    user = db.get(user_id, {})

    # ===== 1. SALAM / START =====
    if any(x in msg_low for x in ["salam", "hi", "hello", "assalam", "start"]):
        return "Assalam-o-Alaikum! Main AI Ustad hun - Abbottabad KPK Board. 📚\n\nRegistration ke liye aise likhen:\n`Register Ali, Class 4, Private`\nYa\n`Register Fatima, Class 9, Sarkari`"

    # ===== 2. REGISTRATION =====
    if "register" in msg_low:
        try:
            # Format: Register Ali, Class 4, Private
            parts = msg.replace("Register", "").replace("register", "").split(",")
            name = parts[0].strip()
            cls = parts[1].replace("Class", "").replace("class", "").strip()
            school_type = parts[2].strip().lower()  # private / sarkari
            if school_type not in ["private", "sarkari"]:
                school_type = "private"
            fee_range = get_fee_range(cls)
            monthly_fee = FEE_STRUCTURE[school_type][fee_range]
            db[user_id] = {
                "name": name, "class": cls, "school": school_type,
                "fee_total": monthly_fee, "fee_paid": 0, "fee_due": monthly_fee,
                "registered_on": str(datetime.now().date()), "attendance": "Present"
            }
            save_db(db)
            subjects = ", ".join(SYLLABUS.get(cls, []))
            return f"✅ REGISTRATION HO GAYI! Mubarak Ho!\n\n👤 Naam: {name}\n📚 Class: {cls}\n🏫 School: {school_type.title()} (KPK Abbottabad Board)\n💰 Monthly Fee: Rs. {monthly_fee}\n\n📖 {cls} Class ke Subjects:\n{subjects}\n\nAb likhen: `Fee` ya `Report` ya koi sawal!"
        except:
            return "Registration ka tareeka galat hai. Aise likhen:\n`Register Ali, Class 4, Private`"

    # Agar register nahi hai
    if not user:
        return "Pehle Registration karwain! Aise likhen:\n`Register Ali, Class 4, Private`"

    # ===== 3. SYLLABUS =====
    if "syllabus" in msg_low or "subject" in msg_low or "kitab" in msg_low:
        cls = user["class"]
        subjects = "\n- ".join(SYLLABUS.get(cls, []))
        return f"📚 Class {cls} - KPK Abbottabad Board Syllabus:\n- {subjects}\n\nSchool Type: {user['school'].title()}"

    # ===== 4. FEE UPDATE =====
    if "fee" in msg_low or "fees" in msg_low or "paisa" in msg_low:
        # Agar "Fee Paid 1500" likha ho to update karo
        if "paid" in msg_low:
            try:
                amount = int(''.join(filter(str.isdigit, msg)))
                user["fee_paid"] += amount
                user["fee_due"] = user["fee_total"] - user["fee_paid"]
                if user["fee_due"] < 0: user["fee_due"] = 0
                db[user_id] = user; save_db(db)
            except: pass
        return f"💰 FEE UPDATE - {user['name']}\n\nTotal Fee: Rs. {user['fee_total']}\nJama: Rs. {user['fee_paid']}\nBaqaya: Rs. {user['fee_due']}\n\nFee jama karne ke liye likhen:\n`Fee Paid 1500`"

    # ===== 5. DAILY REPORT FOR PARENTS =====
    if "report" in msg_low or "daily" in msg_low or "progress" in msg_low:
        return f"📊 DAILY REPORT - {user['name']} (Class {user['class']})\n\n✅ Attendance: Present\n📖 Aaj ka Kaam: {SYLLABUS[user['class']][0]} + Maths ki Practice\n⭐ Performance: Bohat Achi! MashAllah\n💰 Fee Baqaya: Rs. {user['fee_due']}\n\nKal ka Homework: {SYLLABUS[user['class']][1]} ke 5 Sawal yaad karne hain.\n\n- AI Ustad, Abbottabad"

    # ===== 6. DIMAGH WALI BAAT - GENERAL QUESTIONS =====
    if "maths" in msg_low or "math" in msg_low or "hisab" in msg_low:
        return f"Hisab ka sawal hai {user['name']}? Class {user['class']} ka Maths bohat aasaan hai. Batao kya sawal hai? Jaise 12 x 8 = 96. Apna sawal likho, main step by step samjha dunga!"
    if "english" in msg_low:
        return f"English me kya seekhna hai {user['name']}? Class {user['class']} ki English me Tenses sab se important hain. Batao, kaunsa topic mushkil lag raha hai?"
    if "urdu" in msg_low:
        return f"Urdu to hamari apni zuban hai! Class {user['class']} ki Urdu me Mazmoon aur Kahani sab se mazedar hain. Konsa sabaq parhna hai?"
    if "science" in msg_low or "physics" in msg_low or "chemistry" in msg_low or "bio" in msg_low:
        return f"Science ka sawal? Wah! Class {user['class']} ka Science samajhna bohat zaroori hai. Apna sawal likho, main aasaan Urdu me samjha dunga!"
    if "homework" in msg_low or "kaam" in msg_low:
        return f"Aaj ka Homework (Class {user['class']}):\n1. {SYLLABUS[user['class']][0]} ka Sabaq 2 baar parhna\n2. Maths ke 10 sawal\n3. English ke 5 naye lafz yaad karne hain.\n\nHo jaye to `Report` likh ke bhejo!"

    # Default smart reply
    return f"Samajh gaya {user['name']}! (Class {user['class']})\n\nMain tumhari madad kar sakta hun:\n- `Syllabus` likho - Subjects dekhne ke liye\n- `Fee` likho - Fee dekhne ke liye\n- `Report` likho - Daily Report ke liye\n- Ya apna sawal likho, main Ustad ki tarah samjha dunga!"

@app.route("/")
def home():
    return "AI Ustad Live Hai! Abbottabad KPK Board - Class 1 to 12"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    # WhatsApp / Testing ke liye
    user_id = data.get("from", "test_user")
    msg = data.get("message", "")
    reply = ai_ustad_reply(user_id, msg)
    return jsonify({"reply": reply})

@app.route("/daily-report", methods=["GET"])
def daily_report_all():
    db = load_db()
    reports = []
    for uid, u in db.items():
        reports.append(f"{u['name']} (Class {u['class']}) - Fee Due Rs. {u['fee_due']} - Present")
    return jsonify({"total_students": len(db), "reports": reports})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
