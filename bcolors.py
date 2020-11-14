#!/usr/bin/python3

import sys

if sys.platform.startswith('win'):
    
    class bcolors:
        CDEFAULT = ''
        CBLUE = ''
        CGREEN = ''
        CYELLOW = ''
        CRED    = ''
        CGREY    = ''
        ENDC = ''
        HEADER = ''
        INFO = ''
        ACTION = ''
        WARNING = ''
        DEBUG = ''
        FAIL = ''
        BOLD = ''
        UNDERLINE = ''
else :
    class bcolors:
        CDEFAULT = '\033[0m'
        CBLUE = '\033[94m'
        CGREEN = '\033[92m'
        CYELLOW = '\033[33m'
        CRED    = '\33[91m'
        CGREY    = '\33[90m'
        ENDC = CDEFAULT
        HEADER = CBLUE
        INFO = CBLUE
        ACTION = CGREEN
        WARNING = CRED
        DEBUG = '\033[90m'
        FAIL = '\033[91m'
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'
