import hashlib
import based58 # type: ignore
from ._ficher import *
from .gorgumu._db import *
from decimal import Decimal
from .gorgumu._loan import *
from tkinter import messagebox
from .gorgumu._uploader import *
from Crypto.Hash import RIPEMD160

'''
Function Count Transactions
'''
def transaction_counter(address):
    try:
        maddress = address
        statement = session.prepare(f"SELECT COUNT(*) FROM gorgumu.transaction WHERE sender = '{maddress}' ALLOW FILTERING")
        rows = session.execute(statement)
        if rows:
            transaction_count = next(rows)[0]  # Assuming the first row contains the count
            return transaction_count
        else:
            print("No transactions found")
            return 0
    except:
        pass
"""
Function To Check Client Iscore
"""
def my_iscore():
    #------------------------|Get_Client_Address|------------------------------
    with open("core/gorgumu/account/efa1f375d76194fa51a3556a97e641e61685f914d446979da50a551a4333ffd7.pem", "rb") as pub:
        public_key_data = pub.read()
        hashing = hashlib.sha256(str(public_key_data).encode()).hexdigest()
        hashing_to_bytes = hashing.encode()
        Ripmd = RIPEMD160.new(hashing_to_bytes)
        last_hash = Ripmd.hexdigest()
        Ripmd_to_bytes = last_hash.encode()
        enc = based58.b58encode(Ripmd_to_bytes)
        dec = enc.decode()
    #-------------------------|Start Check|---------------------------------------
    get_client_iscore = SimpleStatement(f"SELECT iscore FROM gorgumu.wallet WHERE address = '{dec}';")
    client_iscore = session.execute(get_client_iscore).one()
    client_iscore = client_iscore.iscore
    return client_iscore
'''
Function To Calculate & Generate Loan With Interest Rates And Calculate Debts
    [1].Conditions:
        * Client Has Many Transactions More Than 20 trx
        * Client Iscore is Satisfactory (More Than 626pt)
        * Client Data Upload
    [2].Args:
        *order: The Client Address
        *amount: The Loan Amount
    [3].Iscore Rate:
        * From 400 -----To------>520 = High Risk
        * From 521 -----To-----> 625 = Unsatisfactory
        * From 626 -----To-----> 700 = Satisfactory
        * From 701 -----To-----> 750 = Cool
        * From 751 -----To-----> 850 = Perfect
'''
def calculate_loan(order,amount):
    client_score = my_iscore()
    obj = Loan(amount,order)
    get_client_balance = SimpleStatement(f"SELECT balance FROM gorgumu.wallet WHERE address= '{order}';")
    client_balance = session.execute(get_client_balance).one()
    client_balance = client_balance.balance
    get_loanbox_amount = SimpleStatement("SELECT loansupply FROM gorgumu.Loanbox WHERE total = 'MAX';")
    loanbox_amout = session.execute(get_loanbox_amount).one()
    loanbox_amout = loanbox_amout.loansupply
    trx_counter = transaction_counter(order)
    #------------|Check If Client Has More Than 20 Transctions|-----------------
    if trx_counter is not None and trx_counter>=20 and client_score >=626:
        upload_file()
        #---------------------------------|UPDATE CLIENT BALANCE & LOANBOX SUPPLY|-------------------------
        NEW_BALANCE = Decimal(client_balance) + Decimal(amount)
        UPDATE_LOANBOX_SUPPLY = Decimal(loanbox_amout) - Decimal(amount)
        INSERT_NEW_BALANCE = session.prepare(f"UPDATE gorgumu.wallet SET balance = {NEW_BALANCE} WHERE address = '{obj.order}';")
        INSERT_NEW_LOANBOX_SUPPLY = session.prepare(f"UPDATE gorgumu.loanbox SET loansupply = {UPDATE_LOANBOX_SUPPLY} WHERE total = 'MAX';")
        #-------|Calculate Debt|--------
        INTEREST = calculate_real_intrest(amount)
        DEBT = INTEREST + amount
        #----------------------------------------------|Insert Data|--------------------------------------
        INSERT_LOANS_INFO = SimpleStatement(f"INSERT INTO gorgumu.loans(address,amount,debt,datetime,expire_date) VALUES ('{obj.order}',{obj.amount},{DEBT},'{obj.datetime}','{obj.expire_date}')")
        session.execute(INSERT_NEW_BALANCE)
        session.execute(INSERT_NEW_LOANBOX_SUPPLY)
        session.execute(INSERT_LOANS_INFO)
        messagebox.showinfo("Succuful","You Get The Loan Succufull")
    else:
        messagebox.showwarning("Failed","Your Transaction Numbers Not Enough or Your Credit Score Is Less Than Satisfactory")