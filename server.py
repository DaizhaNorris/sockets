# TCP Server
import socket
import library

from storage import Storage


BUFFER = 256


def main():
  s = library.create_server('127.0.0.1', 7777)
  database = Storage()

  # Indefinitely process commands from clients
  while True:
    # Connect the client to the server socket
    connection, addr, port = library.connect_server(s)
    # Get the command
    command = connection.recv(BUFFER)
    # Check if a command was received
    if not command:
      break
    # Process the command and get the return data
    response = library.process_command(command, database)
    # Send it back to the client through the connection
    connection.sendall(response.encode())

    # Clean up the connection
    connection.close()


# Run code
main()