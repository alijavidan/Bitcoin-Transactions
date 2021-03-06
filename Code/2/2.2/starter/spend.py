from sys import exit
from bitcoin.core.script import *
from utils import *
from transaction import (destination_privkey, destination_pubkey, P2PKH_scriptPubKey, P2PKH_scriptPubKey_, my_address, my_private_key)

def multisig_scriptSig(txin, txout, txin_scriptPubKey):
    bank_sig = create_OP_CHECKSIG_signature(txin, txout, txin_scriptPubKey,  my_private_key)
    cust1_sig = create_OP_CHECKSIG_signature(txin, txout, txin_scriptPubKey, destination_privkey[0])
    cust2_sig = create_OP_CHECKSIG_signature(txin, txout, txin_scriptPubKey, destination_privkey[1])
    cust3_sig = create_OP_CHECKSIG_signature(txin, txout, txin_scriptPubKey, destination_privkey[2])

    return [OP_0, cust1_sig, cust2_sig, bank_sig]



def send_from_multisig_transaction(amount_to_send, txid_to_spend, utxo_index, txin_scriptPubKey, txout_scriptPubKey):
    txout = create_txout(amount_to_send, txout_scriptPubKey)
    txin = create_txin(txid_to_spend, utxo_index)
    txin_scriptSig = multisig_scriptSig(txin, txout, txin_scriptPubKey)
    new_tx = create_signed_transaction(txin, txout, txin_scriptPubKey, txin_scriptSig)

    return broadcast_transaction(new_tx)

if __name__ == '__main__':

    amount_to_send = 0.0106006 # 0.01070060 - 0.0001
    txid_to_spend = 'a2e495c17f3408416f0abbfe94934b0c3268df3ff99fa2cf77110bd5846a2a8d'
    utxo_index = 0

    txin_scriptPubKey = P2PKH_scriptPubKey_(destination_pubkey)
    txout_scriptPubKey = P2PKH_scriptPubKey(my_address)

    response = send_from_multisig_transaction(
        amount_to_send, txid_to_spend, utxo_index,
        txin_scriptPubKey, txout_scriptPubKey)
    print(response.status_code, response.reason)
    print(response.text)
