from flask import Flask, request, make_response
import hashlib
import xml.etree.ElementTree as ET
import logging
import sys

app = Flask(__name__)

# 日志配置
logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger()

# 替换成您的Token、EncodingAESKey和AppID
WECHAT_TOKEN = 'oscar'
WECHAT_AESKEY = 'aALEFhhfFZz7g26WhrsU2HjQWjQkiQgtNqi5NAzWtj8'
WECHAT_APPID = 'wx913eb91e3e41654e'

@app.route('/wechat', methods=['GET', 'POST'])
def wechat():
    if request.method == 'GET':
        # 记录GET请求的参数
        logger.info("Received GET request with params: %s", request.args)

        # 微信认证
        # ... [微信认证逻辑]

        # 记录认证结果
        if hashcode == signature:
            logger.info("Verified GET request successfully.")
            return make_response(echostr)
        else:
            logger.warning("Failed to verify GET request.")
            return ""
    else:
        # 记录POST请求的数据
        logger.info("Received POST request with data: %s", request.data)

        # 处理微信发来的消息
        # ... [消息处理逻辑]

        return "success"

if __name__ == '__main__':
    app.run(debug=True)
