from bitcoinrpc.authproxy import AuthServiceProxy

# Connect to Bitcoin Core regtest node via RPC
rpc_user = "stavros"
rpc_pass = "1234"
rpc_connection = AuthServiceProxy(f"http://{rpc_user}:{rpc_pass}@localhost:18443")

try:

   # Send 10
   tx_id = rpc_connection.sendtoaddress("2N8o1x97HdRExwwHzCQ3QfkT5iFAVfB4qMh", 10)
   print(tx_id)
   # Send 15
   tx_id2 = rpc_connection.sendtoaddress("2N8o1x97HdRExwwHzCQ3QfkT5iFAVfB4qMh", 15)
   print(tx_id2)
   # # Send 5
   # tx_id3 = rpc_connection.sendtoaddress("2N8o1x97HdRExwwHzCQ3QfkT5iFAVfB4qMh", 5)
   # print(tx_id3)

   address = rpc_connection.getnewaddress("my lock4_address", "legacy")
   rpc_connection.generatetoaddress(101, address)

except Exception as e:
    print("Error:", e)