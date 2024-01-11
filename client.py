import socket
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("-host", "--host", help="Host IP", default="localhost")
parser.add_argument("-port", "--port", help="Port", default=9000)

args = parser.parse_args()

class Client:
    def __init__(self, host = args.host, port = int(args.port)):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as self.cl_socket:
            self.cl_socket.connect((host, port))

            print("Connected to", host, ":", port)
            
            while True:
                data = input("Enter data: ")
                self.cl_socket.sendall(data.encode())
                
                data = self.cl_socket.recv(1024)
                print("Received -> ", data.decode())
                
    def close(self):
        self.cl_socket.close()

cl = Client()