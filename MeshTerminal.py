# This program connects to a local Meshtastic node (via WiFi)
# and a remote Meshtastic node (via Mesh). It implements a terminal
# program for two-way "chats" between the two nodes.
#
# The ipList dictionary must be edited to reflect the ShortName
# and IP address of your Meshtastic nodes. 
#
import meshtastic.tcp_interface
from pubsub import pub
from datetime import datetime
import pytz
import time
#
# Edit ipList and messages as needed
#
ipList = { "N7IW" : "10.0.0.187",
           'JR02' : '10.0.0.133',
           'JR03' : '10.0.0.197',
           'JR04' : '10.0.0.56'}
        
def GetLocalNode():
    valid = False
    while valid == False:
        print ("> Type ? for options")
        print ("> Enter Local Node Name:")
        text = input("> ")
        if text == '?': PrintIpList()
        else:
            ip_num = ipList.get(text, "None")
            if ip_num == "None": print ("> Node not found \n>")
            else: valid = True
    print ("> Success!")
    print ("> Local Node:",text)
    print ("-------------------------------")
    return ip_num       
        
def GetDestNode():
    valid = False
    while valid == False:
        print ("> Type ? for options")
        print ("> Enter Remote Node Name:")
        text = input("> ")
        if text == '?': PrintDestNodeList()
        else:
            num = GetNodeNumber(text)
            if num == 0x0 : print ("> Node not found")
            else: valid = True
    print ("> Success!")
    print ("> Remote Node:",GetNodeName(num))
    print (">", GetCurrentTime())
    print ("-------------------------------")
    return num

def PrintIpList():
    for name, ip in ipList.items():
        print (name)
        
def PrintDestNodeList():
    for node in interface.nodes.values():
        print (node["user"]["shortName"])

def GetNodeName(nodeID):
    nodeName = "!" +"%08x" % nodeID
    for node in interface.nodes.values():
        if nodeName == node["user"]["id"]:
            nodeName = node["user"]["longName"]
    return nodeName

def GetNodeNumber(shortName):
    nodeNumber = 0x0
    for node in interface.nodes.values():
        if shortName == node["user"]["shortName"]:
            hex_num = node["user"]["id"]
            nodeNumber = (int(hex_num[1:], 16))
    return nodeNumber

def GetCurrentTime():
    tz = pytz.timezone('US/Pacific')
    now_tz = tz.localize(datetime.now())
    now_str = now_tz.strftime("%Y-%m-%d %I:%M:%S %p")
    return now_str

def onReceive(packet, interface):
    try:
        if 'decoded' in packet and packet['decoded']['portnum'] == 'TEXT_MESSAGE_APP':
             if (packet['from'] == dest_node):
                message_string = packet['decoded']['text']
                print(f"{message_string} \n> ", end="", flush=True)
    except KeyError: print(f"Error processing packet: {e}")

def send_message(message, destination):
    interface.sendText(message, destination)

# *** Executable Code Starts Here ***
print ("> Mesh P2P Terminal")
print ("> Version 0.1")
print ("-------------------------------")
# Connect to local node via WiFI
hostname = GetLocalNode()
interface = meshtastic.tcp_interface.TCPInterface(hostname)
# Connect to remote node via Mesh
dest_node = GetDestNode()
pub.subscribe(onReceive, 'meshtastic.receive')
#----------
while True:
    text = input("> ")
    send_message(text, dest_node)
    
interface.close()