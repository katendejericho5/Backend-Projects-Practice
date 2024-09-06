import socket
import threading

# Global lists to store connected clients and message history
clients = []
message_history = []  # List to store message history

def broadcast(message, current_client):
    # Add the message to the history
    message_history.append(message.decode('utf-8'))

    # Send message to all clients except the sender
    for client in clients:
        if client != current_client:
            try:
                client.send(message)
            except:
                client.close()
                remove(client)

def send_history(client_socket):
    # Send stored message history to the newly connected client
    for message in message_history:
        try:
            client_socket.send(message.encode('utf-8'))
        except:
            client_socket.close()
            remove(client_socket)

def handle_client(client_socket):
    # Send message history to the client first
    send_history(client_socket)

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
