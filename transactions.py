from decimal import Decimal
import decimal
import time 
import json
import random
import argparse

import requests 
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException

import logging


with open('config.json','r') as conf:
    configs = json.loads(conf.read())

rpc_user = configs['rpc_user']
rpc_password = configs['rpc_user']

account_pool_endpoint = configs['account_pool_endpoint']


parser = argparse.ArgumentParser(description='configs')
parser.add_argument('--speed', dest='speed', type=int, help='how many accounts per minute')
parser.add_argument('--debug', dest='debug', default=0, type=bool, help='debug')

node_name = configs['node_name']
names = configs['names']




# rpc_connection.getnewaddress(node_name)
if __name__ == "__main__":
        args = parser.parse_args()
        logging.basicConfig()
        logger = logging.getLogger(__name__)


        if args.debug:
            logger.setLevel(logging.DEBUG)

        while(True):
            try:
                rpc_connection = AuthServiceProxy("http://%s:%s@127.0.0.1:18443"%(rpc_user, rpc_password))
            
                listunspent = []
                while(not listunspent):
                    r = requests.get(f'{account_pool_endpoint}/account/{node_name}')
                    sender=r.json()["address"]
                    logger.debug(f"sender: {str(sender)}")
                    listunspent = rpc_connection.listunspent(0,9999,[f"{sender}"])

                    logger.debug(f"unspent:{listunspent}")
                
                unspent = random.choice(listunspent)
                while(unspent["amount"]<0.1):
                    unspent = random.choice(listunspent)

                    

                balance =  unspent['amount']
                logger.debug(f"-------------")
                logger.debug(f"unspent:{unspent}")
                logger.debug(unspent['spendable'])
                if unspent['spendable']:
                    can_spend = 1
                    txid  = unspent['txid']
                    vout = 0
                    amount_to_spend = Decimal(random.uniform(0,float(balance)*0.5))
                    fee = Decimal(0.00001111)
                    change = balance-(amount_to_spend+fee)

                
            
                
                # unspent = random.choice(listunspent)
                # balance =  unspent['amount']
                # logger.debug("balance:",balance)
                # logger.debug("spendable?:",unspent['spendable'])
                # if unspent['spendable']:
                #     txid  = unspent['txid']
                #     vout = 0
                #     amount_to_spend = Decimal(random.uniform(0,float(balance)*0.5))
                #     fee = balance*Decimal(0.05)
                #     change = balance-amount_to_spend-fee
                #     break

                    
                reciever = requests.get(f'{account_pool_endpoint}/account').json()["address"]

                logger.debug(f"amount_to_spend:{amount_to_spend}")
                logger.debug(f"change:{change}")
                logger.debug(f"fee:{fee}")

                rawtransaction =rpc_connection.createrawtransaction(
                    [{"txid":txid,"vout":0}],
                    {reciever:amount_to_spend,sender:change}
                )

                logger.debug(f"rawtransaction:{rawtransaction}")

                privkey = rpc_connection.dumpprivkey(
                    sender
                )
                logger.debug(f"key:{privkey}")

                signed_transaction = rpc_connection.signrawtransactionwithkey(
                    rawtransaction,
                    [privkey]
                )
                logger.debug(f"signed transaction:{signed_transaction}")

                hex = signed_transaction["hex"]
                logger.debug(f"hex:{hex}")
                sent_rawtransaction = rpc_connection.sendrawtransaction(
                    hex
                )

                logger.debug(f"sent_transaction:{sent_rawtransaction}")

                time.sleep(60/args.speed)
            except:
                pass

    



# ./bitcoin-cli createrawtransaction "[{\"txid\":\"2f7aa4499f94371c942d326da5127c8cb15ea97b82c31453338de7eb15844d25\",\"vout\":0}]" "{\"2NBVRHmHS3ReJ7sTQxxAmVHyak9BwWUnxzA\":1.0,\"2N91bwsns4Hd5rLLMVMUVhqut17oq3L96nN\":45.52992940}"

# 0200000001254d8415ebe78d335314c3827ba95eb18c7c12a56d322d941c37949f49a47a2f0000000000ffffffff0200e1f5050000000017a914c8218580adab134ef396f41436d5543af89ce8e887ac28610f0100000017a914acee84e3dc1719d398b82287ccd0db658561cbec8700000000

# ./bitcoin-cli signrawtransactionwithkey "0200000001254d8415ebe78d335314c3827ba95eb18c7c12a56d322d941c37949f49a47a2f0000000000ffffffff0200e1f5050000000017a914c8218580adab134ef396f41436d5543af89ce8e887ac28610f0100000017a914acee84e3dc1719d398b82287ccd0db658561cbec8700000000" "[\"cUCcoPJx2vaKL7CAAPbissa4bLuWivzyCC3JWzGTWhqVYkavc7Yc\"]"

# {
#   "hex": "02000000000101254d8415ebe78d335314c3827ba95eb18c7c12a56d322d941c37949f49a47a2f000000001716001449ca9ac7497e741737f03f8f160b929de23f0924ffffffff0200e1f5050000000017a914c8218580adab134ef396f41436d5543af89ce8e887ac28610f0100000017a914acee84e3dc1719d398b82287ccd0db658561cbec8702473044022068665fa3259cd8e1fa9067ece0a05699546fa65a484d0370da7589311727092402204a5b36dbfe9d9c43df3fc09f971dd1cef28902b08b7354ea860e4f20df9e7965012103bd20c009a1d867482a4d1691d35ee7b7a228046f2c442a42a0b655336237ea0d00000000",
#   "complete": true
# }

# ./bitcoin-cli sendrawtransaction 02000000000101254d8415ebe78d335314c3827ba95eb18c7c12a56d322d941c37949f49a47a2f000000001716001449ca9ac7497e741737f03f8f160b929de23f0924ffffffff0200e1f5050000000017a914c8218580adab134ef396f41436d5543af89ce8e887ac28610f0100000017a914acee84e3dc1719d398b82287ccd0db658561cbec8702473044022068665fa3259cd8e1fa9067ece0a05699546fa65a484d0370da7589311727092402204a5b36dbfe9d9c43df3fc09f971dd1cef28902b08b7354ea860e4f20df9e7965012103bd20c009a1d867482a4d1691d35ee7b7a228046f2c442a42a0b655336237ea0d00000000

# 636620655b14c862b76aeef301029d1d147c559ab1152a137a7c78d7ffb47683

# ./bitcoin-cli listunspent 0 99999 "[\"2NBVRHmHS3ReJ7sTQxxAmVHyak9BwWUnxzA\"]"