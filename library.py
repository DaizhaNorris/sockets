import socket

BUFFER = 256
SERVER_PORT = 7777
PROXY_PORT = 8888

def create_server(host, port):
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.bind((host, port))
  s.listen(1)
  print(f"Server initialized and running at {host}:{port}")
  return s

def connect_server(s):
  connection, (addr, port) = s.accept()
  print(f"Received connection from: {addr}:{port}")
  return connection, addr, port

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


def process_command(cmdline, database, proxy=False):
  # Get individual parts from client command
  command, key, value = parse_command(cmdline)
  
   # Execute the command based on the first word in the command line.
  if command == 'PUT' and proxy:
    forward_command(cmdline, SERVER_PORT)
    return database.save(key, value) + "\n"
  elif command == 'GET':
    return database.retrieve(key) + "\n"
  elif command == 'DUMP':
    return database.dump() + "\n"
  else:
    return "Unknown command " + command


def create_client(host, port):
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.connect((host, port))
  return s

def forward_command(command, port):
  s = create_client('127.0.0.1', port)
  s.sendall(command)
  response = s.recv(BUFFER).decode() + "\n"
  s.close()
  return response
  

