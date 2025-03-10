from fastapi import FastAPI, Request
from telegram import Update
from app.telegram_handlers import handle_update
from app.config import TELEGRAM_BOT

def setup_routes(app: FastAPI):
    @app.post("/webhook")
    async def telegram_webhook(request: Request):
        data = await request.json()
        update = Update.de_json(data, TELEGRAM_BOT.bot)
        await handle_update(update)  # Delegar la lógica al manejador de Telegram
        return {"ok": True}
