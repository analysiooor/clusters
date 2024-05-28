import requests
import json
import time
import os

# Define the chain name
chain_name = 'cro'

# Load the protocol data files
protocols = []
for file in [f for f in os.listdir('.') if f.endswith(f'_{chain_name}.json')]:
    protocol_name = file.replace(f'_{chain_name}.json', '')
    with open(file, 'r') as f:
        protocol_data = json.load(f)
    protocols.append({'name': protocol_name, 'data': protocol_data, 'full_data': []})

# Initialize empty lists to store the results
for protocol in protocols:
    protocol['full_data'] = []

# Set the RPC URL
rpc_url = f'https://cronos.drpc.org'

# Batch size
batch_size = 10

# Maximum number of retries
max_retries = 3

# Process each protocol
for protocol in protocols:
    print(f"Processing {protocol['name']}...")
    for i in range(0, len(protocol['data']), batch_size):
        print(f"Processing {i}/{len(protocol['data'])}")
        batch = protocol['data'][i:i + batch_size]
        tx_hashes = [item[1] for item in batch]

        # Create a list of requests
        reqs = []
        for j, tx_hash in enumerate(tx_hashes):
            req = {
                "jsonrpc": "2.0",
                "method": "eth_getTransactionByHash",
                "params": [tx_hash],
                "id": j
            }
            reqs.append(req)

        # Send the batch request with retries
        retries = 0
        while retries < max_retries:
            try:
                payload = json.dumps(reqs)
                headers = {'Content-Type': 'application/json'}
                response = requests.post(rpc_url, data=payload, headers=headers)
                response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
                data = response.json()
                break
            except requests.exceptions.RequestException as e:
                print(f"Error: {e}. Retrying...")
                retries += 1
                time.sleep(1)  # Wait for 1 second before retrying

        if retries == max_retries:
            print(f"Failed to process batch after {max_retries} retries. Skipping...")
            continue

        # Extract the from address and append to the full list
        for result in data:
            if "result" in result:
                tx_receipt = result["result"]
                if tx_receipt is None or not 'from' in tx_receipt:
                    print('no tx')
                    continue
                from_address = tx_receipt["from"]
                recipient_address = batch[result["id"]][0]
                tx_hash = batch[result["id"]][1]
                protocol['full_data'].append([from_address, recipient_address, tx_hash])
            else:
                print("Error:", result)

    # Save the full data list to protocol_<chain_name>_full.json
    with open(f'{protocol["name"]}_{chain_name}_full.json', 'w') as f:
        json.dump(protocol['full_data'], f)

    print(f"Finished processing {protocol['name']}!")

print("All done!")
