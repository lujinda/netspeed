from core.config import *
from threading import Thread
import time
import sys

def get_if_list():
    import re
    re_if=re.compile(r"\s(.+?):")
    dev_data=open(DEVPATH,'rb').read()
    if_list=re_if.findall(dev_data)
    return [iface.strip() for iface in if_list]
    

class IfaceData(Thread):
    def __init__(self,stat_list,if_list,show_mode,interval):
        Thread.__init__(self)
        self.interval=interval
        self.stat_list=stat_list
        for if_name in if_list:
            self.stat_list[if_name]={}
        
        self.run_first=True

        self.if_list=if_list
        
        self.show_mode=show_mode

    def run(self):
        while True:
            self.get_if_stat()
            self.run_first=False
            time.sleep(self.interval)
            


    def get_if_stat(self):
        try:
            dev_data=open(DEVPATH,'rb').readlines()
        except OSError:
            sys.stdout.write("Not File",DEVPATH)
        for line in dev_data[2:]:
            line=line.strip()
            if_name,if_data=line.split(':',1)
            if if_name in self.if_list:
                if_now=self.stat_list[if_name]
                data_size=if_data.split()
                r_size=int(data_size[0])
                t_size=int(data_size[8])

                if self.run_first:
                    if_now['start_size']=[r_size,t_size]
                    if_now['speed_size']=[0,0]
                else:
                    if_now['speed_size']=map(lambda x,y:(y-x)/self.interval,if_now['last_size'],[r_size,t_size])
                if_now['last_size']=[r_size,t_size]

            
