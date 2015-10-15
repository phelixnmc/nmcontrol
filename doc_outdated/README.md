Status
======

nmcontrol : alpha, no service yet

nmcontrol-gui : none

Description
===========

nmcontrol is a python software that will provide services based on namecoin like DNS, proxy, name (domain, alias, etc) registration and renewal.

It is composed of a daemon (nmcontrol) that communicates with namecoin and provide services, and a GUI (nmcontrol-gui) that manages the daemon.

It will allow you to :
- create domains, alias and auto renew them
- listen for dns requests
- listen for socks requests
- publish your services (in a namecoin record/namespace, services could announce themselves in the blockchain)
- etc

It is multi-threaded and designed with plugins, to enable each person to activate only what they need and what they want to share (for example, they will be able to share their DNS server).

Aim of this software is to allow people to easily build things/services based on namecoin.

Features
========

It can currently :
- start in background mode or normal mode
- send/receive rpc commands to itself
- fetch data at startup, from namecoin or from a file (then use local cached data)
- or fetch data when asked from namecoin (then use local cached data)
- manage plugins (start, stop, restart and minimal status, at least) + config files
- be easily extended

Documentation
=============

[doc/TODO.md](doc/TODO.md)

[doc/INSTALL.md](doc/INSTALL.md)

REST API
========

NMControl will by default start a REST API server on 127.0.0.2:8080.  You can access it like this:

    http://127.0.0.2:8080/dns/getIp4/bluishcoder.bit.json

Which will return something like this:

    {"result": "[\"198.58.109.235\"]"}

All non-dangerous methods should be available via REST.  Potentially dangerous methods, such as the "stop" method, are not accessible via REST for security reasons, and can only be accessed via RPC.

When accessing a method which takes multiple arguments, the arguments should be separated by a space character (%20 in the URL).

Note that we are **not** committing to a stable API at this point, so consider the REST feature to be experimental.

Developer Notes
============
The windows build system consisting of the PyInstaller batch files "build_windows_gui.bat" and "build_windows_console.bat" as well as the InnoSetup "setup_script.iss" might be replaced with something different in the future.
