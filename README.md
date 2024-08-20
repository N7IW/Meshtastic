This is a collection of python scripts I've written using the Meshtastic API.


**MeshPacketAnalyzer.py**
decodes and displays all data from all packets received.

**MeshTrafficMonitor.py** 
displays the time, type and source of each packet received, one line per per packet.

**MeshPacketCounter.py** 
prints the current time and number of packets received in the previous minute. Updates once per minute.  Provides a simple metric for channel activity.

**MeshSimpleServer.py**
sends a response to every Text packet received.  Default is to echo received packet,
but stored messages can be selected from a menu.  Starting point for a more sophisticated
server or BBS

**MeshTerminal.py**
connects to a local node via WiFi and a remote node via Mesh.  Implements a command line
"chat" function between the two nodes.

**MeshBatteryMonitor.py**
monitors Telemetry packets from a remote node and displays the battery level and voltage.  The default time between Telemetry packets is ~90 minutes, so while waiting for an update, it prints a line with a series of dots. A new dot is added each time any packet is received.  This gives a visual confirmation that the local node is still active.

**MeshSignalReportRobot.py**
sends a response to each Text packet received. The response is an echo of the text along with the RSSI, SNR and Hops report.  When this script is running at a base station, mobile stations can recieve a timestamped signal report.  If the text sent by the mobile station is a location (ie, 'First + Main"), a record of the of the mobile station's location vs. signal strength can be created. The script also produces a local log of all transmissions that can be saved and used to create a map of signal coverage for the base station.
