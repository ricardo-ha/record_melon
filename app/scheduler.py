from apscheduler.schedulers.background import BackgroundScheduler
import asyncio

from app.database.crud import get_reminder
from app.config import TELEGRAM_BOT

async def send_reminder_message(chat_id, task):
    """Envía un mensaje a un usuario específico."""
    await TELEGRAM_BOT.bot.send_message(chat_id=chat_id, text=task)

def send_reminders():
    """Consulta la base de datos y envía recordatorios a los usuarios."""
    users = get_reminder()
    
    if not users:
        return  # No hay usuarios para enviar recordatorios

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    tasks = [send_reminder_message(user.user_id, user.task) for user in users]
    loop.run_until_complete(asyncio.gather(*tasks))

    loop.close()

# Configurar el scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(send_reminders, "cron", minute="*")  # Ejecuta cada minuto
#scheduler.start()