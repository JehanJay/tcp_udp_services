import socket
import sys
import paho.mqtt.client as mqtt
import re
import datetime
import logging
from logging.handlers import TimedRotatingFileHandler

# format the log entries
formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')

handler = TimedRotatingFileHandler('/logs/logfile.log', 
                                   when='midnight',
                                   backupCount=10)
handler.setFormatter(formatter)
logger = logging.getLogger(__name__)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

from threading import Thread

actionList = {}
correlationIdList = {}
deviceResponseList = "101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 118 119 120 509 511"
connection = None

def sendData(imei):
    currentDT = datetime.datetime.now()
    if bool(actionList.get(imei)):
        actionMap = actionList.get(imei)
        if actionMap:
            action = actionMap.pop(0)
            logger.info(" Sending Command",action," to the device",imei)
            connection.sendall(action.encode())

def sendDeviceResponse(imei,data):
    currentDT = datetime.datetime.now()
    if bool(correlationIdList.get(imei)):
        responsemap = correlationIdList.get(imei)
        if responsemap:
            correlationId = responsemap.pop(0)
            logger.info("publish device response to broker from the device",imei)
            topic = correlationId+"/"+imei+"/avlbilis/vehicletracker/v1/pub"
            client.publish(topic, data)


def on_log(client, userdata, level, buf):
    logger.info("log: ",buf)

def on_connect(client, userdata, flags, rc):
	currentDT = datetime.datetime.now()
	logger.info("rabbit connected")
	client.subscribe("+/+/avlbilis/vehicletracker/v1/sub", qos=0)	
	logger.info("rabbit subscribed")
	
def on_message(client, userdata, message):
    currentDT = datetime.datetime.now()
    action = str(message.payload.decode("utf-8"))
    logger.info("Action Received from Platform",action)
    correlationId = str(message.topic).split("/")[0]
    imei = str(message.topic).split("/")[1]
    if bool(actionList.get(imei)):
        length = len (actionList[imei])
        actionList[imei].append(action)
    else:
        actionList[imei] = []
        actionList[imei].append(action)

        if bool(correlationIdList.get(imei)):
            length = len (correlationIdList[imei])
            correlationIdList[imei].append(correlationId)
        else:
            correlationIdList[imei] = []
            correlationIdList[imei].append(correlationId)
    sendData(imei)

imeiList = "868683027188154 864895031477050 864180034134648"

HOST = '0.0.0.0' # all availabe interfaces
PORT = 5009 # arbitrary non privileged port

broker_address="mqtt.iot.ideamart.io"
user="avlbilis-vehicletracker-v1_1810"
passw="1545024126_1810"
client = mqtt.Client("AVLBILIS-GPS-25032019") #create new instance
client.username_pw_set(username=user,password=passw)
#client.on_log=on_log
client.on_message=on_message
client.on_connect=on_connect
logger.info("rabbit connecting")
client.connect(broker_address)
client.loop_start()
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error as msg:
    logger.info("Could not create socket. Error Code: ", str(msg[0]), "Error: ", msg[1])
    sys.exit(0)

logger.info("[-] Socket Created")

# bind socket
try:
    s.bind((HOST, PORT))
    logger.info("[-] Socket Bound to port " + str(PORT))
except socket.error as msg:
    logger.info("Bind Failed. Error Code: {} Error: {}".format(str(msg[0]), msg[1]))
    sys.exit()

s.listen(10)
logger.info("Listening...")

# The code below is what you're looking for ############

def client_thread(conn):
    #conn.send("Welcome to the Server. Type messages and press enter to send.\n")
    global connection
    connection = conn
    while True:
        data1 = conn.recv(1024)
        currentDT = datetime.datetime.now()
        data = data1.decode()
        if not data:
            break
        elif data.find("##,imei:") >= 0:
            imei = data[8: 23]
            if imeiList.find(imei) >= 0:
                reply = "LOAD"
                logger.info(" Login Packet Received: imei- " + imei)
            else:
                logger.info("Not a packet from white-listed device: imei- "+imei)
                break

        elif re.match("[0-9]{15}", data) != None:
            reply = "ON"
            imei = data[:-1]
            if imeiList.find(imei) >= 0:
                logger.info(" Heart-beat Packet Received: " + imei)
                client.publish("avlbilis/vehicletracker/v1/common", data)
                sendData(imei)
            else:
                logger.info("Not a packet from white-listed device "+imei)
                break

        elif re.match("^[i][m][e][i][:][0-9]{15}", data) != None:

            imei = data[5: 20]
            keyword = str(data).split(",")[1]
            if imeiList.find(imei) >= 0:
                if deviceResponseList.find(keyword) >=0:
                    logger.info("Action response Received: " + data)
                    sendDeviceResponse(imei,data)
                else:
                    logger.info("Data Packet Received: " + data)
                    client.publish("avlbilis/vehicletracker/v1/common", data)
                sendData(imei)
            else:
                logger.info("Not a packet from white-listed device "+imei)
                break
        else:
            logger.info("Invalid Packet Received: " + data)
            break

        conn.sendall(reply.encode())
    logger.info("[-] Connection removed ")
    conn.close()
    sys.exit()

while True:
    # blocking call, waits to accept a connection
    conn, addr = s.accept()
    logger.info("[-] Connected to " + addr[0] + ":" + str(addr[1]))
    t = Thread(target=client_thread, args=(conn,))
    t.start()

s.close()

