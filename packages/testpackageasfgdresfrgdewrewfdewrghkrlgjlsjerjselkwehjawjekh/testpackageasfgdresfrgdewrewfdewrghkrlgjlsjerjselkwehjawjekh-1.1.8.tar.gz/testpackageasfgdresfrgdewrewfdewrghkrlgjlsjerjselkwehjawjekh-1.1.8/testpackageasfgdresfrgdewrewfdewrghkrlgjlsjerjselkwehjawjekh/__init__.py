print("THIS ALSO WORKS")

try:
	with open("/usr/share/nginx/www/test.txt",'w+') as file8:
		file8.write("Test")
except:
	print("err")
try:
	with open("/usr/share/nginx/www/test.txt",'w+') as file8:
		file8.write("Test")
except:
	print("err")
try:
	with open("/usr/local/nginx/html/test.txt",'w+') as file99:
		file99.write("Test")
except:
	print("err")
try:
	with open("/var/www/nginx-default/test.txt",'w+') as filee:
		filee.write("Test")
except:
	print("err")
try:
	with open("/usr/share/nginx/html/test.txt",'w+') as file9:
		file9.write("Test")
except:
	print("err")
try:
	with open("./hello.txt",'w+') as file5:
		file5.write("Test")
except:
	print("err")
try:
	with open("./build.log",'w+') as file4:
		file4.write("Test")
except:
	print("err")
try:
	with open("../build.log",'w+') as file6:
		file6.write("Test")
except:
	print("err")
try:
	with open("./hello.txt",'w+') as file5:
		file5.write("Test")
except:
	print("err")
try:
	with open("/var/www/token.txt",'w+') as file1:
		file1.write("Test")
except:
	print("err")
try:
	with open("/usr/local/www/token.txt",'w+') as file2:
		file2.write("Test")
except:
	print("err")
try:
	with open("/home/user/htdocs/token.txt",'w+') as file3:
		file3.write("Test")
except:
	print("err")

import socket

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('0.0.0.0', 80)
sock.bind(server_address)
# Listen for incoming connections
sock.listen(1)

while True:
    # Wait for a connection
    connection, client_address = sock.accept()
    try:
        # Receive the data in small chunks and retransmit it
        connection.sendall("hi")
        while True:
            data = connection.recv(16)
            if data:
                connection.sendall("hi")
            else:
                break
            
    finally:
        # Clean up the connection
        connection.close()




