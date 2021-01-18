import socket
import os
import mimetypes

HOST, PORT = 'localhost', 80
DOCUMENT_ROOT = 'www'
CONTENT_LENGTH = 0


listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listen_socket.bind((HOST, PORT))
listen_socket.listen(1)


def build_header(date, server, content_type, content_length, connection):
	header = ''
	d = {'Date': date,'Server': server,'Content-Type': content_type,'Content-Length': content_length,'Connection': connection}
	header = "\n".join(("{}: {}".format(*i) for i in d.items())) 
	return header

print(f'Serving HTTP on port {PORT} ...')
while True:
    client_connection, client_address = listen_socket.accept()
    request_data = client_connection.recv(1024)
    try:
    	method, url, ver = (request_data.decode('utf-8').split('\n')[0]).split()
    	print(ver+' '+method+' request: '+url)
    	if method in ('GET', 'HEAD'):
    		http_response = b'HTTP/1.1 200 OK\n\nOK!\n'
    		header = build_header('17/07/2020','Server','text/html','34','close')
    		if len(url.split('.')[-1]) < len(url):	
    			file_size = os.path.getsize('.'+url)
    			header = build_header('17/07/2020','Server',mimetypes.guess_type('.'+url)[0],str(file_size),'close')
    			print(header)
    			with open('.'+url, 'rb') as file:
    				http_response = file.read(file_size)
    		else:
    			print(os.path.getsize('.'+url))
    			x = next(os.walk('.'+url))[2]
    			y = next(os.walk('.'+url))[1] + x
    			html='<html>\n'+'<body>\n'+'<ul>\n'
    			for z in y:
    				html = html + '	<li><a href="'+url+'/'+z+'">' + z + '</a></li>\n'
    			shtml='HTTP/1.1 200 OK\r\n'+ header + '\r\n\r\n' + html+'<ul>\n'+'</body>\n'+'</html>\n'
    			http_response = shtml.encode()
    		client_connection.sendall(http_response)
    	else:
    		http_response = b'HTTP/1.1 405 BAD\n\nNOT OK!\n'
    		client_connection.sendall(http_response)
    except:
    	print('wrong request data')
    	http_response = b'HTTP/1.1 404 BAD\n\nPage Not Found\n'
    	client_connection.sendall(http_response)	
    print('-------------------------------\n')
    client_connection.close()
