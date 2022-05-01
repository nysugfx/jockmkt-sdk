from client import Client
import sys
import requests
sys.path.insert(1, "/Users/alexfriedman/Documents/JockMKT Trading Scripts")
from jock_key import secret_key, api_key

client = Client(secret_key, api_key)

for i in range(1):
    client.place_order('tdbl_626379d38245ff282ea263ef8e7523a7', price=1.10, qty=1)

