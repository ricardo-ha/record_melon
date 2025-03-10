from telegram import Update

from app.utils import help_message, welcome_message, speech_to_text, get_remider_from_text, register_message

#USER_STATES = {} # Dictionary to store user states (It's used to handle the interactive commands)

async def handle_update(update: Update):
    """Handle the update from Telegram."""
    if update.message:
        # Handle voice messages
        if update.message.voice:
            await handle_voice_message(update)
            return

        # Handle text messages
        if update.message.text:
            if update.message.text.startswith("/"):
                await handle_command(update)
            else:
                await handle_message(update)
        else:
            await update.message.reply_text("Unsupported message type.")

async def handle_command(update: Update):
    """Handle the commands from the user."""
    match update.message.text.split()[0]:
        case "/start":
            start_message = welcome_message(update.message.from_user.username)
            await update.message.reply_text(start_message, parse_mode="Markdown")
        case "/help":
            message = help_message()
            await update.message.reply_text(message, parse_mode="Markdown")
        case "/register":
            try:
                message = register_message(update.message.chat_id, update.message.text.split()[1])
                await update.message.reply_text(message, parse_mode="Markdown")
            except Exception as e:
                await update.message.reply_text(f"Usage: /register <your_time>")
        case _:
            await update.message.reply_text("Unsupported command.")

async def handle_voice_message(update: Update):
    """Handle the voice messages from the user."""
    voice_file_id = update.message.voice.file_id
    voice_file = await update.message.get_bot().get_file(voice_file_id)
    audio_bytes = await voice_file.download_as_bytearray()

    text = speech_to_text(audio_bytes)
    message = get_remider_from_text(update.message.chat_id, text)
    await update.message.reply_text(message)

async def handle_message(update: Update):
    """Handle the message from the user."""
    message = get_remider_from_text(update.message.chat_id, update.message.text)
    await update.message.reply_text(message)
