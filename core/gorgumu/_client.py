import os
import re
import time
import ecdsa # type: ignore
import qrcode # type: ignore
import socket
import hashlib
import secrets
import based58 # type: ignore
import secrets
import platform
import datetime
from ._db import *
from datetime import date
from Crypto.Hash import RIPEMD160
from cassandra.cluster import Cluster
from ecdsa.util import encoded_oid_ecPublicKey # type: ignore
# Generate a random 256-bit integer as private key
private_key_bytes = secrets.token_bytes(32)  # 32 bytes for 256 bits
private_key_int = int.from_bytes(private_key_bytes, byteorder='big')
delta = datetime.timedelta(days=120)
#Create Wallet
class Wallet:
    def __init__(self):
        self.private_key = ecdsa.SigningKey.from_string(private_key_bytes, curve=ecdsa.SECP256k1)
        self.public_key =  self.private_key.verifying_key
        self.balance = 2
        self.iscore = 650
        self.datetime = datetime.date.today()
        self.expire_date = self.datetime + delta
    #------|convert keys format to string to hex decimal|-------------
    def key_to_string(self):
        private_key_hex = self.private_key.to_string().hex()
        public_key_hex = self.public_key.to_string().hex()
        return private_key_hex,public_key_hex
    #------------------|save keys to user device|---------------------------------------------- 
    def save_keys(self):
        directory = "core/gorgumu/account"
        if not os.path.exists(directory):
            os.mkdir(directory)
        else:
            pass
        private_key_file_name = "715dc8493c36579a5b116995100f635e3572fdf8703e708ef1a08d943b36774e.pem"
        public_key_file_name = "efa1f375d76194fa51a3556a97e641e61685f914d446979da50a551a4333ffd7.pem"
        key1_path = os.path.join(directory, private_key_file_name)
        key2_path = os.path.join(directory, public_key_file_name)
        with open(key1_path,"wb") as private_address:
            private_address.write(self.private_key.to_pem())
        with open(key2_path,"wb") as public_address:
            public_address.write(self.public_key.to_pem())
    #-----------|Encrypt Password:|----------------------
    def encrypt_password(self,psslog):
       Mac_address = None
       Hostname = socket.gethostname()
       Operation_System = platform.system()
       Passwd = str(psslog) + str(Mac_address) + str(Hostname) + str(Operation_System)
       hash = hashlib.sha256(Passwd.encode()).hexdigest()
       #-------|save password|----------
       with open("core/gorgumu/account/e7cf3ef4f17c3999a94f2c6f612e8a888e5b1026878e4e19398b23bd38ec221a.ini","w") as psw:
            psw.write(hash)
       #-------|Save Session File|--------
       today = datetime.datetime.now()
       with open("core/gorgumu/account/3f3af1ecebbd1410ab417ec0d27bbfcb5d340e177ae159b59fc8626c2dfd9175.tmp","w") as Session:
            Session.write(str(today))
    #------------------------------------|Register Wallet|------------------------------------------------
    def register_wallet(self):
        with open("core/gorgumu/account/efa1f375d76194fa51a3556a97e641e61685f914d446979da50a551a4333ffd7.pem","rb") as pub:
            public_key_data = pub.read()
            global hashing
            #---|Hashing Public Key To Sha256|----
            hashing = hashlib.sha256(str(public_key_data).encode()).hexdigest()
            #---|Convert Sha256 To RipeMd|---
            hashing_to_bytes = hashing.encode()
            Ripmd = RIPEMD160.new(hashing_to_bytes)
            last_hash = Ripmd.hexdigest()
            #---|Encode RipMd With Base58|----
            Ripmd_to_bytes = last_hash.encode()
            enc = based58.b58encode(Ripmd_to_bytes)
            global dec
            dec = enc.decode()
        #cluster = Cluster()
        #session = cluster.connect()
        insert_statement = session.prepare(f"INSERT INTO gorgumu.wallet (address, balance, datetime, expire_date,iscore) VALUES ('{dec}', {self.balance}, '{self.datetime}', '{self.expire_date}',{self.iscore})")
        session.execute(insert_statement)
        #session.shutdown()
        #cluster.shutdown()
    #----------------------------------------------------|qrcode|-------------------------------------------
    def myqrcode(self):
        myqr = qrcode.make(dec)
        myqr.save("core/gorgumu/account/61f2c041d4e9e0f558ae5ee8d6adb62e79bacce45be6d0b6d0bbe8947f5f0dd9.png")