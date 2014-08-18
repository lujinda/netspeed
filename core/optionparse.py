from core import iface
from core.config import *

class UnknowIface(Exception):
    pass

def parser_args():
    import optparse
    usage="Usage: %prog [options] device1 ..."

    parser=optparse.OptionParser(usage,version=VERSION)
    help="show output is  B"
    parser.add_option('-B',dest="B",
            action="store_true",help=help)

    help="show output is  KB"
    parser.add_option('-K',dest="K",
            action="store_true",help=help)

    help="show output is MB"
    parser.add_option('-M',dest='M',
            action="store_true",help=help)

    help="print sizes in human readable format (e.g., 1K 234M)"
    parser.add_option('-H',dest='H',
            action="store_true",help=help)

    help="interval in seconds(default 1)"
    parser.add_option('-i','--interval',
            type=int,default=1,
            metavar='INTERVAL',help=help)
    
    opt,args=parser.parse_args()
    opt.show_mode=None

    if opt.B:
        opt.show_mode='B'
    elif opt.K:
        opt.show_mode='K'
    elif opt.M:
        opt.show_mode='M'
    else:
        opt.show_mode='H'

    
    unknow_if=list(set(args)-set(iface.get_if_list()))


    if unknow_if:
        raise UnknowIface("UnkonowIface %s"%(' '.join(unknow_if)))


    opt.ifaces=args or iface.get_if_list()
        
    return opt,args
    
