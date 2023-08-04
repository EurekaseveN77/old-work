Prerequisites
Python


Running the Program
1) Open a command window in the directory where the file is located, easy method is entering "cmd" in the address bar at the top of the folder window
2) Run the command "py chat.py <port_no>" or "python chat.py <port_no>" to start the chat. Replace <port_no> with the desired port number for the server to listen on (ex. "py chat.py 55555").
3)Open another command window and enter a different port number than the first one used, multiple windows can be opened to test the messaging
4)On the window you want to connect to, in the other windows enter "connect <IP address> <port no.)>" and it will connect to the one you want to be the host (ex. "connect 192.168.1.155 55555")
5)Once connected they can message between each other based on their ID no. from the "list" by using "send <connection_id> <message>" (ex. "send 0 hey"). 
6)Windows connecting to the host cannot message each other until they connect to each other with the "connect" command.
7)The connection made between user's can be cut by using the "terminate <connection_id>" command using the number from their list number. (ex. "terminate 0")
8)A user can also make themseleves exit the program by entering "exit"



Available Commands
1) list - Display a numbered list of all the connections that the chat is part of.
2) send <connection_id> <message> - Send a message to the connection by the specified <connection_id>.
3) connect <destination> <port_no> - Establish a new TCP connection to the specified <destination> at the specified <port_no>.
4) terminate <connection_id> - Terminate the connection listed under the specified number when list is used to display all connections.
5) myip - Display the IP address of the machine where the chat is running.
6) myport - Display the port number that the chat is listening on.
7) help - Display a list of available commands.
8) exit - Close all connections and stop script.



Contributons 
James Carton got the "list", "send" and "connect" commands functional but was unable to get terminate working. 
Tigran Meliksetyants incorporated a feature to terminate connection, but faced challenges in implementing it without causing script failure due to threads. Once he overcame the issue, he proceeded to include the remaining commands in the program and added error checks.