#!/usr/bin/env python
# coding=utf-8
import schedule
import time
import MySQLdb
import redis

def to_insert(args):
	db = MySQLdb.connect(user= "root",db= "mqtt",passwd= "frappe",host= "192.168.199.162",charset= "utf8")
	cursor = db.cursor()
	sql = "INSERT INTO `send_info` (`content`, `time`, `topic`)VALUES(%s,%s,%s)"
	cursor.executemany(sql,args)
	db.commit()
	cursor.close()
	db.close()

def strtotuple(tableNo,rds):
	msg_list = []
	table_value = rds.get(tableNo).split("*")
	for rv in table_value:
		if len(rv): # 排除空字符串
			msg_list.append(eval(rv)) # string to tuple,放入数组中
	to_insert(tuple(msg_list)) # 批量写入数据,需放入元组格式
	rds.set(tableNo,"",ex=300) # 写入数据后置空,防止重复写入
	print tableNo,rds.get(tableNo)

def job():
	print("I'm working...")
	pool = redis.ConnectionPool(host="127.0.0.1", port=6379, db=1)
	rds = redis.Redis(connection_pool=pool)
	tableNo = rds.get("table00")
	q_table = ""
	if tableNo and rds.get(tableNo): # table01与table02互相切换,避免写入数据库时有消息存入此表
		if tableNo == "table01":
			q_table = "table02"
		else:
			q_table = "table01"
		rds.set(q_table,"",ex=300) # 打开要写入的表
		rds.set("table00",q_table,ex=300) # 修改标志表
		time.sleep(1)
		strtotuple(tableNo,rds)
	else:
		q_table = "table01"
		rds.set(q_table,"",ex=300)
		print "set -- > ",q_table
	rds.set("table00",q_table,ex=300) # table00中存放emq消息应该写入的表

schedule.every(0.1).minutes.do(job)

while True:
	schedule.run_pending()
	time.sleep(6)
