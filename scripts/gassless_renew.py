
import json
from eth_account import Account
from eth_account.messages import encode_structured_data  # <-- use encode_structured_data here
from web3 import Web3

# -------------------- USER SETUP --------------------
# TESTNET-only private key
user_private_key = "b6de2b175f123a0fbd3c50e518eada57e66418a749a9b2df252e8be7a3b6a39e"
user = Account.from_key(user_private_key)
print(f"User address: {user.address}")

# Addresses
forwarder_address = "0x497b11C99CB77920EFC63e4a5D7396B3709BcDB3"
membership_contract = "0xAaf086EC89D311f3fcAB1B17A735d4c8D746DFcF"

# REAL Infura Project ID required:
INFURA_PROJECT_ID = "YOUR_INFURA_KEY"
w3 = Web3(Web3.HTTPProvider(f"https://sepolia.infura.io/v3/0dd19889e5b44ef28f8f1c0804a2a784"))

# Load ABIs
with open("build/contracts/NFTMembership.json") as f:
    membership_abi = json.load(f)["abi"]
nft = w3.eth.contract(address=membership_contract, abi=membership_abi)

with open("build/contracts/MinimalForwarder.json") as f:
    forwarder_abi = json.load(f)["abi"]
forwarder = w3.eth.contract(address=forwarder_address, abi=forwarder_abi)

# -------------------- META-TX DETAILS --------------------
token_id = 1
duration_seconds = 30 * 24 * 3600  # 30 days
membership_fee_wei = w3.to_wei("0.01", "ether")  # forwarder can forward ETH if coded
gas_limit = 100000

# Nonce from forwarder
nonce = forwarder.functions.getNonce(user.address).call()

# Encode call data
call_data_hex = nft.encodeABI(
    fn_name="metaRenewMembership",
    args=[token_id, duration_seconds, user.address]
)
call_data_bytes = bytes.fromhex(call_data_hex[2:])

# -------------------- EIP-712 DOMAIN --------------------
domain = {
    "name": "MinimalForwarder",
    "version": "1",
    "chainId": 0,
    "verifyingContract": "0x0000000000000000000000000000000000000000"
}

types = {
    "EIP712Domain": [
        {"name": "name",               "type": "string"},
        {"name": "version",            "type": "string"},
        {"name": "chainId",            "type": "uint256"},
        {"name": "verifyingContract",  "type": "address"}
    ],
    "ForwardRequest": [
        {"name": "from",   "type": "address"},
        {"name": "to",     "type": "address"},
        {"name": "value",  "type": "uint256"},
        {"name": "gas",    "type": "uint256"},
        {"name": "nonce",  "type": "uint256"},
        {"name": "data",   "type": "bytes"}
    ]
}

request = {
    "from": user.address,
    "to": membership_contract,
    "value": membership_fee_wei,
    "gas": gas_limit,
    "nonce": nonce,
    "data": call_data_bytes
}

structured_data = {
    "types": types,
    "domain": domain,
    "primaryType": "ForwardRequest",
    "message": request
}

# -------------------- SIGNING --------------------
encoded_msg = encode_structured_data(primitive=structured_data)  # <--
signed_message = Account.sign_message(encoded_msg, private_key=user_private_key)

signature_hex = signed_message.signature.hex()
print("User script: EIP-712 signature created.")

export_payload = {
    "request": {
        "from": request["from"],
        "to": request["to"],
        "value": str(request["value"]),
        "gas": request["gas"],
        "nonce": request["nonce"],
        "data": call_data_hex
    },
    "signature": signature_hex
}

with open("signed_request.json", "w") as f:
    json.dump(export_payload, f, indent=2)

print("Wrote signed_request.json:")
print(json.dumps(export_payload, indent=2))
