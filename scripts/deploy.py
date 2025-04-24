import os
from brownie import NFTMembership, accounts, network, config

def main():
    # Option A: Load Brownie account by alias
    deployer = accounts.load("myDeployerAccount")
    
    # Option B: Alternatively, add private key from env variable
    # deployer = accounts.add(os.getenv("PRIVATE_KEY"))

    forwarder_address = "0x497b11C99CB77920EFC63e4a5D7396B3709BcDB3"

    # Example: membershipPrice = 0.01 ETH => 10**16 wei
    membershipPrice = 10**16  # 0.01 ETH in Wei

    # Typical transaction parameters
    tx_params = {"from": deployer, "gas_limit": 3_000_000, "allow_revert": True}

    # Deploy
    deployed_contract = NFTMembership.deploy(
        "MembershipPass",     # _name
        "MBR",                # _symbol
        membershipPrice,      # initialPrice
        forwarder_address,    # forwarder
        tx_params
    )

    print(f"NFTMembership deployed at: {deployed_contract.address}")

