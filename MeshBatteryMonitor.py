# This program connects to a local Meshtastic node (via WiFi)
# and monitors the battery level and voltage of a remote node.
#
# Telemetry packets from the selected remote node are decoded
# and the battery information is extracted. Note that running
# this program adds no additional load to the remote battery.
# We are just decoding packets remote node is already required
# to send.
#
# While waiting for a telemetery packet from the remote node,
# the program prints "Waiting." and appends a dot each time a
# packet is received.  This provides a visual confirmation that
# the local node is receiving packets frome the Mesh.
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
        print ("> Enter Node to Monitor Battery:")
        text = input("> ")
        if text == '?': PrintDestNodeList()
        else:
            num = GetNodeNumber(text)
            if num == 0x0 : print ("> Node not found")
            else: valid = True
    print ("> Success!")
    print ("> Battery Data for:",GetNodeName(num))
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
    nodeName = "!" + "%08x" % nodeID
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
        if 'decoded' in packet:
            if packet['decoded'].get('portnum') == 'TELEMETRY_APP':
                if packet['from'] == dest_node :
                    telemetry = packet['decoded'].get('telemetry', {})
                    device_metrics = telemetry.get('deviceMetrics', {})
                    if device_metrics:
                        time  = GetCurrentTime()
                        level = device_metrics.get('batteryLevel', '???')
                        volts = device_metrics.get('voltage', '?.???')
                        txt = "{0} > Level: {1}%  Voltage: {2}v".format(time, level, volts)
                        ClearDotLine()
                        print (GetNodeName(packet['from']) + ":")
                        print(txt)
                        print ("------------------------------------------------------")
                        NewDotLine()

        # Print a dot for each packet received while waiting
        PrintDots()
        
    except KeyError: print(f"Error processing packet: {e}")

def SendMessage(message, destination):
    interface.sendText(message, destination)
    
def PrintDots():
    global dots
    dots += "."
    if len(dots) > 40 : NewDotLine()
    else: print("\rWaiting" + dots, end="") 
    
def NewDotLine():
    global dots
    dots = ""
    print ("\r"," "*60,"\rWaiting.\r", end = "")
    
def ClearDotLine() :
    print ("\r"," "*60,"\r", end = "")
    
# *** Executable Code Starts Here ***
print ("> Mesh Battery Monitor")
print ("> Version 0.1")
print ("-------------------------------")
# Connect to local node via WiFI
hostname = GetLocalNode()
interface = meshtastic.tcp_interface.TCPInterface(hostname)
# Connect to remote node via Mesh
dest_node = GetDestNode()
pub.subscribe(onReceive, 'meshtastic.receive')
NewDotLine()
while True: time.sleep(0.1)
interface.close()