# -*- coding: utf-8 -*-

import sys

def log(message, *args, **kwargs):
    print(message, *args, **kwargs)

def error(message, *args, **kwargs):
    print(message, *args, file=sys.stderr, **kwargs)
