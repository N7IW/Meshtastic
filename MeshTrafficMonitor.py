# This program connects to a local Meshtastic node (via WiFi)
# and displays the time, source and type of all packets received.
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
# Edit ipList as needed for your local nodes
#
ipList = { "N7IW" : "10.0.0.187",
           'JR02' : '10.0.0.133',
           'JR03' : '10.0.0.197',
           'JR04' : '10.0.0.56'}

def PrintIpList():
    for name, ip in ipList.items():
        print (name)
        
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
    print ("> Connected to:",text)
    print ("-------------------------------")
    return ip_num       
 
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
interface = meshtastic.tcp_interface.TCPInterface(hostname)
pub.subscribe(onConnection, 'meshtastic.connection.established')
pub.subscribe(onReceive, 'meshtastic.receive')
while True: time.sleep(1)
interface.close()