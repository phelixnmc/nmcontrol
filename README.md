# NMControl
Copyright: 2012- Namecoin Project  
License: LGPLv3 (unless otherwise noted in code)  
Original idea and implementation: Khal  
  

NMControl connects .bit domain lookups to the Namecoin client to allow for easy browsing of .bit domains. 
It's modular design allows for easy extension via plugins.  

On the first start NMControl will generate various configuration files which can be edited to change behaviour (see below for operating system specific folder locations).


## Prerequisites
Fetching data from an API server or as an SPV client is in development but for now a Namecoin client needs to run and have finished downloading the blockchain. Also you need to create a `namecoin.conf` file in the Namecoin config folder like this:
```
    # server=1 tells Namecoin Core GUI to accept JSON-RPC commands.
    # By default, only RPC connections from localhost are allowed.
    server=1

    # You must set rpcuser and rpcpassword to secure the JSON-RPC api
    rpcuser=winston
    rpcpassword=USE_THIS_STRING_TO_GET_ROBBED._JUST_HAMMER_YOUR_KEYBOARD

    # namehistory=1 tells Namecoin Core to enable name history at the cost of
    # a slightly larger database (optional) (always enabled for v0.3.x client)
    #namehistory=1
```


## Windows
NMControl config folder in `%appdata%\Nmcontrol`  
Namecoin config folder in `%appdata%\Namecoin`  

### Binaries
The setup file will automatically install .bit support on Windows 8 and higher. Only .bit DNS requests will be handled by NMControl in the default configuration. Note the system tray icon.  

### Running from source: Windows
```
    pip install pywin32
    pip install bottle
    python nmcontrolwin.pyw  # GUI version
    
    # alternatively start console version in debug mode
    python nmcontrol.py --debug=1
```

### Manual DNS config Windows < 8
Point your primary system DNS to 127.0.0.1 (leave the secondary empty). This will redirect ALL your DNS requests to NMControl so you should to tell NMControl how to handle things.  
In `%appdata%/Nmcontrol/conf/service-dns.conf`:  
set `disable_standard_lookups` to 0 (and make sure there is no semicolon ";" in front)  
optional: set `resolver` to your favorite DNS server if you don't like the Google default ones. (often this is a router IP address, e.g. 192.168.1.1)  
Restart NMControl  
You can test on the command line like this: `nslookup namecoin.org 127.0.0.1` or `nslookup nx.bit 127.0.0.1`.  
  

```
; service-dns.conf example

[dns]
; Launch at startup
;start=1

; Listen on ip
;host=127.0.0.1

; Disable lookups for standard domains
disable_standard_lookups=0

; Listen on port
;port=53

; Forward standard requests to
resolver=192.168.1.1
```


## Linux / Mac OS X
NMControl config folder Linux: `/var/lib/nmcontrol` OR `~/.config/nmcontrol`  
Namecoin config folder Linux: `~/.namecoin`  
  
NMControl config folder OS X: `~/Library/Application Support/Nmcontrol`  
Namecoin config folder OS X: `~/Library/Application Support/Namecoin`  

### Running from source: Linux / Mac OS X
```
    # install pip on Linux
    sudo apt-get install python-pip

    # install pip on Mac OS X
    sudo easy_install pip

    pip install bottle
    python ./nmcontrol.py

    # alternatively start in debug mode:
    nmcontrol.py --daemon=0 --debug=1 start
```


### DNS config on Linux / Mac OS X
tbd


## Developer Notes
The windows build system consisting of the PyInstaller batch files "build_windows_gui.bat" and "build_windows_console.bat" as well as the InnoSetup "setup_script.iss" might be replaced with something different in the future.
