import bitcoin.wallet
from bitcoin.core import COIN, b2lx, serialize, x, lx, b2x
from utils import *
from bitcoin.core.script import *

bitcoin.SelectParams("testnet")
my_private_key = bitcoin.wallet.CBitcoinSecret("91fvmHgYAUbWLvYFNh6XVf41v2FBEPBbfTWRbXzBZ4tJuBpLrSk")
my_public_key = my_private_key.pub
my_address = bitcoin.wallet.P2PKHBitcoinAddress.from_pubkey(my_public_key)
destination_privkey = [bitcoin.wallet.CBitcoinSecret('92UWGcga2spQvdxbnRfi8CSwqkoU5p5X6PZmNw8TLpiT3GUVxGq'),
                    bitcoin.wallet.CBitcoinSecret('91mTV3ZqxgKGpwfTKQy2sMnnWKJHYaZNiSf5s2X6NzsiRMFzx7e'),
                    bitcoin.wallet.CBitcoinSecret('92r3GRWcM4vgWDS9TNCTWFdKXsn7APDeBKvvec1kcLwYXj128Ur')]
destination_pubkey = [destination_privkey[0].pub,
                    destination_privkey[1].pub,
                    destination_privkey[2].pub]

def P2PKH_scriptPubKey_(destination_pubkey):
    return [my_public_key, OP_CHECKSIGVERIFY, OP_2, destination_pubkey[0], destination_pubkey[1], destination_pubkey[2], OP_3, OP_CHECKMULTISIG]

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
    amount_to_send = 0.0107006 # 0.01080060 - 0.0001
    txid_to_spend = ('852c9e863ddee205720ab7031d5e562692ddc07fc0e96649b9a47c2ed9ecb208')
    utxo_index = 0

    print(my_address)
    print(my_public_key.hex())
    print(my_private_key.hex())
    txout_scriptPubKey = P2PKH_scriptPubKey_(destination_pubkey)
    response = send_from_P2PKH_transaction(amount_to_send, txid_to_spend, utxo_index, txout_scriptPubKey)
    print(response.status_code, response.reason)
    print(response.text)