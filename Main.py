import socket
import threading

def handlerequest(client_conn):
    try:
        request_data = client_conn.recv(4096)

        remote_host = 'www.google.com'
        remote_port = 80

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as remote_conn:
            try:
                remote_conn.connect((remote_host, remote_port))
                remote_conn.sendall(request_data)

                while True:
                    response_data = remote_conn.recv(4096)
                    if not response_data:
                        break
                    client_conn.sendall(response_data)

            except socket.error as e:
                print(f'Could not connect to {remote_host}:{remote_port} - {e}')

    except Exception as e:
        print(f'Error: {e}')
    finally:
        client_conn.close()

def main():
    proxy_host = '127.0.0.1'
    proxy_port = 8888

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((proxy_host, proxy_port))
        server.listen(5)

        print(f'Proxy server listening on {proxy_host}:{proxy_port}')

        while True:
            client_conn, client_addr = server.accept()
            print(f'Accepted connection from {client_addr}')
            thread = threading.Thread(target=handlerequest, args=(client_conn,))
            thread.daemon = True
            thread.start()

if __name__ == "__main":
    main()