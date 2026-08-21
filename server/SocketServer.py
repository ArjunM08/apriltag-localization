import socket
import pickle
import struct

class SocketServer:
    def __init__(self, IP: str, PORT:int):
        #initialize socket at given IP and PORT using TCP for guaranteed transmission of data
        self.IP = IP
        self.PORT = PORT
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start_server(self) -> None:
        self.socket.bind((self.IP, self.PORT))
        self.socket.listen()
        print("listening for connection...")
        self.connection, self.clientAddr = self.socket.accept()
        print(f"connected to: {self.clientAddr}")

    def recieve_bytes(self, numOfBytes: int) -> bytearray:
         #Helper function to ensure all bytes specified are received
         data = bytearray()
         while len(data) < numOfBytes:
              packet = self.connection.recv(numOfBytes - len(data))
            #   if not packet:
            #     raise RuntimeError("Socket connection broken")  
              data.extend(packet)
         return data

    def get_full_Payload(self, headerSize = 4):
        assert headerSize == 4, "Header size is expected to be 4 bytes for unpacking the length of the body"

        #First get header which indicates how long the full mssg will be to ensure it is fully recieved
        payloadLength = self.recieve_bytes(headerSize)
        bodyLength = struct.unpack("!I", payloadLength)[0]  #unpack the header to get the length of the body

        serialized_body = self.recieve_bytes(bodyLength)

        try:
            deserialized_body = pickle.loads(serialized_body)
        except Exception as e:
             raise RuntimeError("Issue deserializing payload with pickle") from e
        
        return deserialized_body

    def close_connection(self) -> None:
        self.connection.close()
        self.socket.close()