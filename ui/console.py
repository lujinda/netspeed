#/usr/bin/env python
#coding:utf8
from core.config import *
from threading import Thread
from core import iface
from core import switchmode
import sys
import signal
import time

class UpdateUi(Thread):
    def __init__(self,opt):
        Thread.__init__(self)
        self.interval=opt.interval
        self.start_time=time.time()
        self.show_mode=opt.show_mode
        self.time_loop=True
        self.SwitchMode=switchmode.SwitchMode(self.show_mode)
        signal.signal(signal.SIGINT,self.stop)
        signal.signal(signal.SIGTERM,self.stop)

        self.if_list=opt.ifaces
        self.if_nums=len(self.if_list)
        self.mess_list_len=dict().fromkeys(self.if_list,0)  # 清空输出，用于记录上一次消息的位数

    def move_up(self,times):
        for i in range(times):
            esc=chr(27)
            sys.stdout.write(esc + '[A')
            sys.stdout.flush()
            

    def run(self):
        self.stat_list={}  # iface netspeed stat list
        ifaceData=iface.IfaceData(self.stat_list,
                self.if_list,self.show_mode,self.interval)
        ifaceData.setDaemon(True)
        ifaceData.start()
        
        
        while True:
            self.refresh()
            if not self.time_loop:break
            self.clear_line(self.line_count)
            

    def refresh(self):
        now_time=time.time()
        cost_time=now_time-self.start_time

        self.show_time(cost_time)
        self.show_if_stat()
        time.sleep(self.interval)

    def clear_line(self,line_count):
        self.move_up(self.if_nums)
        for if_name in self.if_list:
            sys.stdout.write(' '*self.mess_list_len[if_name]+'\n')
        self.move_up(self.line_count)
            
    def get_total(self,if_data):
        try:
            r_total,t_total=map(lambda x,y,z:y+z-x,
                if_data['start_size'],if_data['last_size'],
                    if_data['speed_size']) # 计算当前总输出的数据
        except KeyError:
            r_total,t_total=0,0

        return r_total,t_total
                

        
    def show_if_stat(self):
        if self.stat_list:
            for if_name in self.if_list:
                if_data=self.stat_list[if_name]
                r_speed,t_speed=if_data.get('speed_size',(0,0))
                r_total,t_total=self.get_total(if_data)

                mess="%-8s :%10s/s\t%10s/s\t%10s\t%10s"%(if_name,
                        self.SwitchMode.swit_mode(r_speed),
                        self.SwitchMode.swit_mode(t_speed),
                        self.SwitchMode.swit_mode(r_total),
                        self.SwitchMode.swit_mode(t_total),)
                self.mess_list_len[if_name]=len(mess)
                sys.stdout.write(mess + '\n')

                sys.stdout.flush()
            self.line_count=1+len(self.stat_list)
        else:
            self.line_count=1

    def show_time(self,cost_time):
        hours=int(cost_time/60/60)
        mins=cost_time/60%60
        secs=cost_time%60
        
        sys.stdout.write("already run : %02d:%02d:%02d\n"%(hours,
            mins,secs))

    def stop(self,signum,_):
        self.time_loop=False

class show_ui(object):
    def __init__(self,opt):
        self.if_list=opt.ifaces
        self.show_mode=opt.show_mode
        print "netspeed v0.1\t——q8886888@qq.com\n"
        print "%-8s  %10s\t%10s\t%10s\t%10s"%("iface","Receive","Transmit",
                "RX total","TX total")
        update_ui=UpdateUi(opt)
        update_ui.setDaemon(True)
        update_ui.start()
        while True:
            if not update_ui.isAlive():
                break
            time.sleep(1)

def main(opt):
    try:
        show_ui(opt)
    except KeyboardInterrupt:
        print 'bye~'
        sys.exit(0)
        
        
    
    
