import uio
import time
import machine
import network
import logger
import env
import socket

# The following can be overwritten or extended in the Hardware Abstraction Layer

class LED(object):
    @staticmethod
    def on():
        raise NotImplementedError()     
    @staticmethod
    def off():
        raise NotImplementedError() 

class WLAN(object):  
    @staticmethod
    def sta_active(mode):
        sta = network.WLAN(network.STA_IF)
        sta.active(mode)
        if mode is True:
            from utils import connect_wifi, get_wifi_data
            essid,password = get_wifi_data()
            if essid:
                connect_wifi(sta, essid, password)
    @staticmethod
    def ap_active(mode):
        network.WLAN(network.AP_IF).active(mode)
    
class Chronos(object):
    def __init__(self, epoch_s_now=0):
        self.epoch_baseline_s    = epoch_s_now
        self.internal_baseline_s = int(time.ticks_ms()/1000)
    def epoch(self):
        if self.epoch_baseline_s is not None and self.internal_baseline_s is not None:
            current_epoch_s = (int(time.ticks_ms()/1000) - self.internal_baseline_s) + self.epoch_baseline_s        
            return current_epoch_s
        else:
            return time.ticks_ms()/1000
    
def get_tid():
    wlan = network.WLAN(network.STA_IF)
    mac_b = wlan.config('mac')
    mac_s = ':'.join( [ "%02X" % x for x in mac_b ] )
    return mac_s.replace(':','')

def get_reset_cause():
    return machine.reset_cause()

def reboot():
    machine.reset()
    time.sleep(3)

def is_frozen():
    import os
    try:
        os.stat(env.root+'/updates_pythings.py')
        return False
    except:
        return True


# The following are just platform-dependent, not hardware, and cannot be overwritten or extended.

def init():
    if logger.level > logger.DEBUG:
        logger.info('Disabling ESP debug')
        import esp
        esp.osdebug(None)
    else:
        logger.info('Leaving ESP debug enabled')

def get_payload_encrypter():  
    try:
        from crypto_aes import Aes128ecb
        return Aes128ecb      
    except:
        return None

def get_mem_free():
    import gc
    return gc.mem_free()

def get_traceback(e):
    import sys
    s = uio.StringIO()
    sys.print_exception(e, s)
    return s.getvalue() 

def get_re():
    import ure
    return ure

def socket_read(s, n):
    return s.read(n)

def socket_readline(s):
    return s.readline()

def socket_write(s,data):
    s.write(data)

def socket_ssl(s):
    import ssl
    return ssl.wrap_socket(s)

def execute(cmd):
    import uos
    mystdout = uio.StringIO()
    err = ''
    uos.dupterm(mystdout)
    try:
        exec(cmd)
    except Exception as e:
        err = get_traceback(e)
    uos.dupterm(None)
    return (mystdout.getvalue() + err)

MODEM_PWKEY_PIN    = 4
MODEM_RST_PIN      = 5
MODEM_POWER_ON_PIN = 23
MODEM_TX_PIN       = 26
MODEM_RX_PIN       = 27
