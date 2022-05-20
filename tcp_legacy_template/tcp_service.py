import socket
import sys
import paho.mqtt.client as mqtt
import re
import datetime
import logging
import json
from logging.handlers import TimedRotatingFileHandler

#PLEASE DO NOT EDIT THE FOLLOWING DATA

# format the log entries
formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')
#log rotate
handler = TimedRotatingFileHandler('logs/logfile.log', 
                                   when='midnight',
                                   backupCount=10)
handler.setFormatter(formatter)
logger = logging.getLogger(__name__)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

#DATA EDITABLE FROM HERE DOWNWARD

from threading import Thread

actionList = {}
correlationIdList = {}
#The following are the list of pre-defined message types:
#deviceResponseList, loginMessageList, dataMessageList, heartbeartMessageList & alarmMessageList
#The responsible developer should write an identifier for each of these message types.
#Developer to fill below required details: (e.g. :deviceResponseList = "T3 T4 T7" )
deviceResponseList = " "
loginMessageList = " "
dataMessageList = " "
heartbeartMessageList = " "
alarmMessageList = " "

connection = None

SERVER_HOST = '127.0.0.1' # Add server IP
SERVER_PORT = 5008 # Add server port

broker_address="Add broker address"
user="Add user name listed in developer portal, definition section"
passw="Add password listed in developer portal, definition section"

common_topic="Add common topic listed in developer portal, definition section"
action_topic="Add action topic listed in developer portal, definition section"
action_response_topic="Add action topic listed in developer portal, definition section"

client = mqtt.Client("Add a unique client ID") #create new instance
client.username_pw_set(username=user,password=passw)
#client.on_log=on_log
COMMON_REGEX="^\[[0-9]{4}[-][0-9]{2}[-][0-9]{2}[0-9]{2}[:][0-9]{2}[:][0-9]{2}[,]" #[2011-12-1510:00:00,
LOGIN_MSG_REGEX="[T20]"
HEARTBEAT_REGEX=COMMON_REGEX+"[T14]"
DATA_REGEX=COMMON_REGEX+"T3"
ALARM_REGEX=COMMON_REGEX+"[T8|T9|T10|T11|T12|T13|T15]"
RESPONSE_REGEX=COMMON_REGEX+"[T4|T5|T6|T16]"

def on_log(client, userdata, level, buf):
    logger.info("log: ",buf)
#This method is used to connect to MQTT broker. Upon connection, it will be subscribed to action topic
def on_connect(client, userdata, flags, rc):
	
	logger.info("broker connected")
	client.subscribe(action_topic, qos=0)	
	logger.info("broker subscribed")
	
#This method is used to get messages from core platform
#Once the message is received, it needs to be queued and sent to the device
def on_message(client, userdata, message):
    
    correlationId = str(message.topic).split("/")[0]
    imei = str(message.topic).split("/")[1]
    dt_string = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    actionJson = json.loads(message.payload)
    name = actionJson["actionName"]
    parameters = actionJson['actionParameters']
    action = "["+dt_string+","+name
    if parameters is None:
	    action = action + "]"
	    logger.info("Action parameters are empty")
		
    else:
        #logger.info("Action parameters: ",str(parameters))
        params = ","
        for key, value in parameters.items():
            params += str(value) + ","
			
        params = params[:-1]	# remove last ,    		
        action += params + "]"
    logger.info("Adding Action "+str(action)+" to the queue for send to device")
		
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

#Set message handler	
client.on_message=on_message
#Set connection handler
client.on_connect=on_connect
logger.info("broker connecting")
#Initiate the connection
client.connect(broker_address)
#keep connecting
client.loop_start()

#This method is used to send command to device
def sendData(imei):
    	
    if bool(actionList.get(imei)):
        actionMap = actionList.get(imei)
        if actionMap:
            if connection != None:
                logger.info("connection is availabe")
                action = actionMap.pop(0)
                logger.info(" Sending Command to the device "+imei)
                connection.sendall(action.encode())
            else:
                logger.info("connection is not availabe")
				
#This method used to publish response to the action response topic
def sendDeviceResponse(imei,data):
    
    if bool(correlationIdList.get(imei)):
        responsemap = correlationIdList.get(imei)
        if responsemap:
            correlationId = responsemap.pop(0)
            logger.info("publish device response to broker from the device",imei)
            topic = correlationId+"/"+imei+action_response_topic
            client.publish(topic, data)

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error as msg:
    logger.info("Could not create socket. Error Code: ", str(msg[0]), "Error: ", msg[1])
    sys.exit(0)

logger.info("[-] Socket Created")

#Bind socket
try:
    s.bind((SERVER_HOST, SERVER_PORT))
    logger.info("[-] Socket Bound to port " + str(SERVER_PORT))
except socket.error as msg:
    logger.info("Bind Failed. Error Code: {} Error: {}".format(str(msg[0]), msg[1]))
    sys.exit()

s.listen(10)
logger.info("Listening...")

#Start a new thread for each device
def client_thread(conn):
    global connection
    connection = conn
    sendReply = True
    while True:
        data1 = conn.recv(1024)
        
        data = data1.decode()
        if not data:
            logger.info("Empty data packet Received")
            break
        elif re.match(COMMON_REGEX,data) != None:
            
            imei = "Extract IMEI number from message"
            			
            if loginMessageList.find(type) >= 0:
                
                reply = "set reply you want to send to device"
                logger.info(" Login Packet Received: imei- " + imei)
				
            elif dataMessageList.find(type) >= 0:
                logger.info("Data Packet Received: imei- "+imei)
				#Publish data to the common topic
                client.publish(common_topic, data)
				#Send any actions available in the queue to the device
                sendData(imei)
				
            elif heartbeartMessageList.find(type) >= 0:
                logger.info("Heart Beat Packet Received: imei- "+imei)
				#Publish data to the common topic
                client.publish(common_topic, data)
				#Send any actions available in the queue to the device
                sendData(imei)
				
            elif alarmMessageList.find(type) >= 0:
                logger.info("Alarm Packet Received: imei- "+imei)
				#Publish data to the common topic
                client.publish(common, data)
				#Send any actions available in the queue to the device
                sendData(imei)
				
            elif deviceResponseList.find(type) >= 0:
                logger.info("Action response Received: imei- "+imei)
				#Publish response to the action response topic
                sendDeviceResponse(imei,data)
				#Send any actions available in the queue to the device
                sendData(imei)				
                sendReply = False
            else:
                logger.info("Invalid Packet Received: data- "+data)
                break
		
        if(sendReply == True):
            logger.info("reply "+ reply)
            conn.sendall(reply.encode())
    logger.info("[-] Connection removed ")
    conn.close()
    sys.exit()

while True:
    #Blocking call, await to accept a connection
    conn, addr = s.accept()
    logger.info("[-] Connected to " + addr[0] + ":" + str(addr[1]))
    t = Thread(target=client_thread, args=(conn,))
    t.start()

s.close()

