#!/usr/bin/env python

class TorNotFoundError(Exception):
    pass

import urllib2
import socks
import sockshandler

import common

AUTO = "auto"

doCheck = True
def build_opener(ip="127.0.0.1", port=9150):
    o = urllib2.build_opener(sockshandler.SocksiPyHandler(socks.PROXY_TYPE_SOCKS5, ip, port))
    global doCheck
    if doCheck:
        try:
            o.open("http://127.0.0.1")
        except socks.ProxyConnectionError:
            raise TorNotFoundError
        except socks.SOCKS5Error:
            # error because no http server is running locally
            pass
        doCheck = False
    return o

goodPort = None
def build_opener_default_port(ip="127.0.0.1"):
    global goodPort
    if goodPort:
        return build_opener(ip=ip, port=goodPort)
    try:
        o = build_opener(ip=ip, port=9050)
        goodPort = 9050
    except TorNotFoundError:
        o = build_opener(ip=ip, port=9150)
        goodPort = 9150
    return o

def opener():
    if not common.app['plugins']['main'].conf['tor']:
        return None  # urllib2.build_opener()
    if common.app['plugins']['main'].conf['torport'] == AUTO:
        return build_opener_default_port(ip=common.app['plugins']['main'].conf['torip'])
    return build_opener(ip=common.app['plugins']['main'].conf['torip'],
                        port=common.app['plugins']['main'].conf['torport'])
    
if __name__ == "__main__":
    print "ip without tor:", urllib2.urlopen('http://icanhazip.com').read()
    opener = build_opener()
    print "ip with tor:",  opener.open('http://icanhazip.com').read()

    try:
        print "error on localhost:"
        opener.open('http://127.0.0.1')
    except:
        import traceback
        traceback.print_exc()

    try:
        print "error on wrong port and localhost:"
        openerWrongPort = build_opener(port=11150)
        openerWrongPort.open('http://127.0.0.1')
    except:
        import traceback
        traceback.print_exc()
