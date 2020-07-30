import socket
import time

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
sock.connect(('localhost', 5000))

start = time.time()
for _ in range(100000):
    sock.sendall(b'BENCHMARKING!!!')
    resp = sock.recv(512)
end = time.time()

print(100000 / (end - start))
