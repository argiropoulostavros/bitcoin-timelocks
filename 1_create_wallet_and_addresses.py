from bitcoinrpc.authproxy import AuthServiceProxy

# Connect to Bitcoin Core regtest node via RPC
rpc_user = "stavros"
rpc_pass = "1234"
rpc_connection = AuthServiceProxy(f"http://{rpc_user}:{rpc_pass}@localhost:18443")

try:

   # Create wallet
   response = rpc_connection.createwallet(
        "stavros_wallet", 
        False, 
        False, 
        "", 
        False, 
        False,  # descriptors=False
        True    # load_on_startup=True
    )
   print("Wallet created:", response)
   
   # Create address 1
   address = rpc_connection.getnewaddress("my lock1_address", "legacy")
   print("Legacy Address:", address)

   # Create address 2
   address2 = rpc_connection.getnewaddress("my lock2_address", "legacy")
   print("Legacy Address:", address2)

   # Create address 3
   address3 = rpc_connection.getnewaddress("my lock3_address", "legacy")
   print("Legacy Address:", address3)

   rpc_connection.generatetoaddress(50, address)
   rpc_connection.generatetoaddress(50, address2)
   rpc_connection.generatetoaddress(50, address3)

except Exception as e:
    print("Error:", e)