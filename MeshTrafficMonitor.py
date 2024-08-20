# This program connects to a local Meshtastic node (via WiFi)
# and displays the time, source and type of all packets received.
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

def GetNodeName(nodeID):
    nodeName = "!" +"%08x" % nodeID
    for node in interface.nodes.values():
        if nodeName == node["user"]["id"]:
            nodeName = node["user"]["longName"]
    return nodeName

def onConnection(interface, topic=pub.AUTO_TOPIC):
    print ("> Mesh Traffic Monitor Program")
    print ("> Version 0.1")
    print ("> Connected to " + GetNodeName(interface.myInfo.my_node_num))
    print (">", GetCurrentTime())
    print ("-------------------------------")

def onReceive(packet, interface):
    try:
        source = GetNodeName(packet['from'])
        if 'decoded' in packet:
            match packet['decoded'].get('portnum'):
                case 'NODEINFO_APP':      portName = "NodeInfo "
                case 'POSITION_APP':      portName = "Position "
                case 'TELEMETRY_APP':     portName = "Telemetry"
                case 'TEXT_MESSAGE_APP':  portName = "Text     "
                case 'ADMIN_APP':         portName = "Admin    "
                case 'ATAK_PLUGIN':       portName = "ATAK     "
                case 'RANGE_TEST_APP':    portName = "RangeTest"
                case 'PAXCOUNTER_APP':    portName = "PaxCounter"
                case 'ROUTING_APP':       portName = "Routing  "
                case 'NEIGHBORINFO_APP':  portName = "NeighborInfo"
                case 'STORE_FORWARD_APP': portName = "StoreForward"
                case _:                   portName = "???"
        else:                             portName = "Encrypted"
        print (GetCurrentTime(),">", portName,"from:",source)
    except KeyError: print (GetCurrentTime(),">","Error processing packet")
   
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

while True: time.sleep(1)
interface.close()