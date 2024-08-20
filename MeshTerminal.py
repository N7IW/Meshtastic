# This program connects to a local Meshtastic node (via WiFi)
# and a remote Meshtastic node (via Mesh). It implements a terminal
# program for two-way "chats" between the two nodes.
#
# The ipList dictionary must be edited to reflect the ShortName
# and IP address of your Meshtastic nodes. 
#
import meshtastic.serial_interface
import meshtastic.tcp_interface
from pubsub import pub
from datetime import datetime
import pytz
import time

# Edit ipList as needed for your local nodes

ipList = { "N7IW" : "10.0.0.187",
           'JR02' : '10.0.0.133',
           'JR03' : '10.0.0.197',
           'JR04' : '10.0.0.56',
           '1BA8' : '192.168.1.214'}

def PrintIpList():
    for name, ip in ipList.items():
        print (name)
        
def GetLocalNode():
    valid = False
    while not valid:
        print("* Connect to Local Node *")
        print("* Type ? for options    *")
        print("> Enter Interface Type (tcp|serial):")
        interface_mode = input("> ")
        if interface_mode == '?': 
            print("Help Information:")
        elif interface_mode == 'tcp':
            PrintIpList()
            print("> Enter Local Node Name:")
            text = input("> ")
            ip_num = ipList.get(text, "None")
            if ip_num == "None": 
                print("> Node not found \n>")
            else:
                print("> Success!")
                print("> Connected to:", text)
                print("-------------------------------")
                return (ip_num, interface_mode)
                valid = True
        elif interface_mode == 'serial':
            print("Serial Selected")
            print("> Success!")
            print("> Connected to: Serial")
            print("-------------------------------")
            return interface_mode
            valid = True
   
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
# *** Executable Code Starts Here ***
hostname = GetLocalNode()
if hostname[1] == 'tcp':
    interface = meshtastic.tcp_interface.TCPInterface(hostname[0])
elif hostname == 'serial':
    interface = meshtastic.serial_interface.SerialInterface()
# Connect to remote node via Mesh
dest_node = GetDestNode()
pub.subscribe(onReceive, 'meshtastic.receive')
#----------
while True:
    text = input("> ")
    send_message(text, dest_node)
    
interface.close()