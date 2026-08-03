import threading
from app import app
from bot import bot

def run_flask():
    app.run(host='0.0.0.0', port=5000)

def run_bot():
    bot.infinity_polling()

if name == 'main':
    t1 = threading.Thread(target=run_flask)
    t2 = threading.Thread(target=run_bot)
    t1.start()
    t2.start()
    t1.join()
    t2.join()