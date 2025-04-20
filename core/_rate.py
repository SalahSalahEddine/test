import os
import requests
from web3 import Web3 # type: ignore
from .gorgumu._db import *
from dotenv import load_dotenv
from decimal import Decimal
from ._connexion import is_online
from cassandra.query import SimpleStatement
load_dotenv()

#infura_url = 'https://mainnet.infura.io/v3/91df789839434f4fb1a03af2f2b60a38' #Replace With Main Network
#w3 = Web3(Web3.HTTPProvider(infura_url))
#CoinWalletAddress = '0x566F7bc73a06DC140B4e9e51c6d0EF6c63224bd8' #Replace With Coin Metamask ETh Address
# Get ETH balance
#eth_balance = w3.eth.get_balance(CoinWalletAddress)
#eth_balance_in_ether = w3.from_wei(eth_balance, 'ether')
# Fetch ETH/USD exchange rate from a reliable source like CoinGecko
#url = "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd"
#response = requests.get(url)
#data = response.json()
#eth_usd_price = data['ethereum']['usd']
#capital_per_currency = eth_balance_in_ether * eth_usd_price
#Using Cassandra Table  Liquidity To Get Circullation Supply
capital_per_currency = 1000
query = SimpleStatement(f"SELECT * FROM gorgumu.Liquidity;")
rows = session.execute(query)
for curculating_supply in rows:
    number_of_units = curculating_supply.circulating
#----------|Calculate GRM Price Action|-------------
Gorgumu_Price = Decimal(capital_per_currency) / number_of_units


