import requests
import sqlalchemy
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
from data_sheet import get_sheet,session,User,ShortMessage,Transaction
from tool import check_message,short_message,check_Indonesia
from sqlalchemy.sql import and_,asc,desc,or_
import datetime
from tool import get_age
bp = Blueprint("trade", __name__, url_prefix="/trade")

@bp.route("/put_new_transaction",methods=["POST"])
def put_new_transaction():
    user_id= request.json.get("user_id")
    price = request.json.get("price")
    channel = request.json.get("channel")
    login_method = request.json.get("login_method")
    message = request.json.get("message")
    system = request.json.get("system")
    addiction = request.json.get("addiction")
    user = session.query(User).filter(User.id == user_id).first()
    birthday  = user.birthday
    if birthday is None:
        return {"code":401,"message":"您未完成实名认证"}
    age = get_age(birthday)
    if age < 18:
        return {"code": 402, "message": "您未成年，不可进行交易"}
    save_path = r"E:\trade\account"
    if not os.path.exists(save_path):  # 检测目录是否存在，不在则创建
        os.makedirs(save_path)
    try:
        newTransaction = Transaction(price = price,addiction = addiction,channel = channel,login_method = login_method,seller = user_id,system = system,approved = False)
        session.add(newTransaction)
        session.commit()
        tradtionId = session.query(Transaction).first().id
        f = open(save_path + '\\' + str(tradtionId) + ".txt", 'w')
        f.write(message)
    except Exception as e:
        print(e)
        return {"code": 307, "message": "信息储存失败，请稍后再试"}
    return {"code":200,"message":"success"}

@bp.route("/get_transaction")
def get_transaction():
    id= request.json.get("id")
    result = session.query(Transaction).filter(Transaction.id == id).first()
    if result is None:
        return {"code":302,"message":"这条商品信息不存在"}
    price = result.price
    channel = result.channel
    login_method = result.login_method
    system = result.system
    addiction = result.addiction
    message = ""
    try:
        file_path = r'E:\trade\account' + '\\' + str(id) + ".txt"
        if not os.path.exists(file_path):  # 检测目录是否存在，不在则创建
            return {'code': 302, 'message': '简历不存在'}
        f = open(file_path, 'r')
        for line in f:
            message += line
        data = {"price": price, "channel": channel, "login_method": login_method, "message": message, "system": system,
            "addiction": addiction, "seller": result.seller}
    except Exception as e:
        print(e)
        return {"code": 307, "message": "信息储存失败，请稍后再试"}
    return {"code":200,"message":"success","data":data}




