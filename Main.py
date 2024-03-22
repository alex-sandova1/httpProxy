import socket
import threading

remote_host = 'www.example.com'
remote_port = 80

def handle_request(client_conn):
    try:
        request_data = client_conn.recv(4096)

        remote_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        remote_conn.connect((remote_host, remote_port))
        remote_conn.sendall(request_data)
        
        response_data = remote_conn.recv(4096)
        client_conn.sendall(response_data)

        remote_conn.close()
    except Exception as e:
        print(f'Error: {e}')
    finally:
        client_conn.close()

def main():
    proxy_host = '127.0.0.1'
    proxy_port = 8888
    
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((proxy_host, proxy_port))
    server.listen(5)
    
    print(f'Proxy server listening on {proxy_host}:{proxy_port}')
    
    while True:
        client_conn, client_addr = server.accept()
        print(f'Accepted connection from {client_addr}')
        thread = threading.Thread(target=handle_request, args=(client_conn,))
        thread.start()

if __name__ == "__main__":
    main()
