# This program connects to a local Meshtastic node (via WiFi)
# and implements a simple server that automatically responds
# to packets sent to it.
#
# The default operation is to respond to every packet received
# with an echo of the packet text. This way you can always
# know if the server node "heard" you.
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
#
# Edit ipList and messages as needed
#
ipList = { "N7IW" : "10.0.0.187",
           'JR02' : '10.0.0.133',
           'JR03' : '10.0.0.197',
           'JR04' : '10.0.0.56',
           '1BA8' : '192.168.1.214'}

msg_info = "Station Info line #1\n"\
           "Station Info line #2\n"\
           "Station Info line #3\n"\
           "Station Info line #4"

msg_help = "Options: \n"\
           "    Send 1 for Station Info \n"\
           "    Send 2 for Time and Date \n"\
           "    Send ? for this message \n"\
           "    Other messages are echoed"

msg_def1 = ""
msg_def2 = "\nSend '?' for options"

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
    now_str = now_tz.strftime("%Y-%m-%d %I:%M:%S %p")
    return now_str

def GetNodeName(nodeID):
    nodeName = "!" +"%08x" % nodeID
    for node in interface.nodes.values():
        if nodeName == node["user"]["id"]:
            nodeName = node["user"]["longName"]
    return nodeName

def onConnection(interface):
    print ("> Mesh Server Program")
    print ("> Version 0.1")
    print ("> Connected to " + GetNodeName(interface.myInfo.my_node_num))
    print ("> " + GetCurrentTime())
    print ("-------------------------------")   

def onReceive(packet, interface):
    try:
        if 'decoded' in packet:
            if packet['decoded']['portnum'] == 'TEXT_MESSAGE_APP':
                # Respond *only* to packets sent to just this node                 
                if packet['to'] == interface.myInfo.my_node_num:
                    msg = packet['decoded']['text']
                    match msg:
                        case '1': reply_message = msg_info
                        case '2': reply_message = GetCurrentTime()
                        case '?': reply_message = msg_help
                        case _  : reply_message = msg_def1 + msg + msg_def2 
                    #------------------------------------------------------
                    # Respond to sender
                    send_message(reply_message, packet['from'])
    except KeyError : print("> Error processing packet")

def send_message(message, destination):
    interface.sendText(message, destination)
    print ("Time: " + GetCurrentTime())
    print ("Dest: " + GetNodeName(destination))
    print ("Message:")
    print ("========")
    print (message)
    print ("-------------------------------")
    
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