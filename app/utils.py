from app.config import OPENAI_API_KEY
from app.database.crud import post_reminder, post_user, get_user

from datetime import datetime, timedelta
import os
import tempfile

from app.models import Reminder

import openai
CLIENT = openai.OpenAI(api_key=OPENAI_API_KEY) 

def help_message():
    return (
        "Hi, I'm a bot that helps you to remember your daily tasks. Here are the commands available:\n"
        "/start - Start the bot\n"
        "/help - Show this help\n"
    )

def welcome_message(username):
    return f"Wellcome {username}!\n\nDo you want to register?\n*Say me /register*"

def register_message(user_id: int, current_user_time: str) -> str:
    try:
        current_user_time = datetime.strptime(current_user_time, "%H:%M").time()
        now = datetime.now().time()
        base_date = datetime.now().date()
        dt_servidor = datetime.combine(base_date, now)
        dt_usuario = datetime.combine(base_date, current_user_time)
        time_difference = dt_servidor - dt_usuario
        time_difference = round(time_difference.total_seconds() / 3600)

        post_user(user_id, str(time_difference))
        return f"User {user_id} registered with a time at {current_user_time}.\n\nYou can start to use the bot now."
    except ValueError:
        return "Invalid time format. Please enter the time in the format HH:MM."
            

def speech_to_text(audio_bytes) -> str:
    file_format = "ogg"
    with tempfile.NamedTemporaryFile(suffix=f".{file_format}", delete=False) as temp_audio:
        temp_audio.write(audio_bytes)
        temp_audio_path = temp_audio.name

    with open(temp_audio_path, "rb") as audio_file:
        response = CLIENT.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            #language="es"  # If you don't specify the language, it will be detected automatically.
        )

    os.remove(temp_audio_path)

    return response.text

def get_remider_from_text(user_id: int, text: str) -> str:
    """Get the reminder from the text."""
    user = get_user(user_id)
    time_difference = user.timezone
    now = datetime.now()
    now = now - timedelta(hours=int(time_difference))
    current_date = now.strftime("%Y-%m-%d")
    current_time = now.strftime("%H:%M")

    prompt = (        
        f"Current date: {current_date}, Current time: {current_time}. "
        "Extract a structured reminder from the user's message."
        "Return only a JSON object with the format: "
        '{"date": "YYYY-MM-DD", "time": "HH:MM", "task": "task description"}. '
        "Convert relative dates (e.g., 'tomorrow', 'next Monday') to absolute dates. "
        "Use 24-hour format for time. If no time is given, default to '09:00'."
        "Example inputs and expected outputs:\n"
        '"Remind me to call John tomorrow at 3 PM" -> {"date": "2025-03-10 15:00", "task": "Call John"}\n'
        '"In 10 minutes, remind me to check the oven" -> {"date": "2025-03-09 14:40", "task": "Check the oven"}\n'
        '"Remind me to submit the report next Monday" -> {"date": "2025-03-11 09:00", "task": "Submit the report"}\n'
        f"User input: {text}\n"
        "Return only the JSON object."
        )
    
    response = CLIENT.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": prompt}],
        temperature=0.0,
        response_format=Reminder,
    )
    response_data = response.choices[0].message.content
    reminder = Reminder.model_validate_json(response_data)
    datetime_ = (datetime.strptime(reminder.datetime_, "%Y-%m-%d %H:%M") + timedelta(hours=int(time_difference))).strftime("%Y-%m-%d %H:%M")

    if reminder.task == "":
        return "Task is required."
    if reminder.datetime_:
        post_reminder(user_id, datetime_, reminder.task)
    else:
        return "I can't understand when you want to be reminded. Please try again."
    
    return f"Reminder created successfully: to {reminder.task} at {reminder.datetime_.split()[1]} on {reminder.datetime_.split()[0]}"






"""This part is for error handling.
It applies a decorator to all functions that are defined in this module.
The decorator is a function that takes a target exception and a message, and returns a decorator that applies the exception to the function.
"""
import types

def handle_error(target_exception, message="An error occurred"): # This is a decorator that applies to all functions in this module.
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except target_exception as e:
                return f"{message}" # : {e}" # Don't expose the original error message. Delete "e" in production.
        return wrapper
    return decorator


for name, obj in list(globals().items()): # This applies the decorator to all functions in this module.
    if isinstance(obj, types.FunctionType) and obj.__module__ == __name__:
        # Apply a customized decorator to each function
        globals()[name] = handle_error(Exception, "Are you registered?")(obj)
