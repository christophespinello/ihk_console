#!/usr/bin/python3

from utils import load_config, save_config
from serial_ports import serial_ports
import serial
from bcolors import bcolors

CONFIG_FILENAME = './config.yml'

ERR_IHK_SERIAL_OK = 0
ERR_IHK_SERIAL_NO_FRAME = -1

class IHK_Serial(object):

    def __init__(self) :
        self.config = load_config(CONFIG_FILENAME)
        self.port = self.config['comport']
        self.debit = self.config['baudrate']
        self.debug = False
        if (self.config['debug']):
            self.debug = True

    def save_configuration(self) :
        self.config['debug'] = False
        if (self.debug) :
            self.config['debug'] = True
        save_config(self.config, CONFIG_FILENAME)
        print(bcolors.WARNING+"Configuration saved"+bcolors.INFO)
            
    def configure(self):
        print(bcolors.WARNING)
        print(".........................................")
        print("Serial port configuration")
        print(".........................................")
        print(bcolors.ENDC)
        print("List of serial ports ...")
        results = serial_ports()
        config = load_config(CONFIG_FILENAME)
        print("[-] : Do not change (" + config['comport'] + " selected) [Default]")
        for i in (range(1, len(results) + 1)) :
            print("[" + str(i) + '] : ' + results[i - 1])
        try:
            selected = input(bcolors.ACTION+"Type the Uart port to use and press <Enter> : "+bcolors.ENDC)
        except ValueError:
            pass
        if (selected != "0") and (selected != ""):
            self.port = results[int(selected) - 1]
            self.config['comport'] = self.port
            save_config(self.config, CONFIG_FILENAME)
            print("Configuration saved")
            
    def send_frame(self, str, timeout=0.1, display_received_data = False):
        str_serial = []
        self.serialPort = serial.Serial(self.port, self.debit, timeout=timeout)

        self.serialPort.write((str + '\r\n').encode('utf-8'))
        
        if (self.debug) :
            print(">> Send : " + str)

        err = self.receive_frame()
        if (err['str'] != "") :
            if (self.debug) :
                print("<< Receive : " + err['str'])
            elif (display_received_data) :
                print(err['str'])
        self.serialPort.close()
        return err
        
    def receive_frame(self) :
        ret = dict([('err', ERR_IHK_SERIAL_NO_FRAME), ('str', "")])

        while (True) :
            ret['err'] = ERR_IHK_SERIAL_NO_FRAME
            line = self.serialPort.read(128)
            if (line == b'') :
                return ret
            ret['err'] = ERR_IHK_SERIAL_OK
            for i in range(len(line)) :
                ret['str'] = ret['str'] + chr(line[i])
#            return(ret)
    
    def receive_alive_frame(self) :
        ret = self.send_frame(str = "version",display_received_data = True)

    
    def connect(self) :
        self.m_compteurTickFrames = 0
        print("Connect to the product ...")
        
        self.receive_alive_frame()
        



    
