from flask import Flask, request, make_response
import hashlib
import xml.etree.ElementTree as ET
import base64
from Crypto.Cipher import AES
import xmltodict
import json
import time

app = Flask(__name__)

# 替换成您自己的Token和EncodingAESKey
WECHAT_TOKEN = 'oscar'
WECHAT_ENCODING_AES_KEY = 'ekrWcwnkMHXqmAr1TxjfmcS7GeYsqUdGS8WXclTrRxH'
WECHAT_APPID = 'wx913eb91e3e41654e'

class PrpCrypt(object):
    def __init__(self, key):
        self.key = base64.b64decode(key + '=')
        self.mode = AES.MODE_CBC

    def decrypt(self, text):
        cryptor = AES.new(self.key, self.mode, self.key[:16])
        plain_text = cryptor.decrypt(base64.b64decode(text))
        return plain_text.rstrip(b'\0')

def decrypt_msg(msg, timestamp, nonce):
    pc = PrpCrypt(WECHAT_ENCODING_AES_KEY)
    xml_content = pc.decrypt(msg)[20:].decode('utf-8')
    xml_content = xml_content[:xml_content.rindex('>')+1]
    xml_dict = xmltodict.parse(xml_content)
    return xml_dict['xml']

@app.route('/wechat', methods=['GET', 'POST'])
def wechat():
    if request.method == 'GET':
        # 微信认证
        signature = request.args.get('signature')
        timestamp = request.args.get('timestamp')
        nonce = request.args.get('nonce')
        echostr = request.args.get('echostr')

        token = WECHAT_TOKEN
        data = [token, timestamp, nonce]
        data.sort()
        temp = ''.join(data)
        hashcode = hashlib.sha1(temp.encode('utf-8')).hexdigest()
        if hashcode == signature:
            return make_response(echostr)
        else:
            return ""
    else:
        # 处理微信发来的消息
        encrypt_type = request.args.get('encrypt_type')
        msg_signature = request.args.get('msg_signature')
        
        if encrypt_type == 'aes':
            timestamp = request.args.get('timestamp')
            nonce = request.args.get('nonce')
            data = xmltodict.parse(request.data)
            encrypted_msg = data['xml']['Encrypt']

            # 解密消息
            decrypted_msg = decrypt_msg(encrypted_msg, timestamp, nonce)
            msg_type = decrypted_msg['MsgType']
            from_user = decrypted_msg['FromUserName']
            to_user = decrypted_msg['ToUserName']

            if msg_type == "text":
                reply_text = "您发送了文本消息"
                reply_xml = f"""
                <xml>
                <ToUserName><![CDATA[{from_user}]]></ToUserName>
                <FromUserName><![CDATA[{to_user}]]></FromUserName>
                <CreateTime>{int(time.time())}</CreateTime>
                <MsgType><![CDATA[text]]></MsgType>
                <Content><![CDATA[{reply_text}]]></Content>
                </xml>
                """
                return reply_xml
            else:
                return "success"
        else:
            return "success"

if __name__ == '__main__':
    app.run(debug=True)

