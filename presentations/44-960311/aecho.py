import socket
# import asyncio
import play

loop = play.Loop()

async def create_server(addr):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    sock.bind(addr)
    sock.listen(5)
    sock.setblocking(False)
    while True:
        client, addr = await loop.sock_accept(sock)
        print('Connection from: ', addr)
        loop.create_task(echo_handler(client))


async def echo_handler(client):
    with client:
        while True:
            data = await loop.sock_recv(client, 1024)
            if not data:
                break
            await loop.sock_sendall(client, b'Got: ' + data)
        print('Connection closed')

loop.create_task(create_server(('', 5000)))
loop.run_forever()
