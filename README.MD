# 🍈 Record Melon Bot 🤖

A Telegram bot designed to help you never forget your important tasks. Let Record Melon be your personal reminder assistant!

## 🌟 Features

- ⏰ Set reminders with specific date and time
- 📝 Store custom tasks for each user
- 🔔 Automatic notifications at the exact moment
- 🎯 Simple and friendly interface
- 🔒 Secure data management with SQLAlchemy

## 🛠️ Technologies Used

- **Python** 3.11+ - Main language
- **FastAPI** Framework Web.
- **python-telegram-bot** - Framework for Telegram interaction
- **SQLAlchemy** - ORM for database management
- **OpenAI** - AI



## 🚀 Installation

1. **Clone the repository**
```bash
git clone https://github.com/ricardo-ha/record_melon.git
cd record_melon
```

2. **Create a virtual environment**
```bash
python -m venv .env
source .env/bin/activate  # On Windows use: .env\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**
   - Edit `app/config.py` file in the project root
   - Add your Telegram token:
```python
BOT_TOKEN=your_token_here
WEBHOOK_URL=yourdomain.com #I use a DDNS.
OPENAI_API_KEY=your_api_key_here
DATABASE_URL=you_can_use_any_sql_database #I use MySQL
```

## 🎮 Usage

- **Register** your user and talk with it!

## 🔧 Telegram Bot Setup

1. Start a chat with [@BotFather](https://t.me/botfather) on Telegram
2. Create a new bot using the `/newbot` command
3. Follow BotFather's instructions to set up your bot
4. Copy the API token provided
5. Add the token to your `app/config.py` file

## 🤝 Contributing

Contributions are welcome! If you have any ideas to improve the bot:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/improvement`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/improvement`)
5. Open a Pull Request

## 📝 License

This project is under the MIT License - see the [LICENSE](LICENSE) file for details.

## 💖 Acknowledgments

- To the python-telegram-bot community for their excellent documentation
- To all contributors and users who make this project possible

---
⭐ Don't forget to give a star if you found it useful! ⭐