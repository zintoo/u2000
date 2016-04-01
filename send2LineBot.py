#!/usr/bin/env python

import socket

def send2LineBotServer(ip, port, message):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(15)
        sock.connect((ip, port))
        sock.send(message)
        response = sock.recv(1024)
    except Exception as exp:
        print("send2LineBotServer()", exp)

send_data="ccadc20b3a4365ee37f6c45150143c203=%s&" % "ข้อความ"
buffer = str(send_data).encode('utf-8')
send2LineBotServer("192.168.99.100", 54321, buffer)
