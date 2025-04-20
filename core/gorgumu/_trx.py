import socket
import struct
import based58
import rsa
import ecdsa
import zerorpc
import hashlib
import datetime
from Crypto.Hash import RIPEMD160
#-------------|Load RSA Partner Public Key & My Public Key|-------------
try:
    with open("core/gorgumu/auths/partner_public_key.pem",'rb') as f:
        Partner_Public_Key = rsa.PublicKey.load_pkcs1(f.read())
    with open("core/gorgumu/account/efa1f375d76194fa51a3556a97e641e61685f914d446979da50a551a4333ffd7.pem","rb") as pk:
        MPUBKEY = pk.read()
        PUBLIC_KEY = ecdsa.VerifyingKey.from_pem(MPUBKEY)
except FileNotFoundError:
    pass

#-------------|Generate Transaction|-------------------------------------
class Transaction:
    try:
        with open("core/gorgumu/account/efa1f375d76194fa51a3556a97e641e61685f914d446979da50a551a4333ffd7.pem", "rb") as pub:
            public_key_data = pub.read()
            hashing = hashlib.sha256(str(public_key_data).encode()).hexdigest()
            hashing_to_bytes = hashing.encode()
            Ripmd = RIPEMD160.new(hashing_to_bytes)
            last_hash = Ripmd.hexdigest()
            Ripmd_to_bytes = last_hash.encode()
            enc = based58.b58encode(Ripmd_to_bytes)
            me = enc.decode()
    except:
        FileExistsError

    def __init__(self,receiver,amount):
        self.sender = self.me
        self.receiver = receiver
        self.amount = amount
        self.timesamp = datetime.datetime.now().date()
        self.data = f"{self.sender}|{self.receiver}|{self.amount}|{self.timesamp}"
        self.hash = self.calculate_hash()
    '''
    Function To Calculate Transaction Hash
    '''
    def calculate_hash(self):
        sha = hashlib.sha256()
        sha.update(self.data.encode())
        return sha.hexdigest()
    '''
    Function To Sign Transaction
    '''
    def sign_transaction(self,trx):
        trx_data = str(trx)
        trx_bytes = trx_data.encode()    
        with open("core/gorgumu/account/715dc8493c36579a5b116995100f635e3572fdf8703e708ef1a08d943b36774e.pem", "rb") as f:
            private_key_data = f.read()
            if not private_key_data:
                raise ValueError("Private key file is empty")
            private_key_index = private_key_data.find(b"-----BEGIN EC PRIVATE KEY-----")
            if private_key_index == -1:
                raise ValueError("Couldn't find private key in file")
            private_key_data = private_key_data[private_key_index:]
            private_key = ecdsa.SigningKey.from_pem(private_key_data)
            signature = private_key.sign(trx_bytes)
            print(signature)
            return signature
    '''
    Function To Send (Signature & Public_Key) To The 'AMST' Wallet For Verification
    '''
    def Send(self,Trx,Receiver,Amount):
        #------>|Variable To String|----------
        SENDER = str(self.sender)
        SIGNATURE = self.sign_transaction(Trx)
        Time = str(self.timesamp)
        HASH = self.hash
        Am0unt = str(Amount)
        TRX_Data = str(Trx)
        recepient = str(Receiver)
        #--------------------------|Encrypt Data|------------------------------
        ENCRYPT_SENDER = rsa.encrypt(SENDER.encode(),Partner_Public_Key)
        ENCRYPT_TIME = rsa.encrypt(Time.encode(),Partner_Public_Key)
        ENCRYPT_HASH = rsa.encrypt(HASH.encode(),Partner_Public_Key)
        ENCRYPTED_AMOUNT = rsa.encrypt(Am0unt.encode(),Partner_Public_Key)
        ENCRYPTED_RECEIVER = rsa.encrypt(recepient.encode(),Partner_Public_Key)
        ENCRYPTED_TRX = rsa.encrypt(TRX_Data.encode(),Partner_Public_Key)
        public_key_der = PUBLIC_KEY.to_der()
        #---------------------------|Connect With Webserver For Verification With ZERORPC Protocol|--------------------------------
        c = zerorpc.Client()
        c.connect("tcp://136.244.80.252:4242")
        c.verify_transaction(SIGNATURE,ENCRYPTED_TRX,public_key_der,ENCRYPT_SENDER,ENCRYPTED_RECEIVER,ENCRYPTED_AMOUNT,ENCRYPT_TIME, ENCRYPT_HASH)
        return c
