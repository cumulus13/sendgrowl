#!/usr/bin/env python3
from __future__ import print_function

import os, sys
from gntplib import Publisher, Resource, GNTPClient #coerce_to_events
import gntplib
import mimetypes
import argparse
import traceback
from configset import configset
from base64 import b64decode
import re
from pathlib import Path
from pydebugger.debug import debug
import ast


class Growl(Publisher):
    MODE_WRITE = 'wb'
    MODE_READ = 'rb'
    EVENTS = []
    APP = ""
    ICON = None
    CUSTOM_HEADERS = None
    APP_SPECIFIC_HEADERS = None
    GNTP_CLIENT_CLASS = None
    KWARGS = {}
    CONFIG = configset()
    TIMEOUT = 1
    
    def __init__(self, name = None, event_defs = [], icon=None, custom_headers=None, app_specific_headers=None, gntp_client_class=None, **kwargs):
    #def __init__(self, app = None, events = None, icon=None, custom_headers=None, app_specific_headers=None, gntp_client_class=None, **kwargs): 
        # super().__init__(name, event_defs, icon, custom_headers, app_specific_headers, gntp_client_class, **kwargs)
        self.app = name or self.APP or self.CONFIG.get_config('GENERAL', 'app')
        event_defs = self.EVENTS or list(filter(None, list(set([i.strip() for i in re.split(",| |\n", self.CONFIG.get_config('GENERAL', 'events'))]))))
        if not isinstance(event_defs, list or tuple) and event_defs: event_defs = [event_defs]
        # self.events = coerce_to_events(event_defs or 'default') 
        self.event_defs = event_defs or 'default'
        self.icon = icon or self.ICON
        self.custom_headers = custom_headers or self.CUSTOM_HEADERS
        self.app_specific_headers = app_specific_headers or self.APP_SPECIFIC_HEADERS
        self.gntp_client_class = gntp_client_class or self.GNTP_CLIENT_CLASS
        self.timeout = kwargs.get('timeout') or self.TIMEOUT or 1
        kwargs = kwargs or self.KWARGS if isinstance(self.KWARGS, dict) else {}
        
        # super(growl, self).__init__(name, event_defs, self.icon, self.custom_headers, self.app_specific_headers, self.gntp_client_class, **kwargs)
        super().__init__(name, self.event_defs, self.icon, self.custom_headers, self.app_specific_headers, self.gntp_client_class, **kwargs)
    
    def make_icon(self, icon):
        if isinstance(icon, str) and os.path.isfile(icon):
            icon = Resource(open(icon, self.MODE_READ).read())
            return icon
        else:
            icon = self.makeicon(icon)
            if os.path.isfile(str(icon)):
                icon = Resource(open(icon, self.MODE_READ).read())
                return icon
        return None
    
    def makeicon(self, path=None, stricon = None):
        debug(path = path)
        debug(stricon = stricon)
        
        if stricon and isinstance(stricon, str or bytes) and not len(stricon) > 200: stricon = None
        if stricon and os.path.isfile(stricon) and not "image" in mimetypes.guess_type(stricon)[0]: stricon = None
        
        imgfile = path if path and os.path.isfile(str(path)) else str(Path(__file__).parent / 'growl.png')
        debug(imgfile = imgfile)
        if imgfile and os.path.isfile(str(imgfile)) and "image" in mimetypes.guess_type(imgfile)[0]:
            return imgfile
        if not path:
            imgfile = str(Path(__file__).parent / 'growl.png')
            debug(imgfile = imgfile)
        if not os.path.isfile(str(imgfile)):
            self.stricon = stricon or self.stricon
            if self.stricon and not isinstance(self.stricon, bytes): self.stricon = self.stricon.encode('utf')
            if not self.stricon: 
                with open(str(Path(__file__).parent / 'icon.txt'), 'rb') as f: self.stricon = f.read()

            debug(stricon = len(self.stricon))

            with open(imgfile, self.MODE_WRITE) as img: img.write(b64decode(self.stricon))
                    
        debug(imgfile = imgfile)
        
        return imgfile

    def Publish(self, app, event, title, text, id_=None, sticky=False, priority=0, icon=None, coalescing_id=None, callback=None, gntp_callback=None, events = None, iconpath = None, custom_headers=None, app_specific_headers=None, gntp_client_class=None , **kwargs):
        self.name = app or self.app
        self.event_defs = events or self.event_defs
        if not isinstance(self.event_defs, list): self.event_defs = [self.event_defs]
        if not event in self.event_defs: self.event_defs.append(event)
        if 'default' in self.event_defs and event: self.event_defs.remove('default')
        
        self.icon = iconpath if isinstance(iconpath, Resource) else iconpath if os.path.isfile(str(iconpath)) else icon if isinstance(icon, Resource) else icon if os.path.isfile(str(icon)) else self.icon
        self.icon = self.make_icon(self.icon)
        
        self.custom_headers = custom_headers or self.custom_headers
        self.app_specific_headers = app_specific_headers or self.app_specific_headers
        self.gntp_client_class = gntp_client_class or self.gntp_client_class
        
        hosts = kwargs.get('host') or GNTPClient().address[0] or '127.0.0.1'
        hosts = [hosts] if not isinstance(hosts, list or tuple) else hosts
        ports = int(kwargs.get('port') or GNTPClient().address[1] or 23053)
        ports = [ports] if not isinstance(ports, list or tuple) else ports
        
        self.timeout = int(kwargs.get('timeout') or self.timeout) or 1
        
        try:
            kwargs.pop('host')
        except:
            pass
        try:
            kwargs.pop('port')
        except:
            pass
        try:
            kwargs.pop('timeout')
        except:
            pass        
        try:
            self.register()
        except:
            pass        
        
        if hosts:
            for i in hosts:
                if isinstance(i,  dict):
                    host = i.get('host', self.host) or '127.0.0.1'
                    port = int(i.get('port'), self.port or 23053)
                    
                    if ":" in i.get('host') and len(i.get('host').split(":")) == 2:
                        host, port = i.get('host').split(":")
                        host = host.strip() if host else self.host or '127.0.0.1'
                        port = int(port.strip()) if port and str(port).strip() else self.port or 23053
                else:
                    if ":" in i and len(i).split(":") == 2:
                        host, port = i.split(":")
                        host = host.strip() if host else self.host or '127.0.0.1'
                        port = int(port.strip()) if port and str(port).strip() else self.port or 23053
                    else:
                        host = i
                        port = int(ports[hosts.index(i)]) if ports and len(hosts) == len(ports) and str(ports[hosts.index(i)]).isdigit() else ports[0] if str(ports[0]).isdigit() else 23053
                
                try:
                    if os.getenv('DEBUG_EXTRA') or os.getenv('VERBOSE'):
                        print("hosts               :", hosts)
                        print("type(hosts)         :", type(hosts))
                        print("port                :", port)
                        print("type(port)          :", type(port))
                        print("event               :", event)
                        print("type(event)         :", type(event))
                        print("title               :", title)
                        print("type(title)         :", type(title))
                        print("text                :", text)
                        print("type(text)          :", type(text))
                        print("icon                :", type(icon))
                        print("self.icon           :", type(icon))
                        print("priority            :",  priority)
                        print("type(priority)      :",  priority)
                        print("coalescing_id       :", coalescing_id)
                        print("type(coalescing_id) :", coalescing_id)
                        print("callback            :", callback)
                        print("type(callback)      :", type(callback))
                        print("gntp_callback       :", gntp_callback)
                        print("type(gntp_callback) :", type(gntp_callback))
                        #print("self.host           :", self.host)
                        print("kwargs              :", kwargs)
                    
                    debug(host = host)
                    debug(port = port)
                    # if not host in ['localhost', '127.0.0.1']:
                    #     debug(host = host, debug = 1)
                    #     debug(port = port, debug = 1)
                    debug(self_name = self.name)
                    debug(self_event_defs = self.event_defs)
                    debug(event = event)
                    
                    super().__init__(self.name, self.event_defs, self.icon, host = host, port = port, timeout = int(self.timeout or 1))    
                    # if not isinstance(icon, Resource): icon = Resource(open(icon, 'rb').read())
                    self.publish(event, title, text, id_, sticky, priority, icon, coalescing_id, callback, gntp_callback, **kwargs)
                except Exception as e:
                    tp, vp, tb = sys.exc_info()
                    # print(vp.__str__())
                    if "Notification type not registered" in vp.__str__():
                        super().__init__(self.name, self.event_defs, self.icon, host = host, port = port, timeout = int(self.timeout or 1))
                        try:
                            if os.getenv('DEBUG') or os.getenv('VERBOSE'): print(f"register for {host}:{port}/{self.name}/{title}/{event}")
                            # print(f"register for {host}:{port}/{self.name}/{title}/{event}")
                            self.register()
                        except Exception as e1:
                            tp2, vp2, tb2 = sys.exc_info() 
                            if os.getenv('DEBUG') or os.getenv('VERBOSE'):
                                print(traceback.format_exc())
                            else:
                                print(f"[sendgrowl] E0 [{tb.tb_lineno.__str__()}]: {e}, {'activate verbose env to more detail.' if not os.getenv('DEBUG' or 'VERBOSE') else ''}")
                                print(f"[sendgrowl] E1 [{tb2.tb_lineno.__str__()}]: {e1}, {'activate verbose env to more detail.' if not os.getenv('DEBUG' or 'VERBOSE') else ''}")
                    
                    # if not isinstance(icon, Resource): icon = Resource(open(icon, 'rb').read())
                    try:
                        self.publish(event, title, text, id_, sticky, priority, icon, coalescing_id, callback, gntp_callback, **kwargs)
                    except Exception as e2:
                        tp1, vp1, tb1 = sys.exc_info()
                        if vp1.__str__() == 'timed out':
                            print(f"[sendgrowl] E2 [{tb1.tb_lineno.__str__()}]: failed send to {host}:{port} => {vp1.__str__()}, {'activate verbose env to more detail.' if not os.getenv('DEBUG' or 'VERBOSE') else ''}")
                        if os.getenv('DEBUG') or os.getenv('VERBOSE'):
                            print(traceback.format_exc())
                        else:   
                            if os.getenv('DEBUG') or os.getenv('VERBOSE'):
                                print(traceback.format_exc())
                            else:
                                if os.getenv('DEBUG') or os.getenv('VERBOSE'):
                                    print(f"[sendgrowl] E3 [{tb1.tb_lineno.__str__()}]: ", end = '')
                                    for i in ast.literal_eval(vp1.__str__().replace("b'", "'")):
                                        if 'original message:' in i:
                                            print("original message:")
                                            print(ast.literal_eval(i.split('original message:')[1].strip()))
                                        else:
                                            print(i)
                                else:
                                    print(f"[sendgrowl] E2 [{tb1.tb_lineno.__str__()}]: failed send to {host}:{port}, {'activate verbose env to more detail.' if not os.getenv('DEBUG' or 'VERBOSE') else ''}")
        else:
            try:
                super().__init__(self.name, self.event_defs, self.icon, host = host, port = port, timeout = int(self.timeout or 1))
                # if not isinstance(icon, Resource): icon = Resource(open(icon, 'rb').read())
                self.publish(event, title, text, id_, sticky, priority, icon, coalescing_id, callback, gntp_callback, **kwargs)
            except:
                try:
                    self.register()
                except Exception:
                    pass
                
                super().__init__(self.name, self.event_defs, self.icon, host = host, port = port, timeout = int(self.timeout or 1))
                # if not isinstance(icon, Resource): icon = Resource(open(icon, 'rb').read())
                self.publish(event, title, text, id_, sticky, priority, icon, coalescing_id, callback, gntp_callback, **kwargs)
    
    def pub(self, *args, **kwargs):
        return self.Publish(*args, **kwargs)
    
    def send(self, *args, **kwargs):
        return self.Publish(*args, **kwargs)
    
    def __call__(self, *args, **kwargs):
        return self.Publish(*args, **kwargs)

    def usage(self):
        parser = argparse.ArgumentParser(formatter_class = argparse.RawTextHelpFormatter)
        parser.add_argument('APP_NAME', action = 'store', help = 'App name as registered/registering', default = 'test app')
        parser.add_argument('EVENT_NAME', action = 'store', help = 'Event name', default = 'test event')
        parser.add_argument('TITLE', action = 'store', help = 'Title name', default = 'test title')
        parser.add_argument('TEXT', action = 'store', help = 'Message/Text to be sending', default = 'test message')
        parser.add_argument('-H', '--host', action = 'store', help = 'host growl server', nargs = '*')
        parser.add_argument('-P', '--port', action = 'store', help = 'port growl server')
        parser.add_argument('-t', '--timeout', action = 'store', help = 'Timeout message display default: 20')
        parser.add_argument('-i', '--icon', action = 'store', help = 'Image icon path, default growl icon')
        # parser.add_argument('-p', '--pushbullet', action = 'store_true', help = 'Forward to pushbullet')
        if len(sys.argv) == 1:
            parser.print_help()
        else:
            args = parser.parse_args()
            self.Publish(
                args.APP_NAME, 
                args.EVENT_NAME, 
                args.TITLE, 
                args.TEXT, 
                host = args.host, 
                port = args.port, 
                timeout = args.timeout, 
                iconpath = args.icon,
            )

class growl(Growl):
    pass

class Sendgrowl(Growl):
    pass

class SendGrowl(Growl):
    pass

def usage():
    mclass = Growl()
    mclass.usage()

if __name__ == "__main__":
    usage()
