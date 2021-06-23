from bitcoinutils.setup import setup
from bitcoinutils.script import Script
from bitcoinutils.keys import P2wpkhAddress, P2wshAddress, P2shAddress, PrivateKey, PublicKey

def main():
    setup('testnet')

    priv = PrivateKey.from_wif('cVdte9ei2xsVjmZSPtyucG43YZgNkmKTqhwiUA8M4Fc3LdPJxPmZ')

    print("\nPrivate key WIF:", priv.to_wif(compressed=True))

    pub = priv.get_public_key()

    print("Public key:", pub.to_hex(compressed=True))

    address = pub.get_segwit_address()

    print("Native Address:", address.to_string())
    segwit_hash = address.to_hash()
    print("Segwit Hash:", segwit_hash)
    print("Segwit Version:", address.get_type())

    addr2 = P2wpkhAddress.from_hash(segwit_hash)
    print("Created P2wpkhAddress from Segwit Hash and calculate address:")
    print("Native Address:", addr2.to_string())

    addr3 = PrivateKey.from_wif('cTmyBsxMQ3vyh4J3jCKYn2Au7AhTKvqeYuxxkinsg6Rz3BBPrYKK').get_public_key().get_segwit_address()
    addr4 = P2shAddress.from_script(addr3.to_script_pub_key())
    print("P2SH(P2WPKH):", addr4.to_string())

    p2wpkh_key = PrivateKey.from_wif('cNn8itYxAng4xR4eMtrPsrPpDpTdVNuw7Jb6kfhFYZ8DLSZBCg37')
    script = Script(['OP_1', p2wpkh_key.get_public_key().to_hex(), 'OP_1', 'OP_CHECKMULTISIG'])
    p2wsh_addr = P2wshAddress.from_script(script)
    print("P2WSH of P2PK:", p2wsh_addr.to_string() )

    p2sh_p2wsh_addr = P2shAddress.from_script(p2wsh_addr.to_script_pub_key())
    print("P2SH(P2WSH of P2PK):", p2sh_p2wsh_addr.to_string())


if __name__ == "__main__":
    main()