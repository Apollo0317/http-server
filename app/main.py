import socket  # noqa: F401
import re
from concurrent.futures import ThreadPoolExecutor
import os
import sys
import gzip

def handle_request(client_socket:socket.socket):
    content=''
    Content_Encoding=''
    status_describe='Not Found'
    code=404
    bufsize=1024
    Content_Type:str='text/plain'
    Content_length:int=0
    #parsing request
    request=client_socket.recv(bufsize).decode()
    data_list:list[str]=request.split('\r\n')
    request_line=data_list[0].split(' ')
    method=request_line[0]
    target=request_line[1]
    #parsing request header
    request_header={}
    items=re.findall(r'\n(.*?): (.*?)\r',request)
    print('item=',items)
    for (key,value) in items:
        request_header[key]=value

    # depression detection
    try:
        if 'gzip' in request_header.get('Accept-Encoding'):
            Content_Encoding='gzip'
    except Exception as e:
        print(e)

    if method=='POST':
        request_body=data_list[-1]
        Content_Type='application/octet-stream'
        Content_length=len(bytes(request_body,encoding='utf-8'))
        code=201
        status_describe='Created'
        filename=target[7:]
        path=sys.argv[2]
        print(path+filename)
        try:
            with open(file=path+filename,mode='w',encoding='utf-8') as f:
                f.write(request_body)
        except Exception as e:
            print(e)
        client_socket.send("HTTP/1.1 201 Created\r\n\r\n".encode())
        client_socket.close()
        return

    elif target=='/':
        print('\\ get now')
        code=200
        status_describe='OK'

    elif target[:5]=='/echo':
        code=200
        status_describe='OK'
        content=target[6:]
        print('content=',content)

    elif target=='/user-agent':
        code=200
        status_describe='OK'
        content=request_header['User-Agent']
        #Content_length=len(content)

    elif '/files' in target:
        code=200
        status_describe='OK'
        path=sys.argv[2]
        filename=target[7:]
        print(os.listdir(path))
        if filename in os.listdir(path=path):
            try: 
                filepath=path+filename
                print(filepath)
                with open(file=filepath,encoding='utf-8') as f:
                    content=f.read()
            except Exception as e:
                print(e)
            Content_Type='application/octet-stream'
            #Content_length=len(bytes(content,encoding='utf-8'))
        else:
            code=404
            status_describe='Not Found'

    else:
        code=404
        status_describe='Not Found'
    
    if Content_Encoding=='gzip':
            try:
                content=gzip.compress(data=content.encode()).hex()
                print(f'content={content}')
            except:
                pass
    Content_length=len(content)
    #start forming response
    response=b''
    #form response status
    status=bytes('HTTP/1.1 {} {}\r\n'.format(code,status_describe),encoding='utf-8')
    #form response header
    headers=''
    headers+=f'Content-Type: {Content_Type}\r\n'
    headers+=f'Content-Length: {Content_length}\r\n'
    if Content_Encoding:
        headers+=f'Content-Encoding:{Content_Encoding}\r\n'
    headers+='\r\n'
    headers=bytes(headers,encoding='utf-8')
    #headers=bytes(f'Content-Type: {Content_Type}\r\nContent-Length: {Content_length}\r\n\r\n',encoding='utf-8')

    #form response body
    body=bytes(f'{content}',encoding='utf-8')
    response+=status
    response+=headers
    response+=body
    print('response=',response)
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
