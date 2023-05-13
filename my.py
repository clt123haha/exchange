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




app = Flask(__name__)
CORS(app, supports_credentials=True)

app.register_blueprint(user_bp,url_prefix='/user')
app.register_blueprint(tool_bp)



if __name__ == '__main__':
    get_sheet()
    app.run(host='0.0.0.0', debug=True)