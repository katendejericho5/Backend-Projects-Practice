import socket
import threading

def receive_messages(client_socket):
    while True:
        try:
            # Receive and print messages from server
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print(message)
            else:
                break
        except:
            break

def start_client(host='127.0.0.1', port=12345):
    # Create a client socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    print("Connected to the server.")

    # Start a thread to receive messages from server
    threading.Thread(target=receive_messages, args=(client_socket,)).start()

    while True:
        # Send messages to the server
        message = input()
        if message.lower() == 'exit':
            client_socket.close()
            break
        client_socket.send(message.encode('utf-8'))

def main():
    import sys
    if len(sys.argv) < 2:
        print("Usage: broadcast-client connect")
        sys.exit(1)
    
    command = sys.argv[1]

    if command == "connect":
        start_client()
    else:
        print("Unknown command. Use 'connect'.")
        sys.exit(1)

if __name__ == "__main__":
    main()
