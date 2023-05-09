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
bp = Blueprint("user", __name__, url_prefix="/user")


#验证手机验证码的登录接口
@bp.route('/login/moblie',methods=['POST'])
def moblie_login():
    indonesia = requests.get("Indonesia")
    message = request.json.get("message")
    phone = request.json.get("phone")
    ischeak = check_Indonesia(indonesia)
    ischeak2 = check_message(phone,message)
    if ischeak == True and ischeak2 == True:
        return {'code':200,'message':'success'}
    if ischeak == False:
        return {'code': 304, 'message': '验证码错误'}
    if ischeak2 == False:
        return {'code': 305, 'message': '手机验证码错误'}

@bp.route('/login/password',methods=['POST'])
def check_password():
    account = request.json.get("account")
    password = request.json.get("password")
    indonesia = request.json.get("Indonesia")
    if account is None or password is None or indonesia is None:
        return {"code":306,"message":"信息不全"}
    ischeak = check_Indonesia(indonesia)
    result = session.query(User).filter(or_(User.phone==account, User.email==account)).first()
    if ischeak == False:
        return {'code': 304, 'message': '验证码错误'}
    if result == None:
        return {'code': 302, 'message': '账号不存在'}
    if result.password != password:
        return {'code': 303, 'message': '密码错误'}
    return {'code':200,'message':'success'}

@bp.route("/register",methods=['POST'])
def register():
    try:
        phone=request.json.get("phone")
        password=request.json.get("password")
        checkpassword=request.json.get("checkpassword")
        indonesia = requests.get("Indonesia")
        ischeak = check_Indonesia(indonesia)
        if password==checkpassword and ischeak == True:
            result=session.query(User).filter(User.phone == phone).first()
            if result is None:
                newuser=User(mailnum=phone,password=password)
                session.add(newuser)  # 添加记录
                session.flush()
                session.commit()
                return jsonify(code=200,message='success')
            return jsonify(code=403,message="该用户已存在")
        return jsonify(code=403,message="两次输入的密码不一致")
    except Exception as e:
       session.rollback()
       return jsonify(code=404,message=f'{e}')

