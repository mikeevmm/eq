# -*- coding: utf-8 -*-

import sys

def log(message, *args, **kwargs):
    print(message, *args, **kwargs)

def error(message, *args, **kwargs):
    print('ERROR:', message, *args, file=sys.stderr, **kwargs)

def warn(message, *args, **kwargs):
    print('WARNING:', message, *args, file=sys.stderr, **kwargs)

