import socket  # noqa: F401
import re
from concurrent.futures import ThreadPoolExecutor
import os


def handle_request(client_socket:socket.socket):
    content=''
    status_describe='Not Found'
    code=404
    bufsize=1024
    Content_Type:str='text/plain'
    Content_length:int=0
    #parsing request
    request=client_socket.recv(bufsize).decode()
    data_list:list[str]=request.split('\r\n')
    request_line=data_list[0].split(' ')
    target=request_line[1]
    #parsing request header
    request_header={}
    items=re.findall(r'\n(.*?): (.*?)\r',request)
    print('item=',items)
    for (key,value) in items:
        request_header[key]=value
    target=target.strip()
    print('target=',target)
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
    elif 'files' in target:
        filename=target[7:]
        with open(file=filename,encoding='utf-8') as f:
            f.write(content)
        Content_Type='application/octet-stream'
        Content_length=len(bytes(content,encoding='utf-8'))
        print(f'content={content}\nfilename={filename}')
    else:
        code=404
        status_describe='Not Found'
        
    #start forming response
    response=b''
    #form response status
    status=bytes('HTTP/1.1 {} {}\r\n'.format(code,status_describe),encoding='utf-8')
    #form response header
    headers=bytes(f'Content-Type: {Content_Type}\r\nContent-Length:{Content_length}\r\n\r\n',encoding='utf-8')
    #form response body
    body=bytes(f'{content}',encoding='utf-8')
    response+=status
    response+=headers
    response+=body
    client_socket.sendall(response)
    client_socket.close()
    

def main():
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    server_socket.listen(5)
    with ThreadPoolExecutor(max_workers=5) as executor:
        while True:
            client_socket,client_addr=server_socket.accept() # wait for client
            ip=client_addr[0]+':'+str(client_addr[1])
            print(f'ip_addr={ip}')
            executor.submit(handle_request,client_socket)


if __name__ == "__main__":
    main()
