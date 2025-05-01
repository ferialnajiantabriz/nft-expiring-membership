# import os
# import json
# from eth_account import Account
# from eth_account.messages import encode_structured_data
# from web3 import Web3
#
# def main():
#     """
#     This script:
#       1) Loads addresses and keys (currently hard-coded, but you can adapt).
#       2) Creates an EIP-712 structured data object for metaRenewMembership.
#       3) Signs it with the user’s private key.
#       4) Outputs a signed_request.json for the relayer to use.
#     NOTE: This script does NOT execute the transaction on-chain; it only signs it.
#     """
#
#     # ----------------- STEP 1: Setup Web3 & addresses ---------------
#     # If you want to read from environment, uncomment and use os.getenv calls:
#     # INFURA_PROJECT_ID = os.getenv("INFURA_PROJECT_ID")
#     # user_private_key = os.getenv("USER_PRIVATE_KEY")
#     # forwarder_address = os.getenv("FORWARDER_ADDRESS")
#     # membership_contract = os.getenv("MEMBERSHIP_ADDRESS")
# import os
# import json
# from eth_account import Account
# from eth_account.messages import encode_structured_data
# from web3 import Web3
#
# def main():
#     """
#     This script:
#       1) Hard-codes addresses and a user private key
#          (or read from .env if you prefer).
#       2) Creates a metaRenewMembership call in hex form,
#          then converts it to bytes for EIP-712 hashing.
#       3) Builds the EIP-712 'ForwardRequest' object,
#          specifying 'data' as a bytes object, not a string.
#       4) Signs the structured data, then outputs signed_request.json
#          with both the raw bytes (for EIP-712)
#          and the hex version (for reference).
#     """
#
#     # ----------------- STEP 1: Setup ---------------
#     INFURA_PROJECT_ID = "0dd19889e5b44ef28f8f1c0804a2a784"
#     user_private_key = "ad8022ffb47857ff37f093002448f41323f21ec252467d3a8c63c7efc72f927a"
#     forwarder_address = "0x523A5FaF22E7696a53C7C1c1412770E859A685E6"
#     membership_contract = "0xA4bb4e1F3787a2A3C907BF7d751008f0e9b25971"
#
#     w3 = Web3(Web3.HTTPProvider(f"https://sepolia.infura.io/v3/{INFURA_PROJECT_ID}"))
#     user = Account.from_key(user_private_key)
#     print(f"User address: {user.address}")
#
#     token_id = 1
#     duration_seconds = 30 * 24 * 3600  # 30 days
#     membership_fee_wei = w3.to_wei("0.01", "ether")
#     gas_limit = 100000
#     nonce = 0  # Or fetch real nonce from forwarder if needed
#
#     # Hard-coded call data for metaRenewMembership(uint256, uint256, address)
#     #   function selector: 0x48ce240c
#     #   tokenId = 1
#     #   additionalTime = 0x278d00 (2592000 decimal => 30 days)
#     #   realUser = 0x816ca99BE0ba877bD780332B446D5ABC30285a31
#     call_data_hex = (
#         "0x48ce240c"
#         "0000000000000000000000000000000000000000000000000000000000000001" # tokenId=1
#         "0000000000000000000000000000000000000000000000000000000000278d00" # duration=30 days
#         "000000000000000000000000816ca99be0ba877bd780332b446d5abc30285a31" # realUser
#     )
#
#     # Convert that hex string into *bytes*
#     call_data_bytes = bytes.fromhex(call_data_hex[2:])
#
#     # ----------------- STEP 2: EIP-712 domain & message --------------
#     domain = {
#         "name": "MinimalForwarder",
#         "version": "1",
#         "chainId": 11155111,  # Sepolia chain ID
#         "verifyingContract": forwarder_address
#     }
#
#     # We say "data" is type "bytes" => must be a python bytes object
#     types = {
#         "EIP712Domain": [
#             {"name": "name", "type": "string"},
#             {"name": "version", "type": "string"},
#             {"name": "chainId", "type": "uint256"},
#             {"name": "verifyingContract", "type": "address"}
#         ],
#         "ForwardRequest": [
#             {"name": "from", "type": "address"},
#             {"name": "to", "type": "address"},
#             {"name": "value", "type": "uint256"},
#             {"name": "gas", "type": "uint256"},
#             {"name": "nonce", "type": "uint256"},
#             {"name": "data", "type": "bytes"}
#         ]
#     }
#
#     request = {
#         "from": user.address,
#         "to": membership_contract,
#         "value": membership_fee_wei,
#         "gas": gas_limit,
#         "nonce": nonce,
#         "data": call_data_bytes  # *bytes*, not string
#     }
#
#     structured_data = {
#         "types": types,
#         "domain": domain,
#         "primaryType": "ForwardRequest",
#         "message": request
#     }
#
#     # ----------------- STEP 3: Sign the EIP-712 data --------------
#     encoded_msg = encode_structured_data(structured_data)
#     signed_message = Account.sign_message(encoded_msg, private_key=user_private_key)
#     signature_hex = signed_message.signature.hex()
#
#     print("User script: EIP-712 signature created.")
#
#     # We'll store the final JSON. But "request['data']" is bytes in memory.
#     # For clarity, we'll store the hex representation of that bytes in the final file:
#     request_hex = {
#         "from": user.address,
#         "to": membership_contract,
#         "value": str(membership_fee_wei),
#         "gas": gas_limit,
#         "nonce": nonce,
#         "data": call_data_hex  # the original "0x48ce240c..." string
#     }
#
#     export_payload = {
#         "request": request_hex,
#         "signature": signature_hex
#     }
#
#     # Write to signed_request.json
#     with open("signed_request.json", "w") as f:
#         json.dump(export_payload, f, indent=2)
#
#     print("Wrote signed_request.json:")
#     print(json.dumps(export_payload, indent=2))


