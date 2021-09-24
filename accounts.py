import time 
import json
import random
import argparse

import requests 

from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException

rpc_user = '123'
rpc_password = '123'

account_pool_endpoint = "http://localhost:80/wallet"
rpc_connection = AuthServiceProxy("http://%s:%s@127.0.0.1:18443"%(rpc_user, rpc_password))

parser = argparse.ArgumentParser(description='Personal information')
parser.add_argument('--speed', dest='speed', type=int, help='how many accounts per minute')

node_name = 'nodoTest'
name = "name"

# rpc_connection.getnewaddress(node_name)
if __name__ == "__main__":
    args = parser.parse_args()
    while(True):
        count = 1
        new_address = rpc_connection.getnewaddress(f'{node_name}.{name}{count}')
        data = json.dumps({
            "name": f'{node_name}.{name}{count}',
            "address": new_address
        })
        print(data)
        r = requests.post(account_pool_endpoint,data)
        print(r.text)
        time.sleep(60/args.speed)

    



