import requests
import json
import time

def test_rpc_batch(rpc_url, tx_hash):
    max_batch_size = 0
    for batch_size in [1, 2, 3, 5, 10, 15, 20, 25, 30, 50, 75, 100, 150, 200, 250, 300, 500, 1000]:
        reqs = []
        for i in range(batch_size):
            req = {
                "jsonrpc": "2.0",
                "method": "eth_getTransactionByHash",
                "params": [tx_hash],
                "id": i
            }
            reqs.append(req)
        payload = json.dumps(reqs)
        headers = {'Content-Type': 'application/json'}
        start_time = time.time()
        response = requests.post(rpc_url, data=payload, headers=headers)
        end_time = time.time()
        request_time = end_time - start_time
        if response.status_code == 200:
            max_batch_size = batch_size
        else:
            break
    return max_batch_size, request_time

def test_rpc_list(rpc_list, tx_hash):
    for rpc in rpc_list:
        max_batch_size, request_time = test_rpc_batch(rpc, tx_hash)
        print(f"RPC {rpc} supports up to {max_batch_size} batch size, last request took {request_time:.2f} seconds")

# Example usage
rpc_list = ["https://api.tatum.io/v3/blockchain/node/avax-mainnet", "https://avalanche-c-chain-rpc.publicnode.com", "https://avalanche.drpc.org", "https://api.avax.network/ext/bc/C/rpc", "https://avalanche.blockpi.network/v1/rpc/public", "https://endpoints.omniatech.io/v1/avax/mainnet/public", "https://avax-pokt.nodies.app/ext/bc/C/rpc", "https://api.zan.top/node/v1/avax/mainnet/public/ext/bc/C/rpc", "https://1rpc.io/avax/c", "https://avax.meowrpc.com", "https://ava-mainnet.public.blastapi.io/ext/bc/C/rpc", "https://rpc.ankr.com/avalanche", "https://avalanche.public-rpc.com", "https://avalanche.api.onfinality.io/public/ext/bc/C/rpc", "https://public.stackup.sh/api/v1/node/avalanche-mainnet"]
tx_hash = "0x1d06a9d52255a2a4385d55093aec7671f3d7f6d83d4cd438991be8b6588e9b91"

test_rpc_list(rpc_list, tx_hash)
