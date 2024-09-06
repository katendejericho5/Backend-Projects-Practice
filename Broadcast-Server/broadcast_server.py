import socket
import threading

# Global list to store connected clients
clients = []

def broadcast(message, current_client):
    # Send message to all clients except the sender
    for client in clients:
        if client != current_client:
            try:
                client.send(message)
            except:
                client.close()
                remove(client)

def handle_client(client_socket):
    while True:
        try:
            # Receive message from client
            message = client_socket.recv(1024)
            broadcast(message, client_socket)
        except:
            # Handle client disconnection
            remove(client_socket)
            break

def remove(client_socket):
    if client_socket in clients:
        clients.remove(client_socket)

def start_server(port=12345):
    # Create a server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', port))
    server_socket.listen(5)
    print(f"Server started, listening on port {port}...")

    while True:
        client_socket, addr = server_socket.accept()
        clients.append(client_socket)
        print(f"Client {addr} connected.")
        
        # Start a thread to handle each client
        threading.Thread(target=handle_client, args=(client_socket,)).start()

def main():
    import sys
    if len(sys.argv) < 2:
        print("Usage: broadcast-server start")
        sys.exit(1)
    
    command = sys.argv[1]

    if command == "start":
        start_server()
    else:
        print("Unknown command. Use 'start'.")
        sys.exit(1)

if __name__ == "__main__":
    main()
