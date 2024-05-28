import requests
import json

topics = ["0xcba69f43792f9f399347222505213b55af8e0b0b54b893085c2e27ecbe1644f1"]
rpc_urls = ['https://eth.llamarpc.com', 'https://eth-mainnet.g.alchemy.com/v2/demo', 'https://core.gashawk.io/rpc', 'https://rpc.eth.gateway.fm', 'https://endpoints.omniatech.io/v1/eth/mainnet/public', 'https://eth.drpc.org', 'https://rpc.builder0x69.io', 'https://eth.meowrpc.com', 'https://api.tatum.io/v3/blockchain/node/ethereum-mainnet', 'https://rpc.graffiti.farm', 'https://gateway.tenderly.co/public/mainnet', 'https://eth1.lava.build/lava-referer-67d3f842-d21f-489d-b4f2-cf902ea4b1e5', 'https://rpc.flashbots.net/fast', 'https://eth1.lava.build/lava-referer-ed07f753-8c19-4309-b632-5a4a421aa589', 'https://rpc.flashbots.net', 'https://eth.nodeconnect.org', 'https://eth1.lava.build/lava-referer-16223de7-12c0-49f3-8d87-e5f1e6a0eb3b', 'https://eth.merkle.io', 'https://mainnet.gateway.tenderly.co', 'https://api.stateless.solutions/ethereum/v1/demo', 'https://rpc.payload.de', 'https://eth-mainnet.rpcfast.com?api_key=xbhWBI1Wkguk8SNMu1bvvLurPGLXmgwYeC4S6g2H7WdwFigZSmPWVZRxrskEQwIf', 'https://api.securerpc.com/v1', 'https://eth-pokt.nodies.app']
current_rpc_index = 0

result = []

# Get the current block number
params = {
    "jsonrpc": "2.0",
    "method": "eth_blockNumber",
    "params": [],
    "id": 1
}

try:
    response = requests.post(rpc_urls[current_rpc_index], json=params)
    response_json = response.json()
    if "result" in response_json:
        current_block_number = int(response_json["result"], 16)
    else:
        print("Error:", response_json)
        current_block_number = 0
except Exception as e:
    print("Error getting current block number:", str(e))
    current_block_number = 0

block_number = 0
while block_number < current_block_number:
    params = {
        "jsonrpc": "2.0",
        "method": "eth_getLogs",
        "params": [
            {
                "fromBlock": hex(block_number),
                "toBlock": hex(min(block_number + 9999, current_block_number)),
                "topics": topics
            }
        ],
        "id": 1
    }

    try:
        response = requests.post(rpc_urls[current_rpc_index], json=params)
        if response.status_code == 200:
            response_json = response.json()
            if "result" in response_json:
                logs = response_json["result"]
                for log in logs:
                    data = log["data"]
                    recipient = "0x" + data[410:450]  # extract recipient from data
                    tx_hash = log["transactionHash"]
                    result.append((recipient, tx_hash))
                block_number += 10000
                with open('lifi_eth.json', 'w') as f:
                    json.dump(result, f)
                print(f"Saved batch to lifi.json, block number: {block_number}")
            else:
                print("Error:", response_json)
        else:
            print("Error:", response.status_code)
    except Exception as e:
        print("Error getting logs:", str(e))

    # Alternate between RPC endpoints
    current_rpc_index = (current_rpc_index + 1) % len(rpc_urls)

print("Finished!")
