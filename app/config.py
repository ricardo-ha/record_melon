from telegram.ext import Application

BOT_TOKEN = ""
WEBHOOK_URL = ""
OPENAI_API_KEY = ""

# Instancia del bot
TELEGRAM_BOT = Application.builder().token(BOT_TOKEN).build()
#.env/bin/uvicorn main:app --host 0.0.0.0 --port 8000 --reload &

DATABASE_URL = "mysql+mysqlconnector://user:password@localhost:3306/recordmelon"
