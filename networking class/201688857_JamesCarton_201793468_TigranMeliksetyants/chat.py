import socket
import threading
import sys

connections = []
exit = False

#runs in a loop, responsible for receiving messages from the client and handling them
def handle_client(client_socket, client_address):
    while not exit:
        try:
            data = client_socket.recv(1024)
        except:
            return
        if not data:
            connections.remove((client_socket, client_address))
            print(f"Connection closed: {client_address}")
            break
        else:
            if data.decode() == "Close Connection":
                connections.remove((client_socket,client_address))
                print(f"Connection with {client_address} terminated")
            else:
                print(f"Received message from {client_address}: {data.decode()}")

#Accepts incoming connections on the server socket and creates a new thread for each client
def accept_connections(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((socket.gethostbyname(socket.gethostname()), port))
    server_socket.listen(5)
    print(f"Server started and listening on port {port}")
    while True:
        client_socket, client_address = server_socket.accept()
        connections.append((client_socket, client_address))
        print(f"New connection from {client_address}")
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()

#Prints all the current connections
def list_connections():
    print("List of current connections:")
    for i, connection in enumerate(connections):
        print(f"{i}: {connection[1][0]}:{connection[1][1]}")

#Sends a message to a specific connection, using the connection id and the connection's socket
def send_message(connection_id, message):
    connection = connections[connection_id]
    connection[0].sendall(message.encode())
    print(f"message sent to: {connection_id}")

#connects to a specific server and starts a new thread for that connection, creates a new socket from the IP address and port number
def connect_to(address, port):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((address, port))
        connections.append((client_socket, (address, port)))
        print(f"Connected to {address}:{port}")
        client_thread = threading.Thread(target=handle_client, args=(client_socket, (address, port)))
        client_thread.start()
    except:
        print("The address or port is incorrect")

#closes a specific connection id, sends "Close Connection" message to the connection to remove it
def close_connection(connection_id):
    if (connection_id < 0 or connection_id >= len(connections) or len(connections) == 0):
        print("Invalid input of connection id \n")
        return
    connection = connections[connection_id]
    send_message(connection_id, "Close Connection")
    connections.remove(connection)
    connection[0].close()
    print(f"Connection closed: {connection[1]}")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Please specify a port number as a command line argument.")
        sys.exit(1)

    port = int(sys.argv[1])
    accept_thread = threading.Thread(target=accept_connections, args=(port,))
    accept_thread.start()

    ip_address = socket.gethostbyname(socket.gethostname())
    print(f"Server's IP address is {ip_address}")

    while not exit:
        command = input("Enter command: ").split()

        if command[0] == "list":
            list_connections()

        elif command[0] == "send":
            connection_id = int(command[1])
            if(len(connections) == 0 or connection_id < 0 or connection_id >= len(connections)):
                print("Connection Id not exsist")
                continue
            message = ' '.join(command[2:])
            send_message(connection_id, message)

        elif command[0] == "connect":
            if(len(command) == 3):
                address = command[1]
                port = int(command[2])
                connect_to(address, port)
            else:
                print("Invalid Input")

        elif command[0] == "terminate":
            connection_id = int(command[1])
            close_connection(connection_id)

        elif command[0] == "myip":
            print(f"Your IP address is {ip_address}")
        elif command[0] == "myport":
            print(f"Your port is {port}")
        elif command[0] == "exit":
            exit = True
            connection_id = 0
            for connection in connections:
                send_message(connection_id, "Close Connection")
                connection_id += 1
                connection[0].close()
        elif command[0] == "help":
            print("myip Display the IP address of this process.\n")
            print("myport Display the port on which this process is listening for incoming connections.\n")
            print("connect <destination> <port no> This command establishes a new TCP connection to the specified <destination> at the specified < port no>.\n")
            print("list Display a numbered list of all the connections this process is part of.\n")
            print("terminate <connection id.> This command will terminate the connection listed under the specified number when LIST is used to display all connections. \n")
            print("send <connection id.> <message> This will send the message to the host on the connection that is designated.\n")
            print("exit: Close all connections and terminate this process\n")
    
    

