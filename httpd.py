import socket 
import threading
import os
import mimetypes

HEADER = 1024
PORT = 80
SERVER = 'localhost'
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
MSG_END = '\r\n\r\n'
SUPPORTED_METHOD = ('GET', 'HEAD')

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((SERVER, PORT))

def receive(connection):
    result = ''
    while True:
        chunk = connection.recv(HEADER)
        result += chunk.decode(FORMAT)
        if not chunk:
            raise ConnectionError
        if MSG_END in result:
            print('--------------------------------------')
            break
    return result

def build_header(date, server, content_type, content_length, connection):
    header = ''
    d = {'Date': date,'Server': server,'Content-Type': content_type,'Content-Length': content_length,'Connection': connection}
    header = '\r\n'.join(('{}: {}'.format(i, j) for i, j in d.items()))
    return header+'\r\n\r\n'

def build_body(method, url, protocol):
    header = build_header('17/07/2020','Server','text/html','34','close')
    if method in ('GET', 'HEAD'):
        code = 'HTTP/1.1 200 OK\r\n'
        # body = 'OK!\r\n'
        # res = bytes(code + header + body, encoding= 'utf-8')
        if len(url.split('.')[-1]) < len(url):  
                file_size = os.path.getsize('.'+url)
                header = build_header('17/07/2020','Server',mimetypes.MimeTypes().guess_type('.'+url)[0],str(file_size),'close')
                print(type(mimetypes.MimeTypes().guess_type('.'+url)[0]))
                with open('.'+url, 'rb') as file:
                    res = bytearray(code + header, encoding= 'utf-8') + file.read(file_size)
        else:
            file_list = next(os.walk('.'+url))[2]
            full_list = next(os.walk('.'+url))[1] + file_list
            html = '<html>\n<body>\nDirectory index file\n<ul>\n'
            print(os.path.getsize('./httptest/'))
            for x in full_list:
                html = html + ' <li><a href="' + url + '/' + x + '">' + x + '</a></li>\n'
            body = html + '<ul>\n</body>\n</html>\n'
            print(body)
            header = build_header('17/07/2020','Server','text/html',os.path.getsize('.'+url),'close')
            res = bytes(code + header + body, encoding= 'utf-8')
    else:
        code = 'HTTP/1.1 405 Method Not Allowed '
        res = bytes(code, encoding= 'utf-8')
    return res

def build_response(msg):
    try:
        method, url, protocol = (msg.split('\n')[0]).split()
        res = build_body(method, url, protocol)
    except:
        code = 'HTTP/1.1 404 Not Found '
        res = bytes(code, encoding= 'utf-8')
    return res

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    connected = True
    while connected:
        try:
            msg = receive(conn)
            print(len(msg))
            response = build_response(msg)
            conn.sendall(response)
        except:
            if conn:
                conn.close()
        finally:
            conn.close()

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


print("[STARTING] server is starting...")
start()
