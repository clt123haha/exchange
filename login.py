import requests
from flask import Blueprint, request, session, jsonify
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

app = Blueprint("user/login", __name__)

@app.route('/mobile_text',methods=['POST'])
def test():
    phone = request.json.get("phone")
    if phone is None:
        return {'code':201,'message':'请输入手机号码'}
    try:
         indonesia = short_message(phone)
         print(type(indonesia))
    except Exception as e:
        print(e)
        return {'code':202,'meaasge':'发送失败，请稍后再试'}
    try:
        result = session.query(ShortMessage).filter(ShortMessage.phonenumber == phone).first()
        if result is None:
            newMessage = ShortMessage(phonenumber=phone,meaasge="000000",time=str(time.time()))
            session.add(newMessage)
            session.commit()
        else:
            result.meaasge = indonesia
            result.time = str(time.time())
            session.add(result)
            session.commit()
    except Exception as e:
        return {'code':203,'message':'验证码无效'}
    return  {'code':200,'message':'发送成功，短信验证码有效期为十分钟'}

#验证手机验证码的登录接口
@app.route('/moblie',methods=['POST'])
def moblie_login():
    indonesia = requests.get("Indonesia")
    message = request.json.get("message")
    phone = request.json.get("phone")
    ischeak = check_Indonesia(indonesia)
    ischeak2 = check_message(phone,message)
    if ischeak == True and ischeak2 == True:
        return {'code':200,'message':'欢迎回来'}
    if ischeak == False:
        return {'code': 304, 'message': '验证码错误'}
    if ischeak2 == False:
        return {'code': 305, 'message': '手机验证码错误'}
