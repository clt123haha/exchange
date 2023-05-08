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
from random import randint
import os
from data_sheet import get_sheet,session,User,ShortMessage
from tool import app as tool_bp
from login import app as login_bp
from register import app as regist_bp


app = Flask(__name__)

if __name__ == '__main__':
    get_sheet()

    app.register_blueprint(login_bp)
    app.register_blueprint(tool_bp)
    app.register_blueprint(regist_bp)
    app.run(host='0.0.0.0', debug=True)