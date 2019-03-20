#!/usr/bin/env python
# encoding: utf-8
import sys
from greenlet import greenlet
import paho.mqtt.client as mqtt
import time

msg = {"len":0}
mqttc = mqtt.Client()
mqttc.connect("192.168.199.221", 1883, 60)

def loop(s, glets):
	previous = glets[s - 1]
	next = glets[s + 1]
	if s > 1:
		r = previous.switch(s - 1, glets)
	else:
		r = previous.switch()
	while True:
		msg["len"] = msg["len"] + 1
		print msg
		# time.sleep(0.01)
		mqttc.publish("testtopic",payload="WHello, "+str(msg["len"]),qos=0)
		mqttc.loop_start()
		next.switch(r)
		r = previous.switch()
	next.switch(r)

def mloop(s, glets):
	previous = glets[s - 1]
	r = previous.switch(s - 1, glets)
	while True:
		msg["len"] = msg["len"] + 1
		print msg
		mqttc.publish("testtopic",payload="WHello, "+str(msg["len"]),qos=0)
		mqttc.loop_start()
		r = previous.switch()

def run_benchmark(n, m):
	glets = [greenlet.getcurrent()]
	time1 = time.time()
	for s in xrange(1, n):
		seqn = s
		glets.append(greenlet(loop))
	else:
		seqn = s+1
		glets.append(greenlet(mloop))
	glets[-1].switch(seqn, glets)
	for r in xrange(m-1, -1, -1):
		glets[1].switch(r)
	time2 = time.time()
	print time2-time1

if __name__ == "__main__":
	run_benchmark(int(sys.argv[1]), int(sys.argv[2]))

