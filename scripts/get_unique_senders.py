import csv
import json

# Read the CSV file
with open('2024-05-15-snapshot1_transactions.csv', 'r') as f:
    reader = csv.DictReader(f)
    rows = list(reader)

# Extract the list of unique sender wallets
senders = set()
for row in rows:
    senders.add(row['SENDER_WALLET'])

# Write the list of senders to a JSON file
with open('senders.json', 'w') as f:
    json.dump(list(senders), f)
