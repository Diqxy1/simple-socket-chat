import socket
import threading

host = "IPV4 HERE"
port = 8003

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((host, port))

s.listen()
print(f'Server on and listening in {host}:{port}')

clients = []
usernames = []

def global_message(message):
	for client in clients:
		client.send(message)

def handle_messages(client):
	while True:
		try:
			reveice_message_from_client = client.recv(2048).decode('ascii')
			global_message(f'{usernames[clients.index(client)]}: {reveice_message_from_client}'.encode('ascii'))
		except:
			client_leaved = clients.index(client)
			client.close()
			clients.remove(clients[client_leaved])
			client_leaved_username = usernames[client_leaved]
			print(f'{client_leaved_username} has left the chat...')
			global_message(f'{client_leaved_username} has left us...'.encode('ascii'))
			usernames.remove(client_leaved_username)

def initial_connection():
	while True:
		try:
			client, addr = s.accept()
			print(f"New connection: {str(addr)}")
			clients.append(client)
			client.send('get_user'.encode('ascii'))
			username = client.recv(2048).decode('ascii')
			usernames.append(username)
			global_message(f'{username} just joined the chat!'.encode('ascii'))
			user_thread = threading.Thread(target=handle_messages, args=(client,))
			user_thread.start()
		except:
			pass

initial_connection()