# -*- coding: utf-8 -*-
import json
import threading
import paho.mqtt.client as mqtt
import logging
import logging.handlers
import os
from logging import handlers

server_url = '127.0.0.1'
server_port = 1883
callback_dit = {}
publish_dit = {}
mqttc = None
rc = -1
isPrintLog = False
isPrintDebug = False
isPrintError = True
isPrintInfo = True


def setLogPrint(info=True, error=True, debug=False):
    global isPrintDebug, isPrintError, isPrintInfo
    isPrintInfo = info
    isPrintError = error
    isPrintDebug = debug


def setServerUrl(url='127.0.0.1', port=1883):
    global server_url, server_port
    server_url = url
    server_port = port


def setMqttLog(PrintLog=False):
    global isPrintLog
    isPrintLog = PrintLog


class Dxr_url_port:
    pass


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))


# 一旦订阅到消息，回调此方法
def on_message(_, obj, msg):
    global sub_topic_dit, callback_dit
    topic = msg.topic
    callback_dit[topic](msg.payload)


def callback():
    pass


# 一旦订阅成功，回调此方法
def on_subscribe(mqttc, obj, mid, granted_qos):
    # print("Subscribed: " + str(mid) + " " + str(granted_qos))
    pass


# 一旦有log，回调此方法
def on_log(mqttc, obj, level, string):
    global isPrintLog
    if isPrintLog:
        print(string)


def Mqtt():
    global mqttc, server_url, server_port
    if mqttc is None:
        # 新建mqtt客户端，默认没有clientid，clean_session=True, transport="tcp"
        mqttc = mqtt.Client()
        mqttc.on_message = on_message
        mqttc.on_connect = on_connect
        mqttc.on_subscribe = on_subscribe
        mqttc.on_log = on_log
        # 连接broker，心跳时间为60s
        mqttc.connect(server_url, server_port, 60)
        # 订阅该主题，QoS=0
        threading.Thread(target=mqttc.loop_forever).start()
    return mqttc


class Dxr_Subscriber:
    def __init__(self, topic, callback):
        global callback_dit
        self.mqttc = Mqtt()
        self.mqttc.subscribe(topic)
        self.topic = topic
        self.callback = callback
        callback_dit[topic] = callback


class Dxr_Publisher:
    def __init__(self, topic):
        self.topic = topic
        # 新建mqtt客户端，默认没有clientid，clean_session=True, transport="tcp"
        self.mqttc = Mqtt()

    def publish(self, msg):
        self.mqttc.publish(self.topic, json.dumps(msg), qos=0)


class Dxr_UnSubscriber:
    def __init__(self, topic):
        global callback_dit
        self.topic = topic
        self.mqttc = Mqtt()
        self.mqttc.unsubscribe(self.topic)
        callback_dit.pop(self.topic)


class Logger(object):
    #  日志级别关系映射
    level_relations = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'crit': logging.CRITICAL
    }

    def __init__(self, filename, level='info', when='D', backCount=3,
                 fmt='%(asctime)s line %(lineno)s %(levelname)s: %(message)s'):
        self.logger = logging.getLogger(filename)
        format_str = logging.Formatter(fmt)  # 设置日志格式
        self.logger.setLevel(self.level_relations.get(level))  # 设置日志级别
        th = handlers.TimedRotatingFileHandler(filename=filename, when=when, backupCount=backCount, encoding='utf-8')
        th.setFormatter(format_str)  # 设置文件里写入的格式
        # self.logger.addHandler(sh)  # 把对象加到logger里
        self.logger.addHandler(th)


if not os.path.exists('/log/'):  # 判断是否存在文件夹如果不存在则创建为文件夹
    try:
        os.makedirs(os.path.abspath('.') + log_path)  # makedirs 创建文件时如果路径不存在会创建这个路径
    except Exception as ex:
        print(ex)
        pass

all_log = Logger(os.path.abspath('.') + '/log/all.log', level='info')
err_log = Logger(os.path.abspath('.') + '/log/error.log', level='error')
debug_log = Logger(os.path.abspath('.') + '/log/debug.log', level='debug')


def print_info(*args):
    global isPrintInfo
    try:
        all_log.logger.info(*args)
        if isPrintInfo:
            print(*args)
    except Exception as ex:
        print(ex)


def print_debug(*args):
    global isPrintDebug
    try:
        debug_log.logger.debug(*args)
        if isPrintDebug:
            print(*args)
    except Exception as ex:
        print(ex)


def print_error(*args):
    global isPrintError
    try:
        if isPrintError:
            print(*args)
        all_log.logger.debug(*args)
        err_log.logger.error(*args)
    except Exception as ex:
        print(ex)
