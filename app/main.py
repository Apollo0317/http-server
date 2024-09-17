import socket  # noqa: F401
import re

def main():
    content=''
    status_describe='Not Found'
    code=404
    bufsize=1024
    Content_Type:str='text/plain'
    Content_length:int=0
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    client_socket,client_addr=server_socket.accept() # wait for client
    #parsing request
    request=client_socket.recv(bufsize).decode()
    print('request=',request)
    data_list:list[str]=request.split('\r\n')
    request_line=data_list[0].split(' ')
    target=request_line[1]
    Content_length=len(target)-6
    #parsing request header
    request_header=''
    crif=[index for index in range(len(request)) if request[index:index+4]=='\r\n' ]
    print('crif=',crif)
    request_header=request[crif[0]+3:crif[-1]]
    header_dict={}
    items=re.findall(r'(\w+): (.*?)\r\n',request_header+'\r\n')
    print('item=',items)
    for (key,value) in items:
        header_dict[key]=value
    # if target_path!='/' and target_path[:5]!=r'/echo':
    #     code=404
    #     status_describe='Not Found'
    if target=='/':
        code=200
        status_describe='OK'
    if target=='/echo':
        code=200
        status_describe='OK'
        content=target[:6]
    if target=='/user-agent':
        code=200
        status_describe='OK'
        content=header_dict['User-Agent']

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

if __name__ == "__main__":
    main()
