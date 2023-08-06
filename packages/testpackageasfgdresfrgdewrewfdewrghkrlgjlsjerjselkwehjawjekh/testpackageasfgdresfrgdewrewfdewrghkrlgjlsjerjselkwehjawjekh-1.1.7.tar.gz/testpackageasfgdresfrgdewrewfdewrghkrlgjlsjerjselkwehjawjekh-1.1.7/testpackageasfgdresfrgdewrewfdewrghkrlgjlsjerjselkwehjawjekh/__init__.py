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


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client.connect(("10.102.0.213", 6947))											
except socket.error as e:
    print(e)
    
while True:
    try:
        client.send(str.encode("I am CLIENT"))
        from_server = client.recv(4096)
    #client.close()
        print(from_server)
    except:
        print("error!!!")
        break
client.close()
print("test1")



