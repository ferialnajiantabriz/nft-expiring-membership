from brownie import NFTMembership, accounts, network, config
from dotenv import load_dotenv
import os

def main():
    load_dotenv()  # loads variables from .env
    private_key = os.getenv("PRIVATE_KEY")

    account = accounts.add(private_key)

    nft_contract = NFTMembership.deploy(
        "MembershipPass",
        "MBR",
        10**16,  # 0.01 ETH
        {"from": account},
        publish_source=False  # or True if verifying on Etherscan
    )
    print(f"Deployed at: {nft_contract.address}")
