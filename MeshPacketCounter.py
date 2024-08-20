# This program connects to a local Meshtastic node (via WiFi)
# and displays the number of packets received during the previous
# minute.
#
# This can be used to simply measure channel activity or - if
# multiple instances are run simultaneously on multiple nodes -
# to judge the relative performance of individual radios/antennas.
#
# The ipList dictionary must be edited to reflect the ShortName
# and IP address of your Meshtastic nodes.
#
import meshtastic.serial_interface
import meshtastic.tcp_interface
from meshtastic import mesh_pb2, storeforward_pb2, paxcount_pb2, BROADCAST_NUM
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
 
def GetCurrentTime():
    tz = pytz.timezone('US/Pacific')
    now_tz = tz.localize(datetime.now())
    now_str = now_tz.strftime("%Y/%m/%d %I:%M:%S %p")
    return now_str

def GetNodeName(node_id):
    node_name = hex(node_id)
    hex_id = '!' + hex(node_id)[2:]
    for node in interface.nodes.values():
        if   hex_id == node["user"]["id"]:
           node_name = node["user"]["longName"]
    return node_name

def onConnection(interface, topic=pub.AUTO_TOPIC):
    print ("> Mesh Packet Counter Program")
    print ("> Version 0.1")
    print ("> Connected to " + GetNodeName(interface.myInfo.my_node_num))
    print (">", GetCurrentTime())
    print ("-------------------------------")

def onReceive(packet, interface):
    global packetCount
    try: packetCount += 1
    except KeyError: pass
   
# *** Executable Code Starts Here ***
hostname = GetLocalNode()
if hostname[1] == 'tcp':
    interface = meshtastic.tcp_interface.TCPInterface(hostname[0])
    pub.subscribe(onReceive, 'meshtastic.receive')
    pub.subscribe(onConnection, 'meshtastic.connection.established')
elif hostname == 'serial':
    interface = meshtastic.serial_interface.SerialInterface()
    pub.subscribe(onReceive, 'meshtastic.receive')
    pub.subscribe(onConnection, 'meshtastic.connection.established')

tz = pytz.timezone('US/Pacific')
old_min = tz.localize(datetime.now()).minute
packetCount = 0
#------
while True:
    now_time = tz.localize(datetime.now())
    if old_min != now_time.minute:
        old_min = now_time.minute
        now_str = now_time.strftime("%Y/%m/%d %I:%M %p")
        print(now_str,">", packetCount,"Packets Received")
        packetCount = 0

interface.close()