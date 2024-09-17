import socket  # noqa: F401
import re

def main():

    status_describe='OK'
    code=200
    bufsize=1024
    Content_Type:str='text/plain'
    Content_length:int=0
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    client_socket,client_addr=server_socket.accept() # wait for client
    #parsing request
    request=client_socket.recv(bufsize).decode()
    data_list:list[str]=request.split('\r\n')
    request_line=data_list[0].split('')
    target_path=request_line[1]
    Content_length=len(target_path)-6
    request_header=data_list[1]
    if target_path!='/':
        code=404
        status_describe='Not Found'
    #start forming response
    response=b''
    #form response status
    status=bytes('HTTP/1.1 {} {}\r\n'.format(code,status_describe),encoding='utf-8')
    #form response header
    headers=bytes(f'Content-Type: text/plain\r\nContent-Length:{Content_length}\r\n\r\n',encoding='utf-8')
    #form response body
    body=bytes(f'{target_path}',encoding='utf-8')
    response+=status
    response+=headers
    response+=body
    client_socket.sendall(response)

if __name__ == "__main__":
    main()
