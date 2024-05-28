import requests
import json

def eth_getLogs(rpc_url, from_block, to_block, topics):
    payload = {
        "jsonrpc": "2.0",
        "method": "eth_getLogs",
        "params": [{"fromBlock": from_block, "toBlock": to_block, "topics": topics}],
        "id": 1
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post(rpc_url, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        return response.json()
    else:
        return None

def test_rpc_list(rpc_list, from_block, to_block, topics):
    successful_rpс = []
    for rpc in rpc_list:
        result = eth_getLogs(rpc, from_block, to_block, topics)
        print(result)
        if result is not None and 'error' not in result:
            successful_rpс.append(rpc)
    return successful_rpс

# Example usage
rpc_list = ["https://eth.llamarpc.com","https://eth-mainnet.g.alchemy.com/v2/demo","https://go.getblock.io/d9fde9abc97545f4887f56ae54f3c2c0","https://uk.rpc.blxrbdn.com","https://core.gashawk.io/rpc","https://rpc.eth.gateway.fm","https://endpoints.omniatech.io/v1/eth/mainnet/public","https://eth.drpc.org","https://rpc.builder0x69.io","https://virginia.rpc.blxrbdn.com","https://eth.meowrpc.com","https://eth.rpc.blxrbdn.com","https://ethereum.blockpi.network/v1/rpc/public","https://api.tatum.io/v3/blockchain/node/ethereum-mainnet","https://ethereum-rpc.publicnode.com","https://singapore.rpc.blxrbdn.com","https://rpc.graffiti.farm","https://gateway.tenderly.co/public/mainnet","https://eth1.lava.build/lava-referer-67d3f842-d21f-489d-b4f2-cf902ea4b1e5","https://rpc.flashbots.net/fast","https://eth1.lava.build/lava-referer-ed07f753-8c19-4309-b632-5a4a421aa589","https://rpc.flashbots.net","https://public.stackup.sh/api/v1/node/ethereum-mainnet","https://eth.nodeconnect.org","https://eth1.lava.build/lava-referer-16223de7-12c0-49f3-8d87-e5f1e6a0eb3b","https://eth.merkle.io","https://api.zan.top/node/v1/eth/mainnet/public","https://mainnet.gateway.tenderly.co","https://api.stateless.solutions/ethereum/v1/demo","https://rpc.payload.de","https://rpc.lokibuilder.xyz/wallet","https://eth-mainnet.rpcfast.com?api_key=xbhWBI1Wkguk8SNMu1bvvLurPGLXmgwYeC4S6g2H7WdwFigZSmPWVZRxrskEQwIf","https://eth-mainnet.public.blastapi.io","https://api.securerpc.com/v1","https://cloudflare-eth.com","https://rpc.ankr.com/eth","https://eth-pokt.nodies.app"]
from_block = "0x0"
to_block = "0x2710"
topics = ["0xa123dc29aebf7d0c3322c8eeb5b999e859f39937950ed31056532713d0de396f"]

successful_rpс = test_rpc_list(rpc_list, from_block, to_block, topics)
print("RPCs that did the request successfully:")
print(f'rpc_urls = {successful_rpс}')
