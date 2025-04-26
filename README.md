# bitcoin-timelocks

# pip python-bitcoinrpc

# 1. python3 1_create_wallet_and_addresses.py 
# 2. python3 2_create_p2sh_cltv_p2pkh_address.py --private_key cRvyLwCPLU88jsyj94L7iJjQX5C2f8koG4G2gevN4BeSGcEvfKe9 --future_time 150
# 3. python3 3_send_funds.py
# 4. python3 4_spend_p2sh_csv_p2pkh.py --future_time 150 --p2sh_address 2N8o1x97HdRExwwHzCQ3QfkT5iFAVfB4qMh --private_key cRvyLwCPLU88jsyj94L7iJjQX5C2f8koG4G2gevN4BeSGcEvfKe9 --p2pkh_address_to_send n4bkvTyU1dVdzsrhWBqBw8fEMbHjJvtmJR
