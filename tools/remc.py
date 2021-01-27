from zlib import compress
from zlib import decompress
from mss import mss
import socket
from threading import Thread
import pygame
import tkinter as tk
import time
import sys
try:
    h=str(sys.argv[1])
    p=int(sys.argv[2])
    WIDTH = int(sys.argv[3])
    HEIGHT = int(sys.argv[4])
except:
    print ('remc.py <host> <port> <width> <height>')
    exit()
def retreive_screenshot(conn):
    with mss() as sct:
        rect = {'top': 0, 'left': 0, 'width': WIDTH, 'height': HEIGHT}
        while True:
            img = sct.grab(rect)
            pixels = compress(img.rgb, 6)
            size = len(pixels)
            size_len = (size.bit_length() + 7) // 8
            conn.send(bytes([size_len]))
            size_bytes = size.to_bytes(size_len, 'big')
            conn.send(size_bytes)
            conn.sendall(pixels)
try:
    sock = socket.socket()
    sock.connect((h, p))
except:
    exit()
try:
    while True:
        thread = Thread(target=retreive_screenshot, args=(sock,))
        thread.start()
        thread.join()
except Exception as e:
    print(p)
    sock.close()