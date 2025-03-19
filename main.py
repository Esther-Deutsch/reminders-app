from email.policy import default

from flask import Flask, render_template, request
from db import reminders
from sqlalchemy import Nullable
from werkzeug.utils import redirect
# יבוא מודול בשביל להתעסק עם תאריך ושעה
from datetime import datetime, time
# יבוא המודול שנוכל לעבוד עם דאטה בייס
from flask_sqlalchemy import SQLAlchemy


# יצירת אובייקט חכם ליצירת שרת
app = Flask(__name__)
# הגדרה בשביל יצירת הדאטה בייס
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///reminders.db"
#
db = SQLAlchemy(app)

# יצירת טבלה בדאטה בייס
class Reminder(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    todo = db.Column(db.String)#, Nullable = False)
    date = db.Column(db.DateTime, default = datetime.now())
    hour = db.Column(db.Integer, default = datetime.now().time())
    reRemind = db.Column(db.Boolean, default = False)

with app.app_context():
    db.create_all()


# פונקציה שתופעל בעת העליה ותציג את כל התזכורות עם אופציה להוספת תזכורת חדשה
@app.route("/", methods=["GET", "POST"])
def getAll():
    if request.method == "GET":
        return render_template("allReminders.html", reminders= reminders)
    else:
        to_do = request.form['toDo']
        date_str = request.form['date']
        hour_str = request.form['hour']
        re_remind = True if request.form.get('reRemind') == 'on' else False

        #convert the date and hour to dateTime and time
        date = datetime.strptime(date_str, '%Y-%m-%d')
        hour = datetime.strptime(hour_str, '%H:%M').time()

        new_reminder = {"id": reminders[-1]["id"]+1, "todo": to_do, "date": date, "hour": hour, "reRemind": re_remind}
        reminders.append(new_reminder)
        return redirect("/")

# פונקציה למחיקת תזכורת
@app.route("/delete/<int:id>")
def delete(id):
    for r in reminders:
        if r["id"] == id:
            reminders.remove(r)
            break
    return redirect("/")

# פונקציה לעדכון תזכורת
@app.route("/update/<int:id>", methods=["GET", "POST"])
def update(id):
    if request.method == "GET":
        for r in reminders:
            if r["id"] == id:
                reminder = r
                break
        return render_template("update.html", remind=reminder)
    else:
        to_do = request.form['toDo']
        date_str = request.form['date']
        hour_str = request.form['hour']
        re_remind = True if request.form.get('reRemind') == 'on' else False

        # convert the date and hour to dateTime and time
        date = datetime.strptime(date_str, '%Y-%m-%d')
        hour = datetime.strptime(hour_str, '%H:%M').time()
        for r in reminders:
            if r["id"] == id:
                r["todo"] = to_do
                r["date"] = date
                r["hour"] = hour
                r["reRemind"] = re_remind
        return redirect("/")

# מחזיר תזכורת לפי id שמקבל בניתוב
@app.get("/getReminder/<int:id>")
def get_by_id(id):
    # for r in reminders:
    #     if r["id"] == id:
    #         return  r;
    # return f"not found 404"
    return render_template("singleReminder.html")


# מחזיר דף שגיאה לניתוב לא נכון
@app.get("/*")
def error_404():
    return render_template("notFound.html")

# הרצת התוכנית אם תנאי
if __name__ == "__main__":
    app.run(debug=True)