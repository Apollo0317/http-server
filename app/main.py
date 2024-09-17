import socket  # noqa: F401


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    client_socket,client_addr=server_socket.accept() # wait for client
    response=b''
    status=b'HTTP/1.1 200 OK\r\n'
    headers=b'\r\n'
    body=b''
    response+=status
    response+=headers
    response+=body
    client_socket.sendall(response)

if __name__ == "__main__":
    main()
