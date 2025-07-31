from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "⏰🐇"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    server_thread = Thread(target=run)
    server_thread.start()
