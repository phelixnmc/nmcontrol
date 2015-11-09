# NMControl
Copyright: 2012- Namecoin Project  
License: LGPLv3 (unless otherwise noted in code)  
Original idea and implementation: Khal  
  

NMControl connects .bit domain lookups to the Namecoin client to allow for easy browsing of .bit domains. 
It's modular design allows for easy extension via plugins.  

On the first start NMControl will generate various configuration files which can be edited to change behavior (see below for operating system specific folder locations). NMControl needs to be restarted for changes to the configuration files to take effect.  


## Prerequisites
Fetching data from an API server or as an SPV client is in development but for now a Namecoin client needs to run and have finished downloading the blockchain. The Namecoin client datadir (= configuration folder) needs to be in the default location. Also you need to create a `namecoin.conf` file in the Namecoin config folder like this:
```
    # server=1 tells Namecoin Core GUI to accept JSON-RPC commands.
    # By default, only RPC connections from localhost (the local system) are allowed.
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
The setup file will automatically install .bit support on Windows 8 and higher. Only .bit DNS requests will be handled by NMControl in the default configuration. See below for configuration on Windows 7 and lower. Note the system tray icon.  

### Running from source: Windows
```
    pip install pywin32
    pip install bottle
    python nmcontrolwin.pyw  # GUI version
    
    # alternatively start console version in debug mode
    python nmcontrol.py --debug=1
```


## Linux / Mac OS X
NMControl config folder Linux: `/var/lib/nmcontrol` OR `~/.config/nmcontrol`  
Namecoin config folder Linux: `~/.namecoin`  
  
NMControl config folder OS X: `~/Library/Application Support/Nmcontrol`  
Namecoin config folder OS X: `~/Library/Application Support/Namecoin`  

### Running from source: Linux / Mac OS X
Unfortunately we currently need to be started privileged with sudo so that we can open the local DNS port.  
```
    # install pip on Linux
    sudo apt-get install python-pip

    # install pip on Mac OS X
    sudo easy_install pip

    sudo pip install bottle
    
    git clone https://github.com/namecoin/nmcontrol/
    cd nmcontrol
    sudo python ./nmcontrol.py

    # alternatively start in debug mode:
    sudo python nmcontrol.py --daemon=0 --debug=1 start
```


### DNS config on Linux / Mac OS X / Manual DNS config Windows 7 and below
Point your primary system DNS to 127.0.0.1 (leave the secondary empty). This will redirect ALL your DNS requests to NMControl so you should to tell NMControl how to handle things as follows.  
In `%appdata%/Nmcontrol/conf/service-dns.conf`:  
set `disable_standard_lookups` to 0 (and make sure there is no semicolon ";" in front)  
optional: set `resolver` to your favorite DNS server if you don't like the Google default ones. (often this is a router IP address, e.g. 192.168.0.1)  
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

; Forward standard requests to your standard DNS
; There has to be a comma at the end!
; e.g. lokal router ip: resolver=192.168.0.1,
; e.g. Google DNS: resolver=8.8.8.8, 8.8.4.4,
resolver=192.168.0.1,
```


## Developer Notes
The windows build system consisting of the PyInstaller batch files "build_windows_gui.bat" and "build_windows_console.bat" as well as the InnoSetup "setup_script.iss" might be replaced with something different in the future.
