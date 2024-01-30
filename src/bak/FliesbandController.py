#!/usr/bin/env python3

import pyfirmata
import time

dir = 4
en = 3
step = 5

if __name__ == '__main__':
    board = pyfirmata.Arduino('COM3')
    print("Communication Successfully started")
    board.digital[step].write(0)
    while True:
        board.digital[step].write(1)
        time.sleep(0.01)
        board.digital[step].write(0)
        time.sleep(0.1)