import SocketServer

HOST = '192.168.1.223'
PORT = 6800

socket_server = SocketServer.SocketServer(HOST, PORT)
socket_server.start_server()

#while space isnt pressed, keep receiving messages from the client and printing them to the console
while True:
    msg = socket_server.get_full_Payload()
    print(msg)

socket_server.close_connection()