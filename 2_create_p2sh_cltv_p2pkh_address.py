import argparse
import sys
from bitcoinutils.setup import setup
from bitcoinutils.transactions import Sequence
from bitcoinutils.keys import P2shAddress, PrivateKey
from bitcoinutils.script import Script

def main():

    p2pkh_addr=''

    # Parse arguments
    parser = argparse.ArgumentParser(description='Bitcoin core app')
    parser.add_argument('--publickey', action="store", dest='public_key_arg', default=False)
    parser.add_argument('--private_key', action="store", dest='private_key_arg', default=False)    
    parser.add_argument('--future_time', action="store", dest='future_time_arg', default=False)
    args = parser.parse_args()

    if not args.public_key_arg and not args.private_key_arg:
        sys.stdout.write('Missing public or private key\n')
        return

    if args.public_key_arg:
        p2pkh_addr = args.public_key_arg.get_address()
    elif args.private_key_arg:
        p2pkh_sk = PrivateKey(args.private_key_arg)
        p2pkh_addr = p2pkh_sk.get_public_key().get_address()

    # always remember to setup the network
    setup("testnet")

    # create the redeem script
    redeem_script = Script(
        [
            int(args.future_time_arg),
            "OP_CHECKLOCKTIMEVERIFY",
            "OP_DROP",
            "OP_DUP",
            "OP_HASH160",
            p2pkh_addr.to_hash160(),
            "OP_EQUALVERIFY",
            "OP_CHECKSIG",
        ]
    )

    # create a P2SH address from a redeem script
    addr = P2shAddress.from_script(redeem_script)
    print(addr.to_string())
    # print(p2pkh_addr.to_string())

if __name__ == "__main__":
    main()
