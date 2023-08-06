print("THIS ALSO WORKS!")



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

