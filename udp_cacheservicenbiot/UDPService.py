import socket
import os
import time
import threading
import subprocess
import logging
import sys
import paho.mqtt.client as mqtt
from logging.handlers import TimedRotatingFileHandler

formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')
handler = TimedRotatingFileHandler('logs/logfile.log', 
                                   when='midnight',
                                   backupCount=10)
handler.setFormatter(formatter)
logger = logging.getLogger(__name__)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


def on_connect(client, userdata, flags, rc):
    client.subscribe("+/+/laison/watermeter/v2/sub")

def on_message(client, userdata, message):
    actionplug = str(message.payload.decode("utf-8"))
    headers1 = actionplug.split(' ')
    number = headers1[0]
    actionplug = headers1[1]
    logger.info("Meter number : "+ str(number)+" Action content received : "+ str(actionplug)) 
    res = subprocess.check_output(["mono","Laison.dll",number,actionplug])
    for line in res.splitlines():
        resultrec = line.decode("utf-8")

    def fetch_file(number):
        logger.info('Received action frame from Laison.dll: '+ str(resultrec)+' for Meter number:'+str(number))
        save_in_cache(number, resultrec)
        return None

    def save_in_cache(number, content):
        logger.info('Saving the action frame for the {} in the cache'.format(str(number)))
        path = os.path.join(os.path.expanduser('~'), 'cacheNBIOT')
        cached_file = open("cacheNBIOT/cache" + number, 'w')
        cached_file.write(content)
        cached_file.close()
        logger.info("Action frame saved successfully for Meter:"+str(number))

    fetch_file(number)

def packet_validator(k):
    validateSplit = k.split(' ')
    checksumValidate = validateSplit[-2]
    requiredHex = validateSplit[4:-2]
    requiredTest = ' '.join(requiredHex)
    testCheck = bytes.fromhex(requiredTest)
    resultCheck = hex(sum(testCheck) % 256)
    calcChecksum = resultCheck.rstrip("L").lstrip("0x").upper() or "0"
    validCheck = calcChecksum.zfill(2)
    calcChecksum = validCheck
    if checksumValidate.lower() == calcChecksum.lower():
        return True
    else:
        return False


broker_address="mqtt.iot.ideamart.io"
user="laison-watermeter-v2_3963"
passw="1582533639_3963"
client = mqtt.Client("LAISON-WATERMETER_1")
client.username_pw_set(username=user,password=passw)
client.on_connect=on_connect
client.on_message=on_message
client.connect(broker_address)
client.loop_start()
topicPub = "laison/watermeter/v2/common"
topicSub = "+/+/laison/watermeter/v2/sub"

class Broker():


    def __init__(self):
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        ip = '0.0.0.0'
        port = 1121
        address = (ip,port)
        try:
            self.sock.bind(address)
            logger.info("[-] Socket bound to port " + str(port))
        except socket.error as msg:
            logger.info("Bind failed. Error code: {} Error: {}".format(str(msg[0]), msg[1]))
            sys.exit()
        self.addr_list = []
        logger.info ("[-] Started listening " + str(ip)+":"+str(port))



    def talkToClient(self, ip, out, hex_content, content, hex_test_res, test_res, filename, topicPub):
        if(out =="90" and content != ""):
            self.sock.sendto(hex_test_res,ip)
            logger.info("[-] Response sent to the client :" + str(ip) + ": {"+str(test_res)+"} for Meter number: "+str(filename))
            time.sleep(1)
            self.sock.sendto(hex_content,ip)
            logger.info("[-] Actuating frame sent to the client :" + str(ip)+ ": {"+str(content)+"} for Meter number: "+str(filename))
        elif(out  =="fe"):
            logger.info("Actuation reply response packet received for Meter number: "+str(filename))
            contsplit = content.split(' ')
            contvalve1 = contsplit[23]
            contvalve2 = contsplit[24]

            if (contvalve1 == "A7" and contvalve2 == "83"):
                actRes = "Opened"
                resPub = "ACK "+filename+"," + actRes
                client.publish(topicPub,resPub)
                logger.info("Meter number: "+str(filename)+" actuated response published to RabbitMQ: "+str(actRes))
            elif (contvalve1 == "67" and contvalve2 == "93"):
                actRes = "Closed"
                resPub = "ACK "+filename+"," + actRes
                client.publish(topicPub,resPub)
                logger.info("Meter number: "+str(filename)+" actuated response published to RabbitMQ: "+str(actRes))
            else:
                actRes = "ControlValveCommandError"
                resPub = "ACK "+filename+"," + actRes
                client.publish(topicPub,resPub)
                logger.info("Meter number: "+str(filename)+" error published to RabbitMQ: "+str(actRes))


            if os.path.exists("cacheNBIOT/cache"+filename):   
                os.remove("cacheNBIOT/cache"+filename)  
                logger.info("Action cache deleted for Meter number: "+str(filename))
            else:  
                pass  
        elif(out =="90" and content == ""):
            logger.info("No cache actions and no response sent for Meter number: "+str(filename))
    
        else:
            logger.info("Received unknown packet for Meter number: "+str(filename)+". UDP socket closed")
            self.sock.close()


    def listen_clients(self):
        while True:
            data, addr = self.sock.recvfrom(4096)
            k = " ".join(["{:02x}".format(x) for x in data])
            recvsplit = k.split(' ')
            out = recvsplit[0]
            valueRes = "68 "+recvsplit[5]+" "+recvsplit[6]+" "+recvsplit[7]+" "+recvsplit[8]+" "+recvsplit[9]+" "+recvsplit[10]+" 68 02 08 02"
            testcheck = bytes.fromhex(valueRes)
            resultcheck = hex(sum(testcheck) % 256)
            checksum = resultcheck.rstrip("L").lstrip("0x").upper() or "0"
            test_res = "00 00 FE FE 68 "+recvsplit[5]+" "+recvsplit[6]+" "+recvsplit[7]+" "+recvsplit[8]+" "+recvsplit[9]+" "+recvsplit[10]+" 68 02 08 02 "+ checksum +" 16"
            logger.info("[-] Received data from the client "+ str(addr)+"{"+ str(k)+"}")
            hex_test_res = bytes.fromhex(test_res)
            platpub = k+",NACK"
            if len(k) != 0:
                dataStatus = packet_validator(k)
            else:
                dataStatus = False

            def fetch_from_cache(filename):
                try:
                    fin = open("cacheNBIOT/cache" + filename)
                    content = fin.read()
                    fin.close()
                    logger.info('Fetched the action successfully from cache for Meter number:'+str(filename))
                    plugac = content.rstrip()
                    hex_content = bytes.fromhex(plugac)
                    return content,hex_content
                except IOError:
                    logger.info("No prior meter actions received for: "+str(filename))
                    content = ""
                    hex_content = bytes.fromhex(content)
                    return content,hex_content
            if (out == "90"):
                if dataStatus:          	
                    client.publish(topicPub,platpub)
                    filename = recvsplit[10]+recvsplit[9]+recvsplit[8]+recvsplit[7]+recvsplit[6]+recvsplit[5]
                    logger.info("Validated data published to the RabbitMQ: {"+str(platpub)+"} for Meter number : " +str(filename))
                    content,hex_content = fetch_from_cache(filename)
                else:
                    logger.info("Received data not valid from the client "+ str(addr))
            else:
                pass
            if dataStatus:
                t = threading.Thread(target=self.talkToClient, args=(addr, out, hex_content, content, hex_test_res, test_res, filename, topicPub))
                t.start()

if __name__ == '__main__':
    b = Broker()
    b.listen_clients()
