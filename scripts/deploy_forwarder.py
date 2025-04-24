from brownie import MinimalForwarder, accounts

def main():
    # Load deployer account (replace "myDeployerAccount" with your Brownie account alias)
    deployer = accounts.load("myDeployerAccount")
    forwarder = MinimalForwarder.deploy({"from": deployer})
    print(f"Forwarder deployed at: {forwarder.address}")

