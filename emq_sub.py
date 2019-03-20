#!/usr/bin/env python
# coding=utf-8
import paho.mqtt.client as mqtt
import time
import redis

def on_connect(client, userdata, flags, rc):
	print("Connected with result code "+str(rc))

def on_message(client, userdata, msg):
	# 写入到redis中
	msg_now = (msg.payload,time.strftime("%Y-%m-%d %H:%M:%S"),msg.topic+"/"+rds.get("table00"))
	rds.append(rds.get("table00"), str(msg_now)+"*")

pool = redis.ConnectionPool(host="127.0.0.1", port=6379, db=1)
# pool.connection_kwargs["db"] = 2 #连接前切换db
rds = redis.Redis(connection_pool=pool)
# rds.connection_pool.connection_kwargs["db"] = 2 #连接后切换db

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set("admin", "public")
client.connect("192.168.199.221", 1883, 60)
client.subscribe("testtopic",qos=0)
client.loop_forever()
