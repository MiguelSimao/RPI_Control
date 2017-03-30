'''
    Simple socket server using threads
'''
 
import socket
import sys
import RPi.GPIO as GPIO

from thread import *


# GPIO
print 'Setting up GPIO board'

#setup GPIO using Board numbering
GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.OUT) #O1
GPIO.setup(21, GPIO.OUT) #status-led

# SOCKET SERVER
HOST = ''   # Symbolic name meaning all available interfaces
PORT = 1080 # Arbitrary non-privileged portGPIO.setup(23, GPIO.IN
 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'
 
#Bind socket to local host and port
try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
     
print 'Socket bind complete'
ip, port = s.getsockname()
 
#Start listening on socket
s.listen(10)

print 'Socket now listening on port %i' % port
GPIO.output(21,1)


#Function for handling connections. This will be used to create threads
def clientthread(conn,gpio):
    ip, port = s.getsockname()
    print 'Client %s connected on %i' % (ip, port)
    #Sending message to connected client
    conn.send('Welcome to the server. Type something and hit enter\n') #send only takes string
     
    #infinite loop so that function do not terminate and thread do not end.
    while True:
         
        #Receiving from client
        data = conn.recv(1024)
        reply = 'OK...' + data
        #print 'Message length: %i' % len(data)
        if not data: 
            break
        data = data[:-2]
        if data=='O10':
            gpio.output(4,0)
            print ' pin 4 set low'
        elif data=='O11':
            gpio.output(4,1)
            print ' pin 4 set high'
        else:
            print ' message not recognized'

        conn.sendall(reply)
     
    #came out of loop
    conn.close()
    print 'Client %s disconnected' % ip
 
try:
        
    #now keep talking with the client
    while 1:
        #wait to accept a connection - blocking call
        conn, addr = s.accept()
        print 'Connected with ' + addr[0] + ':' + str(addr[1])
        #start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
        start_new_thread(clientthread ,(conn,GPIO,))
            
except socket.error, exc:
   print "Caught exception socket.error : %s" % exc
   s.close()
 

s.close()
GPIO.output(21,0)
