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
