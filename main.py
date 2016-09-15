#!/usr/bin/env python

from flask import Flask
import os
import socket
import json
import MySQLdb

app = Flask(__name__)
ports = [22, 443, 4443, 8080]

@app.route('/internal')
def ip():
    ips = os.environ['CF_INTERNAL_IPS'].split(',')
    instance_ip = os.environ['CF_INSTANCE_IP']

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)

    for ip in ips:
        for port in ports:
            result = s.connect_ex((ip, port))
            if result == 0:
                return "IP {}:{} could be access by {}".format(ip, port, instance_ip)
    s.close()
    return "CF internal IP addresses could not be reached."

@app.route('/mysql')
def mysql_conn():
    services = json.loads(os.environ['VCAP_SERVICES'])
    s = services['p-mysql'][0]['credentials']

    conn = MySQLdb.connect(s['hostname'], s['username'], s['password'], s['name'])
    with conn:
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS Python;")
        cursor.execute("CREATE TABLE Python(Id INT PRIMARY KEY AUTO_INCREMENT);")
        cursor.execute("DROP TABLE Python;")
    return 'connection is ok'

@app.route('/')
def hello():
    return "Hola"

if __name__ == '__main__':
  app.run('0.0.0.0', os.environ['PORT'])
