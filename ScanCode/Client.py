import socket

# Define server address
SERVER_IP = "192.168.64.109"
SERVER_PORT = 12345

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
client_socket.connect((SERVER_IP, SERVER_PORT))

# Send data to the server
data_to_send = "Hello from client"
client_socket.send(data_to_send.encode("utf-8"))

# Receive response from the server
response = client_socket.recv(1024).decode("utf-8")
print(f"Received response from server: {response}")

# Close the connection
client_socket.close()
