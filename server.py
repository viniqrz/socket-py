import socket
import argparse
import selectors
import types

sel = selectors.DefaultSelector()

parser = argparse.ArgumentParser()

parser.add_argument("-host", "--host", help="Host IP", default="localhost")
parser.add_argument("-port", "--port", help="Port", default=9000)

args = parser.parse_args()

class Server :
    def __init__(self, host = args.host, port = int(args.port)):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as self.sv_socket:
            self.sv_socket.bind((host, port))
            self.sv_socket.listen()
            self.sv_socket.setblocking(False)
            
            sel.register(self.sv_socket, selectors.EVENT_READ, data=None)

            print('Server is running on port', port)
            
            while True:
                events = sel.select(timeout=None)
                for key, mask in events:
                    if key.data is None:
                        self.accept_wrapper(key.fileobj)
                    else:
                        self.service_connection(key, mask)

    def service_connection(self, key, mask):
        sock = key.fileobj
        data = key.data
        if mask & selectors.EVENT_READ:
            recv_data = sock.recv(1024)  # Should be ready to read
            if recv_data:
                data.outb += recv_data
            else:
                print(f"Closing connection to {data.addr}")
                sel.unregister(sock)
                sock.close()
        if mask & selectors.EVENT_WRITE:
            if data.outb:
                print(f"Echoing {data.outb!r} to {data.addr}")
                sent = sock.send(data.outb)  # Should be ready to write
                data.outb = data.outb[sent:]
                
    def accept_wrapper(self, sock: socket.socket):
        conn, addr = sock.accept()
        print(f"Accepted connection from {addr}")
        conn.setblocking(False)
        data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        sel.register(conn, events, data=data)
                
    def close(self):
        self.sv_socket.close()
        
    def send(self, data):
        self.sv_socket.sendall(data)
                
sv = Server()