import os
import json
from eth_account import Account
from eth_account.messages import encode_structured_data
from web3 import Web3

def main():
    """
    1) Hard-codes or loads user private key
    2) Creates EIP-712 ForwardRequest for metaRenewMembership
    3) Domain EXACTLY matches your forwarder code:
       name="MinimalForwarder", version="1", chainId=0, verifyingContract=0x0000000000000000000000000000000000000000
    4) The request object also must match your forwarder logic
    5) Writes 'signed_request.json' with the signature
    """

    # --- Step 1: Basic Setup (could read from .env) ---
    INFURA_PROJECT_ID = os.getenv("INFURA_PROJECT_ID", "YOUR_INFURA_KEY")
    user_private_key = os.getenv("USER_PRIVATE_KEY", "0xb6de2b...")
    # no leading 0x is fine if the library can parse it, but typically we do "0x..."
    forwarder_address = os.getenv("FORWARDER_ADDRESS", "<not actually used in domain>")
    membership_contract = os.getenv("MEMBERSHIP_ADDRESS", "0xA4bb4e1F3787...")

    # We'll connect to Sepolia just to do things like w3.toWei
    w3 = Web3(Web3.HTTPProvider(f"https://sepolia.infura.io/v3/{INFURA_PROJECT_ID}"))

    user = Account.from_key(user_private_key)
    print(f"User address: {user.address}\n")

    # --- Step 2: Our minimal data for metaRenewMembership ---
    token_id = 1
    duration_seconds = 30*24*3600
    membership_fee_wei = w3.to_wei("0.01", "ether")
    gas_limit = 100000
    nonce = 0  # if your forwarder is getNonce() logic, we do 0 for now

    # This is your metaRenewMembership function selector + param encoding
    # 0x48ce240c = metaRenewMembership(uint256,uint256,address)
    # We'll paste the last param as user.address
    # Make sure user.address has no uppercase.
    user_addr_no0x = user.address.lower().replace("0x","")

    call_data_hex = (
        "0x48ce240c" 
        "0000000000000000000000000000000000000000000000000000000000000001"  # tokenId=1
        "0000000000000000000000000000000000000000000000000000000000278d00"  # ~30 days
        "000000000000000000000000" + user_addr_no0x  # realUser
    )
    # Convert to bytes for the EIP-712
    call_data_bytes = bytes.fromhex(call_data_hex[2:])

    # --- Step 3: EIP-712 domain EXACTLY as per your forwarder code ---
    # Your forwarder uses "MinimalForwarder", "1", chainId=0, address(0)
    # -> See lines in _hashTypedData where it sets chainId=0, verifyingContract=address(0)
    domain = {
        "name": "MinimalForwarder",
        "version": "1",
        "chainId": 0,
        "verifyingContract": "0x0000000000000000000000000000000000000000"
    }

    types = {
        "EIP712Domain": [
            {"name": "name", "type": "string"},
            {"name": "version", "type": "string"},
            {"name": "chainId", "type": "uint256"},
            {"name": "verifyingContract", "type": "address"}
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

    # --- Step 4: Sign using EIP-712 approach ---
    encoded_msg = encode_structured_data(structured_data)
    signed = Account.sign_message(encoded_msg, private_key=user_private_key)
    signature_hex = signed.signature.hex()

    print("User script: EIP-712 signature created.\n")

    # We'll store 'data' as hex in the final JSON
    request_hex = {
        "from": request["from"],
        "to": request["to"],
        "value": str(request["value"]),
        "gas": request["gas"],
        "nonce": request["nonce"],
        "data": call_data_hex  # revert to the "0x48ce..." for the JSON
    }

    export_payload = {
        "request": request_hex,
        "signature": signature_hex
    }

    with open("signed_request.json","w") as f:
        json.dump(export_payload, f, indent=2)

    print("Wrote signed_request.json:")
    print(json.dumps(export_payload, indent=2))
