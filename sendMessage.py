#!/usr/bin/env python3
#coding:utf-8
'''
# =============================================================================
#      FileName: sendMessage.py
#          Desc: 
#        Author: jianghao
#         Email: mail@jianghao.tech
#      HomePage: http://www.github.com/s-h
#       Version: 0.0.1
#    LastChange: 2020-07-29
#       History:
# =============================================================================
'''
# 不再支持发送消息至企业微信应用
# 支持发送消息至企业微信群组bot
import json
from typing import Dict
import requests
import time
import logging
import re
from optparse import OptionParser
from get_zabbix_img import get_zabbix_img

#logFile = "/tmp/sendMessage.log"
logFile = "sendMessage.log"
logLevel = logging.DEBUG
logging.basicConfig(level=logLevel, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', filename=logFile)
logger = logging.getLogger(__name__)

parser = OptionParser()
#执行动作
parser.add_option("--action", type="string", dest="action", help=" \
    应用发送消息(sendApp)、bot发送消息(sendBot)")
#消息内容
parser.add_option("--content", type="string", dest="content")
#企业微信机器人webhook地址
parser.add_option("--webhookKey", type="string", dest="webhookKey")
(options,args) = parser.parse_args()

def requestURL(url:str, body:Dict=None, n:int=3):
    # 尝试n回访问url
    if n <= 1:
        logger.error("访问'%s'失败" % url)
        raise ConnectionError
    try:
        rs = requests.post(url, body).json()
    except Exception as e:
        logger.warning("连接重试")
        n -= 1
        time.sleep(1)
        requestURL(url, body, n)
    #企业微信返回值不为0则访问错误 
    if rs["errcode"] != 0:
        logger.info(rs["errmsg"])
        raise ConnectionError
    return rs

def sendBootMessage(webhookKey:str, content:str):
    url="https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=" + webhookKey
    values = {
        "msgtype": "markdown",
        "markdown": {
            "content": content
        }
    }
    body=bytes(json.dumps(values, ensure_ascii=False), encoding='utf-8')
    try:
        requestURL(url, body)
    except ConnectionError:
        logger.error("botMessage发送失败")

def sendBootImg(webhookKey:str, img_base64:str, base64_md5:str):
    url="https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=" + webhookKey
    values = {
        "msgtype": "image",
        "image": {
            "base64": str(img_base64),
            "md5": base64_md5
        }
    }
    body=bytes(json.dumps(values, ensure_ascii=False), encoding='utf-8')
    try:
        requestURL(url, body)
    except ConnectionError:
        logger.error("botImg发送失败")

def get_zabbix_itemid(conntent:str):
    results = re.findall('item_id:\s(.*)', conntent)
    print(results)

content = options.content
action = options.action
if action == "sendBot":
    #发送消息到群组机器人
    logger.info("用户动作为sendBot")
    webhookKey = options.webhookKey
    logger.debug("content:%s" % content)
    logger.debug("webhookKey:%s" % webhookKey)
    #发送文字告警消息
    sendBootMessage(webhookKey, content)
    #获取图片
    itemid = get_zabbix_itemid(content)
    logger.info(itemid)
    (img_base64, base64_md5) = get_zabbix_img(itemid)
    logger.info(img_base64)
    logger.info(itemid)
    #发送图片
    sendBootImg(webhookKey, img_base64, base64_md5)

else:
    logger.error("未知动作")
