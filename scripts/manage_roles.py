from brownie import accounts, NFTMembership
import os

def main():
    # Load admin account (deployer)
    admin = accounts.load("myDeployerAccount")  # You will enter your password here

    # Load deployed contract
    contract_address = os.getenv("MEMBERSHIP_ADDRESS")
    contract = NFTMembership.at(contract_address)

    # Define target address (new admin to grant role to)
    new_admin = "0xD56521A2bc066ACFAf2cB398D38Be0C560b6abfD"  # Replace with address to grant ADMIN_ROLE

    # Get the ADMIN_ROLE identifier
    admin_role = contract.ADMIN_ROLE()

    # ✅ Grant ADMIN_ROLE
    print(f"Granting ADMIN_ROLE to: {new_admin}")
    tx = contract.grantRole(admin_role, new_admin, {"from": admin})
    tx.wait(1)
    print("Transaction successful:", tx.txid)

    # ✅ Check if role was granted
    has_role = contract.hasRole(admin_role, new_admin)
    print(f"Does {new_admin} have ADMIN_ROLE? {has_role}")

    # Optional: Revoke role and check
    revoke = input("Do you want to revoke this role? (y/n): ").strip().lower()
    if revoke == 'y':
        revoke_tx = contract.revokeRole(admin_role, new_admin, {"from": admin})
        revoke_tx.wait(1)
        print("Role revoked.")
        print(f"Does {new_admin} still have ADMIN_ROLE? {contract.hasRole(admin_role, new_admin)}")
    else:
        print("Skipping revoke.")

