# NFT Expiring Membership

A decentralized membership pass on Ethereum that uses Non-Fungible Tokens (NFTs) with an expiration date. This allows you to issue time-limited memberships, enforce renewals, and track all activity on-chain without relying on a centralized subscription platform.

## Table of Contents
1. Project Overview
2. Features
3. Tech Stack
4. Setup & Installation
   - Prerequisites
   - Cloning the Repository
   - Python Virtual Environment (Optional)
   - Installing Dependencies
   - Brownie Initialization
   - Configuration Files
5. Folder Structure
6. Compiling Contracts
7. Running Tests
8. Deployment
9. Usage
   - Mint a Membership
   - Check Validity
   - Renew a Membership
10. Additional Features (Optional)
11. Comparative Analysis & On-Chain Data
12. Security & Audits
13. License
14. Contact

-------------------------------------------------------------------------------

## 1. Project Overview

NFT Expiring Membership provides a time-based NFT token—once minted, the NFT is valid until a certain timestamp. After that date passes, membership privileges are invalid unless the owner renews by paying the renewal fee.

It addresses the need for recurring, trust-minimized subscriptions without relying on centralized services (Patreon, OnlyFans, etc.). All membership logic is enforced by a smart contract on the Ethereum blockchain.

-------------------------------------------------------------------------------

## 2. Features

- Time-Limited Ownership: Every membership NFT has an expiration date (validUntil).
- Renewal Mechanics: Users can call renewMembership to extend their membership.
- Payment Enforced: A membershipPrice ensures that minting/renewing requires payment (in ETH).
- Easy Integration: Extendable for role-based access control, meta-transactions (gasless renewals), or custom logic.
- Transparent: All on-chain actions are publicly verifiable.

-------------------------------------------------------------------------------

## 3. Tech Stack

- Solidity (Smart Contracts)
- Brownie (Development & Testing Framework for Ethereum)
- Web3.py (Blockchain interaction in Python)
- Pytest (Testing in Python)
- OpenZeppelin (Secure smart contract libraries)

Optional:
- Meta-Transactions (gasless user experience, e.g., via GSN or Biconomy)
- Flask/React for a user-facing DApp interface.

-------------------------------------------------------------------------------

## 4. Setup & Installation

### Prerequisites
- Python 3.7+
- Git
- (Optional) Node.js if building a front-end with JavaScript
- An Ethereum environment (e.g., Ganache or Brownie’s local test network)

### Cloning the Repository
git clone https://github.com/<YourUsername>/nft-expiring-membership.git
cd nft-expiring-membership

### Python Virtual Environment (Optional)
python -m venv venv
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

### Installing Dependencies
pip install -r requirements.txt

(The requirements file should list eth-brownie, web3, pytest, etc.)

### Brownie Initialization
brownie init
(This sets up a default Brownie project structure if needed.)

### Configuration Files
- brownie-config.yaml: Compiler settings, network configs, etc.
- .env: Private environment variables like keys (DO NOT COMMIT this file).

-------------------------------------------------------------------------------

## 5. Folder Structure

nft-expiring-membership/
├── contracts/
│   └── NFTMembership.sol
├── scripts/
│   └── deploy.py
├── tests/
│   └── test_membership.py
├── .env
├── .gitignore
├── brownie-config.yaml
├── requirements.txt
└── README.md

Explanation:
- contracts/: Solidity files
- scripts/: Python deployment scripts
- tests/: Pytest/Brownie test scripts
- brownie-config.yaml: Project settings and compiler info

-------------------------------------------------------------------------------

## 6. Compiling Contracts

Once your .sol files are ready, run:
brownie compile

Brownie uses the Solidity version specified in brownie-config.yaml. Build artifacts appear under build/.

-------------------------------------------------------------------------------

## 7. Running Tests

brownie test

This command:
- Launches a local test chain
- Deploys contracts
- Executes all test scripts found in tests/
- Prints pass/fail results

For verbose output:
brownie test -s

-------------------------------------------------------------------------------

## 8. Deployment

Use Brownie to deploy to a local, testnet, or mainnet network.

Example script (scripts/deploy.py):

from brownie import NFTMembership, accounts

def main():
    account = accounts.load("myBrownieAccount")
    contract = NFTMembership.deploy(
        "MembershipPass",
        "MBR",
        10**16,
        {"from": account}
    )
    print(f"Deployed at {contract.address}")

Then run:
brownie run scripts/deploy.py --network sepolia

-------------------------------------------------------------------------------

## 9. Usage

### Mint a Membership
mintMembership(address recipient, uint256 duration) external payable

- Requires at least membershipPrice in msg.value
- Sets validUntil[tokenId] = currentTime + duration

Example in Brownie console:
>>> membership.mintMembership(accounts[1], 3600, {"from": accounts[1], "value": "0.01 ether"})

### Check Validity
isValid(uint256 tokenId) public view returns (bool)

Returns true if current block time <= validUntil[tokenId].

### Renew a Membership
renewMembership(uint256 tokenId, uint256 additionalTime) external payable

- Must be called by the token’s owner
- Requires membershipPrice in msg.value
- Extends validUntil[tokenId] by additionalTime

-------------------------------------------------------------------------------

## 10. Additional Features (Optional)

- Role-Based Access Control: Use OpenZeppelin’s AccessControl to manage admin or privileged roles.
- Meta-Transactions: Let a relayer pay gas on behalf of users.
- Tiered Pricing: Different membership levels with varying durations or prices.
- UI/DApp: A front-end (Flask or React) to simplify user interaction.

-------------------------------------------------------------------------------

## 11. Comparative Analysis & On-Chain Data

To differentiate from existing solutions (e.g., Unlock Protocol), we plan to:
- Compare gas usage for minting/renewing
- Analyze real on-chain NFT subscription usage (frequency of renewals, transfers)
- Document these findings in a separate docs folder or final report

-------------------------------------------------------------------------------

## 12. Security & Audits

- Local Testing with Pytest
- Static Analysis (Slither, MythX)
- Use audited libraries (OpenZeppelin) to reduce risk
- Security best practices: withdraw patterns, reentrancy guards if needed

-------------------------------------------------------------------------------

## 13. License

MIT License (or your chosen license)

-------------------------------------------------------------------------------

## 14. Contact

- Maintainer: Your Name
- Email: your.email@example.com
- GitHub: https://github.com/<YourUsername>

