import json
import csv

def main():
    # Load the files
    files = [
        'across_arb_full.json', 'across_avax_full.json', 'across_base_full.json', 'across_bsc_full.json', 'across_cro_full.json', 'across_eth_full.json', 'across_ftm_full.json', 'across_linea_full.json', 'across_mantle_full.json', 'across_poly_full.json',
        'connext_arb_full.json', 'connext_avax_full.json', 'connext_base_full.json', 'connext_bsc_full.json', 'connext_cro_full.json', 'connext_eth_full.json', 'connext_ftm_full.json', 'connext_linea_full.json', 'connext_mantle_full.json', 'connext_op_full.json', 'connext_poly_full.json',
        'hop_arb_full.json', 'hop_avax_full.json', 'hop_base_full.json', 'hop_bsc_full.json', 'hop_cro_full.json', 'hop_eth_full.json', 'hop_ftm_full.json', 'hop_linea_full.json', 'hop_mantle_full.json', 'hop_op_full.json', 'hop_poly_full.json',
        'lifi_arb_full.json', 'lifi_avax_full.json', 'lifi_base_full.json', 'lifi_bsc_full.json', 'lifi_cro_full.json', 'lifi_eth_full.json', 'lifi_ftm_full.json', 'lifi_linea_full.json', 'lifi_mantle_full.json', 'lifi_op_full.json', 'lifi_poly_full.json',
        'stargate_arb_full.json', 'stargate_avax_full.json', 'stargate_base_full.json', 'stargate_bsc_full.json', 'stargate_cro_full.json', 'stargate_eth_full.json', 'stargate_ftm_full.json', 'stargate_linea_full.json', 'stargate_mantle_full.json', 'stargate_op_full.json', 'stargate_poly_full.json'
    ]

    print("Files loaded")

    # Create a dictionary to map file names to protocols and chains
    file_map = {
        'across_arb_full.json': ('across', 'arb'),
        'across_avax_full.json': ('across', 'avax'),
        'across_base_full.json': ('across', 'base'),
        'across_bsc_full.json': ('across', 'bsc'),
        'across_cro_full.json': ('across', 'cro'),
        'across_eth_full.json': ('across', 'eth'),
        'across_ftm_full.json': ('across', 'ftm'),
        'across_linea_full.json': ('across', 'linea'),
        'across_mantle_full.json': ('across', 'mantle'),
        'across_poly_full.json': ('across', 'poly'),
        'connext_arb_full.json': ('connext', 'arb'),
        'connext_avax_full.json': ('connext', 'avax'),
        'connext_base_full.json': ('connext', 'base'),
        'connext_bsc_full.json': ('connext', 'bsc'),
        'connext_cro_full.json': ('connext', 'cro'),
        'connext_eth_full.json': ('connext', 'eth'),
        'connext_ftm_full.json': ('connext', 'ftm'),
        'connext_linea_full.json': ('connext', 'linea'),
        'connext_mantle_full.json': ('connext', 'mantle'),
        'connext_op_full.json': ('connext', 'op'),
        'connext_poly_full.json': ('connext', 'poly'),
        'hop_arb_full.json': ('hop', 'arb'),
        'hop_avax_full.json': ('hop', 'avax'),
        'hop_base_full.json': ('hop', 'base'),
        'hop_bsc_full.json': ('hop', 'bsc'),
        'hop_cro_full.json': ('hop', 'cro'),
        'hop_eth_full.json': ('hop', 'eth'),
        'hop_ftm_full.json': ('hop', 'ftm'),
        'hop_linea_full.json': ('hop', 'linea'),
        'hop_mantle_full.json': ('hop', 'mantle'),
        'hop_op_full.json': ('hop', 'op'),
        'hop_poly_full.json': ('hop', 'poly'),
        'lifi_arb_full.json': ('lifi', 'arb'),
        'lifi_avax_full.json': ('lifi', 'avax'),
        'lifi_base_full.json': ('lifi', 'base'),
        'lifi_bsc_full.json': ('lifi', 'bsc'),
        'lifi_cro_full.json': ('lifi', 'cro'),
        'lifi_eth_full.json': ('lifi', 'eth'),
        'lifi_ftm_full.json': ('lifi', 'ftm'),
        'lifi_linea_full.json': ('lifi', 'linea'),
        'lifi_mantle_full.json': ('lifi', 'mantle'),
        'lifi_op_full.json': ('lifi', 'op'),
        'lifi_poly_full.json': ('lifi', 'poly'),
        'stargate_arb_full.json': ('stargate', 'arb'),
        'stargate_avax_full.json': ('stargate', 'avax'),
        'stargate_base_full.json': ('stargate', 'base'),
        'stargate_bsc_full.json': ('stargate', 'bsc'),
        'stargate_cro_full.json': ('stargate', 'cro'),
        'stargate_eth_full.json': ('stargate', 'eth'),
        'stargate_ftm_full.json': ('stargate', 'ftm'),
        'stargate_linea_full.json': ('stargate', 'linea'),
        'stargate_mantle_full.json': ('stargate', 'mantle'),
        'stargate_op_full.json': ('stargate', 'op'),
        'stargate_poly_full.json': ('stargate', 'poly')
    }

    print("File map created")

    # Process the data
    result = []
    for file in files:
        with open(file, 'r') as f:
            data = json.load(f)
            for row in data:
                from_addr, to_addr, tx_hash = row
                if from_addr == '0x0000000000000000000000000000000000000000' or to_addr == '0x0000000000000000000000000000000000000000':
                    continue
                protocol, chain = file_map[file]
                pair = tuple(sorted([from_addr, to_addr]))
                result.append((pair, (tx_hash, protocol, chain)))

    # Create pairs and links
    pairs = set()
    links = {}
    for pair, link in result:
        pairs.add(pair)
        if pair not in links:
            links[pair] = []
        links[pair].append(link)

    # Load the senders data
    with open('senders.json', 'r') as f:
        senders = set(json.load(f))

    # Load the initialList.csv file
    with open('initialList.csv', 'r') as f:
        reader = csv.reader(f)
        initial_list = set(row[0] for row in reader)

    # Remove addresses present in initialList.csv from senders
    senders -= initial_list

    # Create a graph where each sender is a node, and two nodes are connected if they have a pair in pairs
    graph = {}
    for pair in pairs:
        addr1, addr2 = pair
        if addr1 in senders and addr2 in senders:
            if addr1 not in graph:
                graph[addr1] = set()
            if addr2 not in graph:
                graph[addr2] = set()
            graph[addr1].add(addr2)
            graph[addr2].add(addr1)

    # Perform a depth-first search to find clusters of >= 20 addresses
    def dfs(node, visited, cluster):
        visited.add(node)
        cluster.add(node)
        for neighbor in graph.get(node, set()):
            if neighbor not in visited:
                dfs(neighbor, visited, cluster)

    clusters = []
    visited = set()
    for node in graph:
        if node not in visited:
            cluster = set()
            dfs(node, visited, cluster)
            if len(cluster) >= 20:
                cluster_links = {}
                for addr1 in cluster:
                    for addr2 in cluster:
                        if addr1 != addr2:
                            pair = tuple(sorted([addr1, addr2]))
                            if pair in links:
                                cluster_links[f'{addr1}-{addr2}'] = links[pair]
                clusters.append((list(cluster), cluster_links))

    # Save the clusters to a file
    with open('clusters_detailed.json', 'w') as f:
        json.dump(clusters, f)

if __name__ == '__main__':
    main()
