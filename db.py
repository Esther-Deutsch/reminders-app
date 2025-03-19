from datetime import datetime, time

# מערך של תזכורות
reminders = [
    {"id":1, "todo":"go go sleep", "date": datetime(year=2025,month=6, day=12), "hour": time(hour=16, minute=30), "reRemind": True},
    {"id":2, "todo": "do home work", "date": datetime(year=2025,month=3, day=6), "hour": time(hour=8, minute=00), "reRemind": False},
    {"id":3, "todo": "wake up", "date": datetime(year=2025,month=12, day=25),  "hour": time(hour=10, minute=45), "reRemind": True}
]
