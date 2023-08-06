#!/usr/bin/env python3

from uravo.uravo import Uravo

__version__ = "0.0.2"

uravo = Uravo()

def connect():
    return uravo

def main():
    uravo.main()
