import socket

BUFFER = 256
SERVER_PORT = 7777
PROXY_PORT = 8888

# Returns a server socket created at a given host and port.
def create_server(host, port):
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.bind((host, port))
  s.listen(1)
  print(f"Server initialized and running at {host}:{port}")
  return s

# Returns a usable connection to a client that is accessing the server.
def connect_server(s):
  connection, (addr, port) = s.accept()
  print(f"Received connection from: {addr}:{port}")
  return connection, addr, port

# Returns components of a server command <action> <key> <value>.
def parse_command(command):
  args = command.decode().strip().split(' ')
  command = None
  if args:
    command = args[0]
  key = None
  if len(args) > 1:
    key = args[1]
  value = None
  if len(args) > 2:
    value = ' '.join(args[2:])
  return command, key, value

# Executes command on server and/or proxy based on mode
def process_command(cmdline, database, proxy=False):
  command, key, value = parse_command(cmdline)
   # Execute the command based on the first word in the command line.
  if command == 'PUT':
    # Forward command only if the proxy is enabled
    if proxy:
      server_response = forward_command(cmdline, SERVER_PORT)
    proxy_response = database.save(key, value) + "\n"
    return proxy_response
  elif command == 'GET':
    return database.retrieve(key) + "\n"
  elif command == 'DUMP':
    return database.dump() + "\n"
  else:
    return "Unknown command " + command

# Returns a client socket connected to a given host and port
def create_client(host, port):
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.connect((host, port))
  return s

# Returns the response obtained from forwarding a command from the proxy to server.
def forward_command(command, port):
  print(f"Forwarding command >>> {command.decode()}")
  s = create_client('127.0.0.1', port)
  # Forward the command and get the response
  s.sendall(command)
  response = s.recv(BUFFER).decode() + "\n"
  # Clean up socket
  s.close()
  return response
  

