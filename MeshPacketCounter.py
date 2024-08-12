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
import meshtastic.tcp_interface
from pubsub import pub
from datetime import datetime
import pytz
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
interface = meshtastic.tcp_interface.TCPInterface(hostname)
pub.subscribe(onConnection, 'meshtastic.connection.established')
pub.subscribe(onReceive, 'meshtastic.receive')
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