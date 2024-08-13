This is a collection of python scripts I've written using the Meshtastic API.

**MeshPacketAnalyzer.py** 
Decodes and displays data from all packets received.

**MeshTrafficMonitor.py** 
Displays the time, type and source of each packet received, one line per per packet.

**MeshPacketCounter.py** 
Prints the current time and number of packets received in the previous minute.  
Updates once per minute.  Provides a simple metric for channel activity.

**MeshSimpleServer.py**
Sends a response to every Text packet received.  Default is to echo received packet,
but stored messages can be selected from a menu.  Starting point for a more sophisticated
server or BBS

**MeshTerminal.py**
Connects to a local node via WiFi and a remote node via Mesh.  Implements a command line
"chat" function between the two nodes.
