# This program connects to a local Meshtastic node (via WiFi)
# and responds to each text packet recieved.
#
# The response is an echo of the incoming message followed
# by RSSI, SNR and Hops reports for the incoming signal.
#
# With this program running on a base station, mobile stations
# can send messages and receive a timestamped signal report.
#
# If the text message sent by the mobile station is a
# location (i.e. "1st + Main"), the output of this program can
# be used to map the coverage of the base station.
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
ipList = { 'N7IW' : "10.0.0.187",
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
    print ("------------------------")
    return ip_num       

def GetCurrentTime():
    tz = pytz.timezone('US/Pacific')
    now_tz = tz.localize(datetime.now())
    now_str = now_tz.strftime("%Y-%m-%d %I:%M:%S %p")
    return now_str

def GetNodeName(nodeID):
    nodeName = "!" + "%08x" % nodeID
    for node in interface.nodes.values():
        if nodeName == node["user"]["id"]:
            nodeName = node["user"]["longName"]
    return nodeName

def onConnection(interface):
    print ("> Mesh Signal Reporter Program")
    print ("> Version 0.1")
    print ("> Connected to " + GetNodeName(interface.myInfo.my_node_num))
    print ("> " + GetCurrentTime())
    print ("=======================================")

def onReceive(packet, interface):
    try:
        if 'decoded' in packet:
            if packet['decoded']['portnum'] == 'TEXT_MESSAGE_APP':
                # Respond *only* to packets sent to just this node                 
                if packet['to'] == interface.myInfo.my_node_num:
                    snr =  packet.get('rxSnr', 'n/a')
                    rssi = packet.get('rxRssi','n/a')
                    if 'hopStart' in packet and 'hopLimit' in packet:
                        hop_start = packet.get('hopStart')
                        hop_limit = packet.get('hopLimit')
                        hops = hop_start - hop_limit
                    else: hops = "N/A"
                    msg = packet['decoded']['text']
                    sig_msg = "RSSI: {0}   SNR: {1}   Hops: {2}".format(rssi, snr, hops)
                    # Respond to sender
                    SendMessage(msg + "\n" + sig_msg, packet['from'])
                    # Log response on the console
                    print ("> From: " + GetNodeName(packet['from']))
                    print ("> Time: " + GetCurrentTime())
                    print ("> " + sig_msg)
                    print ("> " + msg)
                    print ("=======================================")
                
    except KeyError : print("> Error processing packet")

def SendMessage(message, destination):
    interface.sendText(message, destination)
   
# *** Executable Code Starts Here ***
hostname = GetLocalNode()
interface = meshtastic.tcp_interface.TCPInterface(hostname)
pub.subscribe(onConnection, 'meshtastic.connection.established')
pub.subscribe(onReceive, 'meshtastic.receive')
while True: time.sleep(1)
interface.close()