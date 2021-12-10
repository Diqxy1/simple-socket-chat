import socket
import threading

server = input("Server IP: ")
port = 8003

c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
	username = input('who are you: ')
	c.connect((server, port))
	print(f'connected successfully to {server}:{port}')
except:
	print(f'Error: please review your server: {server}')

def receive_message():
	while True:
		try:
			message = c.recv(2048).decode('ascii')
			if message == 'get_user':
				c.send(username.encode('ascii'))
			else:
				print(message)
		except socket.error as e:
			print('Error: check your connection or server might be offline')
			# don't break the server ??????
			break


def send_message():
	# help help help
	while True:
		try:
			c.send(input('').encode('ascii'))
		except:
			print('Server offline')
			break

thread_receive = threading.Thread(target=receive_message, args=())
thread_send = threading.Thread(target=send_message, args=())

thread_receive.start()
thread_send.start()