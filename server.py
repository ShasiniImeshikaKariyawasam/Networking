import socket
import threading
import sys
import signal # Allow socket destruction on Ctrl+C


HOST = '127.0.0.1'
PORT = 9090
#https://docs.python.org/2/howto/sockets.html
'''
           serversocket = socket.socket(
               socket.AF_INET, socket.SOCK_STREAM)
           serversocket.bind((socket.gethostname(), 80))
           serversocket.listen(5)
'''
folder = 'web'

print('something')
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM) # socket library, socket method (pass socket method)
def start ():
    #s = socket.socket(socket.AF_INET,socket.SOCK_STREAM) # socket library, socket method (pass socket method)
    
    try:
        print ('Starting server on port %s ...' % PORT)
        
        #s.connect(("",9000))  #s.connect(addr) makes a connection
        s.bind((HOST,PORT)) #   only visible within the same machine
                        # Tuple (() )
        #s.bind(('', 80)) specifies that the socket is reachable by any address the machine happens to have.
        print ('Server Started on port %s ...' % PORT)
    except OSError:
        #print (e)
        print ('Error ! Could not bind to port on %s ...' % PORT)
        shutdown()
        sys.exit(1)
    incoming() #cheak for incoming requests


def shutdown():
        try:
            print ('Shutting down server')
            s.shutdown(socket.SHUT_RDWR) #RD = Read , WR = Write

        except Exception as e:
            print(e)
            pass #pass this , means port is alredy closed
def makeHedder (responceCode):

        header = ''
        if responceCode == 200:
            header = header + 'HTTP/1.1 200 OK\n'
        elif responceCode == 404:
            header = header + 'HTTP/1.1 404 NOT Found \n'

        header = header + 'Connection Closed \n'

        return header
connections =[]   #for connections empty list
def incoming():
        s.listen(5)
        while True:
            con,add = s.accept()
            
            conThread = threading.Thread(target=handler , args=(con,add))   #threading library thread method
            #conThread.daemon = True #wont end until all the threads are done
            conThread.start() #start connetcion

            connections.append(con)
            # print(connections) 
            # print('AAAAAAAAAAAAAAAAAAA \n \n\n\n')
            # print(add)
            # connections =[]   #for connections empty list

            #if request_method == "GET" or request_method == "HEAD":
def handler (con, request_method):
    print('HNS+D')
        #global connections
    while True:
        request = con.recv(1024).decode() #data recive 1024 byts
        # print('BBBBBBBBBB \n \n\n\n')
        # for connect in connections:
        #     connect.send(bytes(request))
        #     print('BBBBBBBBBB \n \n\n\n')

        if not request:  
            connections.remove(con) 
            con.close()
            # print('CCCCCCCCC \n \n\n\n')
            break  #if no data, loop will break 
    
        print (request)
        # print ('aDADaDA \n \n\n\n')

        # request_method = request.split(' ')[0]
        # if request_method == "GET" or request_method == "HEAD":
        #  "GET /index.html" split on space
        file_requested = request.split(' ')[1]

        # If get has parameters ('?'), ignore them
        #"GET /index.html?id=11" split on space
        file_requested =  file_requested.split('?')[0]

        if file_requested == "/":
            file_requested = "/index.html"
        # else:
        #     file_requested = "/index.html"

        filepath_to_serve = folder+file_requested
        # print("Serving web page {fp}".format(fp=filepath_to_serve))

        # Load and Serve files content
        try:

            #with open(filepath_to_serve, 'rb') as f:
        # 
            f = open(filepath_to_serve, 'rb')
            #f = open('index.html', 'rb')
        # if request_method == "GET": # Read only for GET
            response_data = f.read()

            response_data = b'Hellooooo'
            f.close()
            print( 'some some file was requested \n \n',filepath_to_serve)
            print(filepath_to_serve)
            response_header = makeHedder(200)
        except FileNotFoundError:
            print("File not found. Serving 404 page.")
            response_header = makeHedder(404)
            print('sdfsaa \n \n\n\n')
            # if request_method == "GET": # Temporary 404 Response Page
            response_data = b"<html><body><center><h1>Error 404: File not found</h1></center><p>Head back to <a href='/'>dry land</a>.</p></body></html>"

        
        response = response_header.encode('utf-8')
        #print(response)
        # if request_method == "GET":
        response = response + response_data
        print('a \n \n\n\n')

        #response = '<html><body><center><h3>Error 404: File not found</h3><p>Python HTTP Server</p></center></body></html>'.encode('utf-8')
 
        print(response)
        con.send(response)
        print('test \n \n\n\n')

        con.close()
        break
    else:
        print("Unknown HTTP request method: {method}".format(method=request_method))
    # con = connection socket , a = address


start()