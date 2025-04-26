import argparse
from bitcoinutils.setup import setup
from bitcoinutils.utils import to_satoshis
from bitcoinutils.transactions import Transaction, TxInput, TxOutput, Sequence, Locktime
from bitcoinutils.keys import P2pkhAddress, PrivateKey, P2shAddress
from bitcoinutils.script import Script
from bitcoinutils.constants import TYPE_ABSOLUTE_TIMELOCK
from bitcoinrpc.authproxy import AuthServiceProxy
from decimal import *

def get_all_utxos_of_address(p2sh_address):

    to_addr = P2shAddress(p2sh_address)

    # Connect to Bitcoin Core regtest node via RPC
    rpc_user = "stavros"
    rpc_pass = "1234"
    rpc_connection = AuthServiceProxy(f"http://{rpc_user}:{rpc_pass}@localhost:18443")

    try:
        # Scan UTXO set for the address using its descriptor
        descriptor = f"addr({to_addr.to_string()})"
        scan_result = rpc_connection.scantxoutset("start", [descriptor])

        if scan_result['success'] and scan_result['unspents']:
            return scan_result['unspents']
        else:
            return []

    except Exception as e:
        print("Error:", e)

def createTxInTxOut(txid,vout,amount,seq_for_n_seq,to_addr):

    # create transaction input from tx id of UTXO (contained 11.1 tBTC)
    txin = TxInput(txid, vout, sequence=seq_for_n_seq)

    # send/spend to any random address
    # to_addr = P2pkhAddress("n4bkvTyU1dVdzsrhWBqBw8fEMbHjJvtmJR")
    txout = TxOutput(to_satoshis(amount-Decimal('0.01')), to_addr.to_script_pub_key())        

    return txin,txout

def validate_transaction(raw_tx_hex):
    rpc_user = "stavros"
    rpc_pass = "1234"
    rpc_connection = AuthServiceProxy(f"http://{rpc_user}:{rpc_pass}@localhost:18443")

    result = rpc_connection.testmempoolaccept([raw_tx_hex])
    return result[0]["allowed"]

def send_transaction(raw_tx_hex):
    rpc_user = "stavros"
    rpc_pass = "1234"
    rpc_connection = AuthServiceProxy(f"http://{rpc_user}:{rpc_pass}@localhost:18443")

    result = rpc_connection.sendrawtransaction(raw_tx_hex)
    return result

def main():

    # Parse arguments
    parser = argparse.ArgumentParser(description='Bitcoin core app')
    parser.add_argument('--p2sh_address', action="store", dest='p2sh_address_arg', default=False)
    parser.add_argument('--p2pkh_address_to_send', action="store", dest='p2pkh_address_to_send_arg', default=False)
    parser.add_argument('--private_key', action="store", dest='private_key_arg', default=False)    
    parser.add_argument('--future_time', action="store", dest='future_time_arg', default=False)
    args = parser.parse_args()
    future_time = int(args.future_time_arg)
    to_address = P2pkhAddress(args.p2pkh_address_to_send_arg)

    # always remember to setup the network
    setup("testnet")

    seq = Sequence(TYPE_ABSOLUTE_TIMELOCK,future_time)
    seq_for_n_seq = seq.for_input_sequence()

    # Check if the P2SH address has any UTXOs to get funds from
    utxos = get_all_utxos_of_address(args.p2sh_address_arg)
    txins=[]
    txouts=[]
    if len(utxos)>0:
        for utxo in utxos:
            txin,txout = createTxInTxOut(utxo['txid'],utxo['vout'],utxo['amount'],seq_for_n_seq,to_address)
            txins.append(txin)
            txouts.append(txout)

    # secret key needed to spend P2PKH that is wrapped by P2SH
    p2pkh_sk = PrivateKey(args.private_key_arg)
    p2pkh_pk = p2pkh_sk.get_public_key().to_hex()
    p2pkh_addr = p2pkh_sk.get_public_key().get_address()

    # create the redeem script - needed to sign the transaction
    redeem_script = Script(
        [
            future_time,
            "OP_CHECKLOCKTIMEVERIFY",
            "OP_DROP",
            "OP_DUP",
            "OP_HASH160",
            p2pkh_addr.to_hash160(),
            "OP_EQUALVERIFY",
            "OP_CHECKSIG",
        ]
    )

    # create transaction from inputs/outputs
    # tx = Transaction([txin], [txout], Locktime(future_time).for_transaction())
    tx = Transaction(txins, txouts, Locktime(future_time).for_transaction())

    # print raw transaction
    print("\nRaw unsigned transaction:\n" + tx.serialize())

    # use the private key corresponding to the address that contains the
    # UTXO we are trying to spend to create the signature for the txin -
    # note that the redeem script is passed to replace the scriptSig
    # set the scriptSig (unlocking script) -- unlock the P2PKH (sig, pk) plus
    # the redeem script, since it is a P2SH

    for i, txin in enumerate(txins):
        sig = p2pkh_sk.sign_input(tx, i, redeem_script) 
        txin.script_sig = Script([sig, p2pkh_pk, redeem_script.to_hex()])

    signed_tx = tx.serialize()

    # print raw signed transaction ready to be broadcasted
    print("\nRaw signed transaction:\n" + signed_tx)
    if validate_transaction(signed_tx):
        send_transaction(signed_tx)
        print("\nTxId:", tx.get_txid()," is valid" )


if __name__ == "__main__":
    main()
