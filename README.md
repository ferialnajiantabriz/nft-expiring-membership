
# 🧾 Decentralized NFT Membership Pass with Expiring Access (Gasless Renewal)

This project implements a decentralized NFT-based subscription system with **on-chain expiration**, **renewal**, and **gasless transactions** via EIP-712 meta-transactions. It is designed to be a simpler, more focused alternative to protocols like Unlock or Lit, making it ideal for DAOs, online study groups, or small Web3 communities.

> ✅ Deployed and verified on Sepolia Testnet  
> ✅ Integrated with EIP-2771 MinimalForwarder  
> ✅ Event logs, gas benchmarks, and full relayer flow tested  
> ✅ Developed with Brownie and Web3.py (Python)

---

## 📦 Features

- **ERC-721 NFT** with expiration time
- **On-chain membership renewal**  
- Emits `MembershipRenewed` event  
- **Meta-transaction support** using EIP-712  
- Forwarder and user roles separated (relayer-based model)  
- Brownie-based Python deployment & testing  

---

## 🧠 Motivation

Subscription-based Web3 access is often handled by heavy platforms like Unlock or Lit Protocol.  
This project offers a **lightweight, forkable, and gas-efficient** alternative that supports:

- NFT-based access
- Automatic expiration
- User-triggered renewal (including gasless)
- Self-hosted and transparent logic

---

## ⚙️ Technologies Used

- **Solidity**: Smart contract development  
- **Brownie**: Python-based Ethereum framework  
- **Web3.py**: Interact with Ethereum in Python  
- **Infura**: RPC provider (Sepolia)  
- **Etherscan**: Transaction explorer  

---

## 🔗 Deployment Summary

| Contract         | Address                                             |
|------------------|-----------------------------------------------------|
| **NFTMembership**    | `0x4b4b4e1F3787a2A3C907BF7d751008f0e9b25971`       |
| **MinimalForwarder** | `0x523A5FaF22E7696a53C7C1c1412770E859A685E6`       |

---

## 🔍 Workflow Summary

1. **Minting**  
   - `mint_membership.py` mints an ERC-721 NFT with a built-in expiration time.

2. **Standard Renewal**  
   - `test_renew.py` renews an NFT's expiration by sending a normal transaction.

3. **Gasless Renewal**  
   1. **User signs** a meta-transaction using `gasless_renew.py`.  
   2. The signed request is saved as `signed_request.json`.  
   3. A **relayer** runs `relayer_execute.py` to forward the request on-chain.  
   4. The contract verifies the signature and extends the membership without the user paying gas.

---

## 🧪 Event Verification

Each successful call to `renewMembership()` or `metaRenewMembership()` emits:

```solidity
event MembershipRenewed(uint256 tokenId, uint256 newExpiry);
```

**How to confirm**:
- **Brownie console**: Inspect `tx.events`
- **Etherscan logs**:  
  [MembershipRenewed – Sepolia](https://sepolia.etherscan.io/tx/0x93404c7bf8429e12d4c3245435c75c58058781d26c252c8e946c8bcc1e335e3b)

---

## 📊 Gas Benchmarking (Sepolia)

| Action            | Gas Used | Block    | Notes                                 |
|-------------------|---------:|---------:|---------------------------------------|
| Mint Membership   |   81,576 | 8235918  | Low-cost ERC-721 mint                 |
| Renew Membership  |   32,790 | 8235933  | Simple expiry-timestamp update        |
| Relayed Meta-Tx   |   64,395 | 8236390  | EIP-712 signature + verification cost |

🔗 **View Relayed Tx** on Etherscan:  
[https://sepolia.etherscan.io/tx/0x2b759e67a13566fe4dccee3a7ce646b8004dccaa81e2abf8c6c046979b9654a0](https://sepolia.etherscan.io/tx/0x2b759e67a13566fe4dccee3a7ce646b8004dccaa81e2abf8c6c046979b9654a0)

---

## 🔍 Comparative Analysis

| Feature                  | **This Project**                 | **Unlock Protocol**           | **Lit Protocol**                     |
|--------------------------|----------------------------------|-------------------------------|---------------------------------------|
| Expiring NFT             | ✅ Yes                            | ✅ Yes                         | ❌ No (focus on gating)              |
| Meta-transaction support | ✅ EIP-712 + MinimalForwarder     | ✅ Built-in relayer            | ⚠️ Custom integration                |
| Customization            | ✅ Full Solidity control          | ❌ Complex proxy architecture  | ⚠️ JavaScript-based gating           |
| Gas cost                 | ✅ Low (single contract, ~100k)   | ❌ Higher (multi-contract)     | ⚠️ Varies                             |
| Best For                 | DAOs, small groups, self-hosters  | Larger creators/marketplaces  | Content encryption gating            |

---

## 🚀 Run Locally

```bash
# Step 1: Install dependencies
pip install -r requirements.txt

# Step 2: Set up .env (not committed)
cp .env.example .env
# Fill in: INFURA_ID, PRIVATE_KEYs, FORWARDER_ADDRESS, MEMBERSHIP_ADDRESS

# Step 3: Compile contracts
brownie compile

# Step 4: Deploy contracts
brownie run scripts/deploy_forwarder.py --network sepolia
brownie run scripts/deploy.py --network sepolia

# Step 5: Mint NFT
brownie run scripts/mint_membership.py --network sepolia

# Step 6: Renew (normal tx)
brownie run scripts/test_renew.py --network sepolia

# Step 7: Gasless - User signs
brownie run scripts/gasless_renew.py --network sepolia

# Step 8: Gasless - Relayer sends
brownie run scripts/relayer_execute.py --network sepolia

