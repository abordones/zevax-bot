from flask import Flask, request, jsonify
from threading import Thread

app = Flask('')

@app.route('/')
def index():
    return "Webserver is running!"

def run():
    app.run(host='0.0.0.0', port=5000)

def keep_alive():
    server_thread = Thread(target=run)
    server_thread.start()
