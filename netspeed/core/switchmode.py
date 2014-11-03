#!/usr/bin/env python
#coding:utf8

import math
from netspeed.core import config

class SwitchMode(object):
    def __init__(self,show_mode):
        self.show_mode=show_mode
        self.mode_dict={'B':self.b_mode,
                'K':self.k_mode,'M':self.m_mode,
                'H':self.h_mode} # 起了类似于switch case的效果

    def mess_mode(self,speed_data,show_mode):
        if show_mode=='B':
            s="%.2f B"%(speed_data)
        else:
            s="%.2f %sB"%(speed_data,show_mode)
        return s
        

    def swit_mode(self,data):
        if self.show_mode=='H':
            return self.h_mode(data)

        else:
            speed_data=self.mode_dict[self.show_mode](data)
            return self.mess_mode(speed_data,self.show_mode)

    def k_mode(self,data):
        return float(data/config.CONVERSION)

    def m_mode(self,data):
        return float(self.k_mode(data)/config.CONVERSION)

    def b_mode(self,data):
        return float(data)
        
    def h_mode(self,data):
        mode_list=['B','K','M']
        if data:
            t_show_mode=mode_list[int(math.log10(data))/3] # 获取data的位数，以确定相应的单位表示

        else:
            t_show_mode='B' # 如果data还是0的时候，因为 log10中的参数，不可为0,所以手动指定一下单位
            
        speed_data=self.mode_dict[t_show_mode](data)
        return self.mess_mode(speed_data,t_show_mode)


        
        
        
        

