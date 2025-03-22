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
    hour = db.Column(db.Time, default = datetime.now().time())
    reRemind = db.Column(db.Boolean, default = False)

with app.app_context():
    db.create_all()


# פונקציה שתופעל בעת העליה ותציג את כל התזכורות עם אופציה להוספת תזכורת חדשה
@app.route("/", methods=["GET", "POST"])
def getAll():
    if request.method == "GET":
        data = Reminder.query.filter_by().all()
        return render_template("allReminders.html", reminders= data)
    else:
        to_do = request.form['toDo']
        date_str = request.form['date']
        hour_str = request.form['hour']
        re_remind = True if request.form.get('reRemind') == 'on' else False

        #convert the date and hour to dateTime and time
        #if the date or hour is empty, it will take the current date and time
        date = datetime.strptime(date_str, '%Y-%m-%d') if date_str else datetime.now()
        hour = datetime.strptime(hour_str, '%H:%M').time() if hour_str else datetime.now().time()

        add_reminder = Reminder(todo = to_do, date = date, hour = hour, reRemind = re_remind)
        db.session.add(add_reminder)
        db.session.commit()
        return redirect("/")

# פונקציה למחיקת תזכורת
@app.route("/delete/<int:id>")
def delete(id):
    delete_reminder = Reminder.query.get_or_404(id)
    db.session.delete(delete_reminder)
    db.session.commit()
    return redirect("/")

# פונקציה לעדכון תזכורת
@app.route("/update/<int:id>", methods=["GET", "POST"])
def update(id):
    if request.method == "GET":
        update_reminder = Reminder.query.get_or_404(id)
        return render_template("update.html", remind=update_reminder)
    else:
        
        # התזכורת שנרצה לעדכן
        update_reminder = Reminder.query.get_or_404(id)
        
        # שליפת הנתונים מהטופס
        to_do = request.form['toDo']
        date_str = request.form['date']
        hour_str = request.form['hour']
        re_remind = request.form.get('reRemind') == 'on'

        # המרה של התאריך ושעה אם קיבל
        # במידה ולא קיבל הצבה של התאריך והשעה הישנים        
        date = datetime.strptime(date_str, '%Y-%m-%d') if date_str else update_reminder.date
        hour = datetime.strptime(hour_str, '%H:%M').time() if hour_str else update_reminder.hour
        
        # עדכון התזכורת
        update_reminder.todo = to_do
        update_reminder.date = date
        update_reminder.hour = hour
        update_reminder.reRemind = re_remind
        
        #עדכון בדאטה בייס
        db.session.commit()
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