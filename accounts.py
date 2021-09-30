import time 
import json
import random
import argparse
import uuid

import requests 

from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException


with open('config.json','r') as conf:
    configs = json.loads(conf.read())


print(configs)
rpc_user = configs['rpc_user']
rpc_password = configs['rpc_user']

account_pool_endpoint = configs['account_pool_endpoint']


parser = argparse.ArgumentParser(description='Personal information')
parser.add_argument('--speed', dest='speed', type=int, help='how many accounts per minute')

node_name = configs['node_name']
names = configs['names']

# rpc_connection.getnewaddress(node_name)
if __name__ == "__main__":
    args = parser.parse_args()
    while(True):
        rpc_connection = AuthServiceProxy("http://%s:%s@127.0.0.1:18443"%(rpc_user, rpc_password))
        name = random.choice(names)
        uid = uuid.uuid4()
        new_address = rpc_connection.getnewaddress(f'{node_name}.{name}{uid}')
        data = json.dumps({
            "name": f'{node_name}.{name}{uid}',
            "address": new_address
        })
        print(data)
        r = requests.post(f'{account_pool_endpoint}/account',data)
        print(r.text)
        time.sleep(60/args.speed)

    



