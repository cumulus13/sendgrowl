#!/usr/bin/env python3
from __future__ import print_function
from gntplib import Publisher,  Resource
import gntplib
import os, sys
import mimetypes
import argparse
import traceback

class growl(object):
    def __init__(self, icon = None, stricon = None):
        super(growl, self)
        self.icon = icon
        self.stricon = None

        self.IMPORT_CONFIGSET = False
        try:
            from configset import configset
            self.IMPORT_CONFIGSET = True
        except:
            self.IMPORT_CONFIGSET = False

        if self.IMPORT_CONFIGSET:
            self.configname = os.path.join(os.path.dirname(__file__), 'sendgrowl.ini')
            self.config = configset(self.configname)

    def parse_host(self, hosts):
        list_hosts = []
        if isinstance(hosts, list):
            for i in hosts:
                if ":" in i:
                    host, port = str(i).split(":")
                    port = int(port)
                    list_hosts.append({'host':host, 'port':port})
                else:
                    list_hosts.append({'host':i, 'port':23053})
        elif isinstance(hosts, str):
            if "," in hosts:
                hosts = str(hosts).split(",")
                for i in hosts:
                    if ":" in i:
                        host, port = str(i).split(":")
                        port = int(port)
                        list_hosts.append({'host':host, 'port':port})
                    else:
                        list_hosts.append({'host':i, 'port':23053})
            else:
                list_hosts.append({'host':hosts, 'port':23053})
        
        return list_hosts

    def publish(self, app, event, title, text, host='127.0.0.1', port=23053, timeout=20, icon=None, iconpath=None):
        if not icon and iconpath:
            try:
                if os.path.isfile(iconpath):
                    icon = open(iconpath, 'rb').read()
            except:
                pass
        if not iconpath:
            iconpath = self.makeicon()
        if icon:
            icon = Resource(icon)
        if host:
            host = self.parse_host(host)
        else:
            if not host:
                host = '127.0.0.1'
            if not port:
                port = 23053

        if not timeout:
            timeout = 20
        if os.getenv('DEBUG_EXTRA'):
            print ("app               =", app)
            print ("event             =", event)
            print ("title             =", title)
            print ("text              =", text)
            print ("host              =", host)
            print ("port              =", port)
            print ("timeout           =", timeout)
            print ("icon              =", icon)
            print ("iconpath          =", iconpath)
            print ("-"*220)

        if not host:
            if self.IMPORT_CONFIGSET:
                host = self.config.get_config('SERVER', 'host')
            if host == None or host == "None" or not host:
                host = '127.0.0.1'
        if not port:
            if self.IMPORT_CONFIGSET:
                port = self.config.get_config('SERVER', 'port')
            if port:
                port = int(port)
            if port == None or port == "None" or not port:
                port = 23053
        if not timeout:
            if self.IMPORT_CONFIGSET:
                timeout = self.config.get_config('GENERAL', 'timeout')
            if timeout == None or timeout == "None" or not timeout:
                timeout = 20
        if not iconpath:
            if self.IMPORT_CONFIGSET:
                iconpath = self.config.get_config('GENERAL', 'icon')
            if iconpath == "None" or not iconpath:
                iconpath = None
        if not host:
            host = "127.0.0.1"
        #print("host =", host)
        #print("port =", port)
        #print("ICON X =", icon)
        #print("type(icon) =", type(icon))        
        if isinstance(host, list):
            if host == []:
                publisher = Publisher(app, [event], icon=iconpath, timeout = timeout)
                try:
                    publisher.register()
                except:
                    pass
                try:
                    publisher.publish(event, title, text, icon=icon)
                except:
                    if "StopIteration" in traceback.format_exc():
                        print("ERROR [GROWL]: 'StopIteration'")
                    if sys.getenv('DEBUG_EXTRA'):
                        print(traceback.format_exc())
                    
            for i in host:
                publisher = Publisher(app, [event], icon=iconpath, timeout = timeout, host = i.get('host'), port = i.get('port'))
                try:
                    publisher.register()
                except:
                    pass
                try:
                    publisher.publish(event, title, text, icon=icon)
                except:
                    if "StopIteration" in traceback.format_exc():
                        print("ERROR [GROWL]: 'StopIteration'")
                    if sys.getenv('DEBUG_EXTRA'):
                        print(traceback.format_exc())
                        
        else:
            publisher = Publisher(app, [event], icon=iconpath, timeout = timeout, host = host, port = port)
            try:
                publisher.register()
            except:
                pass
                
            try:
                    publisher.publish(event, title, text, icon=icon)
            except:
                if "StopIteration" in traceback.format_exc():
                    print("ERROR [GROWL]: 'StopIteration'")
                if sys.getenv('DEBUG_EXTRA'):
                    print(traceback.format_exc())
                
    def send(self, event, title, text):
        try:
            gntplib.publish(event, title, text)
        except:
            if "StopIteration" in traceback.format_exc():
                print("ERROR [GROWL]: 'StopIteration'")
            if sys.getenv('DEBUG_EXTRA'):
                print(traceback.format_exc())

    def makeicon(self, path=None, stricon = None):
        if self.stricon == None:
            self.stricon = stricon
        if os.path.exists(str(path)):
            if "image" in mimetypes.guess_type(path)[0]:
                return os.path.abspath(path)
        else:
            if self.stricon == None: 
                self.stricon = """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"""
            
            
            imgfile = os.path.join(os.path.dirname(__file__), 'growl.png')
            if isinstance(self.stricon, list):
                print (self.stricon)
            with open(imgfile, 'wb') as img:
                if sys.version_info.major == 3:
                    import base64
                    img.write(base64.b64decode(self.stricon))
                else:
                    img.write(self.stricon.decode('base64'))
            return imgfile

    def usage(self):
        parser = argparse.ArgumentParser(formatter_class = argparse.RawTextHelpFormatter)
        parser.add_argument('APP_NAME', action = 'store', help = 'App name as registered/registering', default = 'test app')
        parser.add_argument('EVENT_NAME', action = 'store', help = 'Event name', default = 'test event')
        parser.add_argument('TITLE', action = 'store', help = 'Title name', default = 'test title')
        parser.add_argument('TEXT', action = 'store', help = 'Message/Text to be sending', default = 'test message')
        parser.add_argument('-H', '--host', action = 'store', help = 'host growl server')
        parser.add_argument('-P', '--port', action = 'store', help = 'port growl server')
        parser.add_argument('-t', '--timeout', action = 'store', help = 'Timeout message display default: 20', type=int)
        parser.add_argument('-i', '--icon', action = 'store', help = 'Image icon path, default growl icon')
        #parser.add_argument('-p', '--pushbullet', action = 'store_true', help = 'Format to pushbullet')
        if len(sys.argv) == 1:
            parser.print_help()
        else:
            args = parser.parse_args()
            self.publish(args.APP_NAME, args.EVENT_NAME, args.TITLE, args.TEXT, args.host, args.port, args.timeout, iconpath = args.icon)

if __name__ == "__main__":
    mclass = growl()
    mclass.usage()
    #event = 'test by me'
    #mclass.published('test', event, "Just Test", "HELLLOOOOOOOO")
    #def publish(self, app, event, title, text, host='127.0.0.1', port=23053, timeout=20, icon=None, iconpath=None):
    #mclass.publish('test', event, "Just Test", "HELLLOOOOOOOO", sys.argv[1])
   
