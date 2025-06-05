from flask import Flask
import threading

app = Flask('')

@app.route('/')
def home():
    return "🤖 Bot is alive and running!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    thread = threading.Thread(target=run)
    thread.start()
