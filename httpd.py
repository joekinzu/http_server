import socket
import os

HOST, PORT = 'localhost', 80

listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listen_socket.bind((HOST, PORT))
listen_socket.listen(1)
print(f'Serving HTTP on port {PORT} ...')
while True:
    client_connection, client_address = listen_socket.accept()
    request_data = client_connection.recv(1024)
    # file_size = os.path.getsize('./httptest/160313.jpg')
    # print(file_size)
    try:
    	method, url, ver = (request_data.decode('utf-8').split('\n')[0]).split()
    	print(method+'--'+url+'--'+ver)
    	# x = [os.path.join('httptest', fn) for fn in next(os.walk('httptest'))[2]]
    	# print(next(os.walk('httptest')))
    	if method in ('GET', 'HEAD'):
    		http_response = b'HTTP/1.1 200 OK\n\nOK!\n'
    		if len(url.split('.')[-1]) < len(url):	
    			file_size = os.path.getsize('.'+url)
    			# content_type = mimetypes.guess_type('./httptest/160313.jpg')[0]
    			# print(content_type, file_size)
    			with open('.'+url, 'rb') as file:
    				http_response = file.read(file_size)
    		client_connection.sendall(http_response)
    	else:
    		http_response = b'HTTP/1.1 400 BAD\n\nNOT OK!\n'
    		client_connection.sendall(http_response)
    except:
    	print('wrong request data')	
    print('-------------------------------\n')
    client_connection.close()
