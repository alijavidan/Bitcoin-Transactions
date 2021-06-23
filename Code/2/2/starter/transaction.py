import bitcoin.wallet
from bitcoin.core import COIN, b2lx, serialize, x, lx, b2x
from utils import *

from bitcoin.core.script import *

bitcoin.SelectParams("testnet")
my_private_key = bitcoin.wallet.CBitcoinSecret("91fvmHgYAUbWLvYFNh6XVf41v2FBEPBbfTWRbXzBZ4tJuBpLrSk")
my_public_key = my_private_key.pub
my_address = bitcoin.wallet.P2PKHBitcoinAddress.from_pubkey(my_public_key)
destination_address = bitcoin.wallet.CBitcoinAddress('mq8F9UnWfVtVAhgpZN89qjRLy3n9eG4Ssw')

def P2PKH_scriptPubKey(address):
    return [OP_DUP, OP_HASH160, address, OP_EQUALVERIFY, OP_CHECKSIG]

def P2PKH_scriptSig(txin, txout, txin_scriptPubKey):
    signature = create_OP_CHECKSIG_signature(txin, txout, txin_scriptPubKey, my_private_key)

    return [signature, my_public_key]

def send_from_P2PKH_transaction(amount_to_send, txid_to_spend, utxo_index, txout_scriptPubKey):
    txout = create_txout(amount_to_send, txout_scriptPubKey)

    txin_scriptPubKey = P2PKH_scriptPubKey(my_address)
    txin = create_txin(txid_to_spend, utxo_index)
    txin_scriptSig = P2PKH_scriptSig(txin, txout, txin_scriptPubKey)

    new_tx = create_signed_transaction(txin, txout, txin_scriptPubKey, txin_scriptSig)

    return broadcast_transaction(new_tx)



if __name__ == '__main__':
    amount_to_send = 0.0008 # 0.00090000 - 0.0001
    txid_to_spend = ('27709b1361d279ade8e85fe7d4fb62948068f5f9be6d88fc83536b3197578fbd')
    utxo_index = 0

    print(my_address)
    print(my_public_key.hex())
    print(my_private_key.hex())
    txout_scriptPubKey = P2PKH_scriptPubKey(destination_address)
    response = send_from_P2PKH_transaction(amount_to_send, txid_to_spend, utxo_index, txout_scriptPubKey)
    print(response.status_code, response.reason)
    print(response.text)