from fastapi import FastAPI
from app.webhook import setup_routes
from contextlib import asynccontextmanager
from app.config import TELEGRAM_BOT, WEBHOOK_URL

from app.scheduler import scheduler

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Configurar el webhook al iniciar el servidor
    await TELEGRAM_BOT.bot.set_webhook(WEBHOOK_URL)
    print("Webhook configurado correctamente")

    scheduler.start()
    print("Scheduler started")

    yield  # Pausa mientras el servidor está activo

    # Eliminar el webhook al cerrar el servidor
    #await TELEGRAM_BOT.bot.delete_webhook()
    print("Webhook eliminado correctamente")

    scheduler.shutdown()
    print("Scheduler stopped")

app = FastAPI(lifespan=lifespan)

# Registrar las rutas del webhook
setup_routes(app)
