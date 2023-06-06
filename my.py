import base64
import random
import time
import urllib.parse
import urllib.request
from io import BytesIO
from flask import send_from_directory, make_response
from flask import Flask, request, jsonify,Blueprint,send_file
import requests
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from flask import Flask
from flask_cors import CORS
from random import randint
import os
from data_sheet import get_sheet,session,User,ShortMessage
from tool import bp as tool_bp
from user import bp as user_bp
from trade import bp as trade_bp
from flask import Flask, render_template
from flask_socketio import SocketIO



app = Flask(__name__)
CORS(app, supports_credentials=True)

app.register_blueprint(user_bp,url_prefix='/user')
app.register_blueprint(tool_bp)
app.register_blueprint(trade_bp)
socketio = SocketIO(app)
@socketio.on('connect')
def test_connect(data):
    sid = data["socketid"]
    id = data["userid"]
    user = session.query(User).filter(User.id == id).first()
    user.sid = sid
    session.add(user)
    session.commit()
    emit('connect response', {'data': 'Connected'})


@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')

@socketio.on('getmessage')
def getmessage(data):
    id1 = request.json.get("userid")
    id2 = request.json.get("talkto")
    message = data["message"]
    sid = session.query(User).filter(User.id == id1).first().sid
    emit("getmeaasge", message, room=sid)
    append(id2, id1, message)
    append(id1, id1, message)

if __name__ == '__main__':
    CORS(app, supports_credentials=True)
    get_sheet()
    socketio.run(app, host='0.0.0.0', debug=True)