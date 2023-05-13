import requests
from flask import Blueprint, request, session, jsonify
from sqlalchemy import or_

from data_sheet import User

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
from tool import check_message,short_message,check_Indonesia
from sqlalchemy.sql import and_,asc,desc,or_
import datetime
from tool import get_age
bp = Blueprint("trade", __name__, url_prefix="/trade")

@bp.route("/put_new_transaction")
def put_new_transaction():
    account = request.json.get("account")
    user = session.query(User).filter(or_(User.phone==account, User.email==account)).first()
    birthday  = user.birthday
    if birthday is None:
        return {"code":401,"message":"您未完成实名认证"}
    age = get_age(birthday)
    if age < 18:
        return {"code": 402, "message": "您未成年，不可进行交易"}


