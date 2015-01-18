import select
import socket
import sys

class Server:
	"""docstring for Server"""
	def __init__(self, port, bufsize = 4096):
		self.port = port
		self.bufsize = bufsize
		self.connections = []
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

	def start(self):
		self.socket.bind(("0.0.0.0", self.port))
		self.socket.listen(10)
		self.connections.append(self.socket)

	def stop(self):
		self.socket.close()

	def accept_client(self):
		sockfd, addr = self.socket.accept()
		self.connections.append(sockfd)
		return addr

	def recieve_message(self, sockfd):
		message = sockfd.recv(self.bufsize)
		if message:
			self.broadcast_message(sockfd, message)

	def remove_client(self, sockfd):
		sockfd.close()
		self.connections.remove(sockfd)

	def broadcast_message(self, sockfd, message):
		for sock in self.connections:
			if sock != self.socket and sock != sockfd:
				try:
					sock.send(message)
				except:
					self.remove_client(sock)

	def get_connections(self):
		return self.connections

	def get_socket(self):
		return self.socket

if __name__ == '__main__':
	if len(sys.argv) < 2:
		print "Usage: python", sys.argv[0], "port"
		sys.exit()

	port = int(sys.argv[1])
	server = Server(port)
	server.start()
	print "Chat Server running on port ", port
	
	while True:
		read_sockets, write_sockets, error_sockets = select.select(server.get_connections(), [], [])
		for sock in read_sockets:
			if sock == server.get_socket():
				addr = server.accept_client()
				print "Client (%s, %s) connected" % addr
			else:
				try:
					server.recieve_message(sock)
				except:
					print "Client (%s, %s) disconnected" % sock.getpeername()
					server.remove_client(sock)

	server.stop()