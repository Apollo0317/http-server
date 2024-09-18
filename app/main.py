import socket  # noqa: F401
import re
from concurrent.futures import ThreadPoolExecutor



def handle_request(server_socket):
    content=''
    status_describe='Not Found'
    code=404
    bufsize=1024
    Content_Type:str='text/plain'
    Content_length:int=0
    client_socket,client_addr=server_socket.accept() # wait for client
    print(f'new connecton:addr={client_addr}')
    #parsing request
    request=client_socket.recv(bufsize).decode()
    print('request=',request)
    data_list:list[str]=request.split('\r\n')
    request_line=data_list[0].split(' ')
    target=request_line[1]
    #parsing request header
    request_header={}
    items=re.findall(r'\n(.*?): (.*?)\r',request)
    print('item=',items)
    for (key,value) in items:
        request_header[key]=value

    if target=='/':
        code=200
        status_describe='OK'
    elif target[:5]=='/echo':
        code=200
        status_describe='OK'
        content=target[6:]
        Content_length=len(content)
    elif target=='/user-agent':
        code=200
        status_describe='OK'
        content=request_header['User-Agent']
        Content_length=len(content)
    else:
        code=404
        status_describe='Not Found'
        
    #start forming response
    response=b''
    #form response status
    status=bytes('HTTP/1.1 {} {}\r\n'.format(code,status_describe),encoding='utf-8')
    #form response header
    headers=bytes(f'Content-Type: text/plain\r\nContent-Length:{Content_length}\r\n\r\n',encoding='utf-8')
    #form response body
    body=bytes(f'{content}',encoding='utf-8')
    response+=status
    response+=headers
    response+=body
    client_socket.sendall(response)

def main():
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    with ThreadPoolExecutor(max_workers=5) as executor:
        executor.submit(handle_request,server_socket)


if __name__ == "__main__":
    main()
