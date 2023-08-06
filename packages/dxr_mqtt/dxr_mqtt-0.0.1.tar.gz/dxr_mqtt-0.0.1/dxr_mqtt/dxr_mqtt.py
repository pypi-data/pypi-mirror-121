# -*- coding: utf-8 -*-
import json
import threading
import paho.mqtt.client as mqtt

server_url = '127.0.0.1'
server_port = 1883


def setServerUrl(url='127.0.0.1', port=1883):
    global server_url, server_port
    server_url = url
    server_port = port


class Dxr_url_port:
    pass


class Dxr_Subscriber:
    def __init__(self, topic, callback):
        global server_url, server_port
        self.server_url = server_url
        self.server_port = server_port
        self.callback = callback
        self.topic = topic
        # 新建mqtt客户端，默认没有clientid，clean_session=True, transport="tcp"
        self.mqttc = mqtt.Client()
        self.mqttc.on_message = self.on_message
        self.mqttc.on_connect = self.on_connect
        self.mqttc.on_subscribe = self.on_subscribe
        self.mqttc.on_log = self.on_log
        # 连接broker，心跳时间为60s
        self.mqttc.connect(self.server_url, self.server_port, 60)
        # 订阅该主题，QoS=0
        threading.Thread(target=self.mqttc.loop_forever).start()

    def on_connect(self, mqttc, obj, flags, rc):
        # print("rc: " + str(rc))
        if rc == 0:
            subscribe_topic_array = [(self.topic, 0)]
            self.mqttc.subscribe(subscribe_topic_array)

    # 一旦订阅到消息，回调此方法
    def on_message(self, mqttc, obj, msg):
        self.callback(msg.payload)

    def callback(self):
        pass

    # 一旦订阅成功，回调此方法
    def on_subscribe(self, mqttc, obj, mid, granted_qos):
        # print("Subscribed: " + str(mid) + " " + str(granted_qos))
        pass

    # 一旦有log，回调此方法
    def on_log(self, mqttc, obj, level, string):
        # print(string)
        pass


class Dxr_Publisher:
    def __init__(self, topic):
        global server_url, server_port
        self.server_url = server_url
        self.server_port = server_port
        self.topic = topic
        # 新建mqtt客户端，默认没有clientid，clean_session=True, transport="tcp"
        self.mqttc = mqtt.Client()
        self.mqttc.on_message = self.on_message
        self.mqttc.on_connect = self.on_connect
        self.mqttc.on_subscribe = self.on_subscribe
        self.mqttc.on_log = self.on_log
        # 连接broker，心跳时间为60s
        self.mqttc.connect(self.server_url, self.server_port, 60)
        # 订阅该主题，QoS=0
        threading.Thread(target=self.mqttc.loop_forever).start()

    def on_connect(self, mqttc, obj, flags, rc):
        pass

    # 一旦订阅到消息，回调此方法
    def on_message(self, mqttc, obj, msg):
        pass

    def callback(self):
        pass

    # 一旦订阅成功，回调此方法
    def on_subscribe(self, mqttc, obj, mid, granted_qos):
        # print("Subscribed: " + str(mid) + " " + str(granted_qos))
        pass

    # 一旦有log，回调此方法
    def on_log(self, mqttc, obj, level, string):
        # print(string)
        pass

    def publish(self, msg):
        self.mqttc.publish(self.topic, json.dumps(msg), qos=0)
