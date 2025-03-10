from .connection import SessionLocal
from .models import ReminderTime, User
from datetime import datetime

def post_user(user_id, time_difference):
    """Guarda un usuario en la base de datos."""
    with SessionLocal() as db:
        new_user = User(telegram_id=user_id, timezone=time_difference)
        db.add(new_user)
        db.commit()


def get_user(user_id):
    """Obtiene un usuario de la base de datos."""
    with SessionLocal() as db:
        user = db.query(User).filter(User.telegram_id == user_id).first()
        if user is None:
            return Exception("User not found")
        return user


def post_reminder(user_id, datetime_, task):
    """Guarda un recordatorio en la base de datos."""
    db = SessionLocal()
    datetime_ = datetime.strptime(f"{datetime_}", "%Y-%m-%d %H:%M")
    new_reminder = ReminderTime(user_id=user_id, datetime=datetime_, task=task)
    db.add(new_reminder)
    db.commit()
    db.close()

def get_reminder(user_id=None):
    """Obtiene el recordatorio de un usuario o de la hora actual.
    Si no se proporciona user_id, obtiene y elimina los recordatorios de la hora actual."""
    now = datetime.now()
    db = SessionLocal()
    if user_id:
        reminder = db.query(ReminderTime).filter(ReminderTime.user_id == user_id).first()
        db.close()
        return reminder
    else:
        users = db.query(ReminderTime).filter(ReminderTime.datetime == now.replace(second=0, microsecond=0)).all()
        #for user in users: #Uncomment this to delete the reminders
        #    db.delete(user)
        #db.commit()
        db.close()
        return users
