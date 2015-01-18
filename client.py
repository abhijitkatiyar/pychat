import socket,select,string,sys

def prompt(name):
	sys.stdout.write('<'+name+'> ')
	sys.stdout.flush()

class Client:
	"""Class contains functions to create,return and connect socket"""

	def __init__(self, host, port):
		self.host=host
		self.port=port

	def create(self):
		self.s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		self.s.settimeout(2)

	def connect(self):
		try:
			self.s.connect((self.host,self.port))
		except:
			return False

	def get_sockets(self):
		self.socket_list=[sys.stdin,self.s]

	def soc(self):
		return self.s

if __name__=="__main__":
	
	if(len(sys.argv)<3):
		print 'Usage-> python client.py host_name port'
		sys.exit()
	
	name=raw_input("Enter Your Name: ")
	obj= Client(sys.argv[1],int(sys.argv[2]))
	
	obj.create()
	
	if(obj.connect()==False):
		print 'Connection Error'
		sys.exit()
	print 'Connected to the host. Start chatting now!!'
	prompt(name)
	while 1:
		pass
		obj.get_sockets()
		read_sockets,write_sockets,error_sockets=select.select(obj.socket_list,[],[])

		for sock in read_sockets:
			if sock==obj.soc():
				data=sock.recv(4096)
				if not data:
					print '\nDisconnected from the server'
					sys.exit()
				else:
					sys.stdout.write('\n'+data)
					prompt(name)

			else:
				msg=sys.stdin.readline()
				obj.soc().send('<'+name+'> '+msg)
				prompt(name)