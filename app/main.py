import socket  # noqa: F401
import re

def main():
    code=200
    bufsize=1024
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    client_socket,client_addr=server_socket.accept() # wait for client

    request=client_socket.recv(bufsize).decode()
    data_list:list[str]=request.split('\r\n')
    target_path=data_list[0].split(' ')[1]
    if target_path=='/index.html':
        code=404
    response=b''
    status=bytes('HTTP/1.1 {} OK\r\n'.format(code),encoding='utf-8')
    headers=b'\r\n'
    body=b''
    response+=status
    response+=headers
    response+=body
    client_socket.sendall(response)

if __name__ == "__main__":
    main()
