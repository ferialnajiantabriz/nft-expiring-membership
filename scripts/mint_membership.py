from brownie import NFTMembership, accounts

def main():
    deployer = accounts.load("myDeployerAccount")
    contract = NFTMembership.at("0xAaf086EC89D311f3fcAB1B17A735d4c8D746DFcF")

    recipient = deployer.address
    duration = 30 * 24 * 60 * 60  # 30 days in seconds

    tx = contract.mintMembership(recipient, duration, {"from": deployer, "value": 10**16})
    tx.wait(1)

    print("✅ Membership minted.")
