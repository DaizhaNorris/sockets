# TCP Proxy Server
import socket
import library
from storage import Storage

BUFFER = 256
SERVER_PORT = 7777
PROXY_PORT = 8888


def main():
  s = library.create_server('127.0.0.1', PROXY_PORT)
  database = Storage()

  # Indefinitely process commands from clients
  while True:
    # Connect the client to the server socket
    connection, addr, port = library.connect_server(s)
    # Get the command
    command = connection.recv(BUFFER)
    # Check if a command was received
    if not command:
      continue
    # Process the command and get the return data
    response = library.process_command(command, database, proxy=True)
    # Send it back to the client through the connection
    connection.sendall(response.encode())

    # Clean up the connection
    connection.close()


# Run code
main()

