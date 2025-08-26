
#  Decentralized NFT Membership Pass with Expiring Access (Gasless Renewal)

##  Project Demo Video

Watch the 17-minute demo explaining the project goals, approach, and key features:

▶ [Watch on YouTube](https://youtu.be/Bupw9KAw7IM)

*Note: This video demonstrates the prototype and key outcomes of the project.*

---

This project implements a decentralized NFT-based subscription system with:

- On-chain expiration
-  On-chain and gasless renewals via EIP-712 meta-transactions
- Role-Based Access Control (RBAC) for secure admin-only logic

It is a **lightweight alternative** to complex protocols like Unlock or Lit Protocol and is ideal for small DAOs, student organizations, gated communities, or Web3-based learning platforms.

---

##  Features

-  ERC-721 NFT with expiration timestamp (`validUntil`)
-  On-chain membership renewal via `renewMembership`
-  Gasless renewal using EIP-712 + MinimalForwarder (EIP-2771)
-  Signature verification and relayer flow
-  Emits `MembershipRenewed` event with updated expiry
-  **RBAC**: Only admins can change price; roles managed with `AccessControl`
-  Tested with Brownie and Web3.py, deployed on Sepolia

---

##  Motivation

This system solves a common problem for smaller communities who want:

- Expiring access control (NFT as a time-based pass)
- A system that works without every user having ETH
- Something **easy to audit, fork, and deploy**, without SDKs or proxy factories

Unlock and Lit Protocol are powerful, but often **too complex** or overbuilt for small teams or educational environments. This project aims to balance **simplicity, security, and usability**.

---

##  Technologies Used

- **Solidity** – smart contracts
- **Brownie** – Python smart contract development framework
- **Web3.py** – EIP-712 signature generation and relayer execution
- **Infura** – Sepolia RPC provider
- **Etherscan** – for transaction/event verification

---

##  Deployment Summary

| Contract              | Address                                                   |
|-----------------------|-----------------------------------------------------------|
| `NFTMembership`       | `0x4b4b4e1F3787a2A3C907BF7d751008f0e9b25971`              |
| `MinimalForwarder`    | `0x523A5FaF22E7696a53C7C1c1412770E859A685E6`              |

---

##  Workflow Summary

###  Minting
```bash
brownie run scripts/mint_membership.py --network sepolia
````

Mints a new NFT to a user, setting an expiration using `validUntil`.

###  Standard Renewal

```bash
brownie run scripts/test_renew.py --network sepolia
```

Directly calls `renewMembership()` to extend the token’s expiration.

###  Gasless Renewal (EIP-712 + EIP-2771)

1. User signs a meta-tx off-chain using `gasless_renew.py`
2. Relayer submits it using `relayer_execute.py`
3. `MinimalForwarder` verifies and forwards the call to `metaRenewMembership()`

---

##  Role-Based Access Control (RBAC)

RBAC is implemented using OpenZeppelin’s `AccessControl`.

| Role                 | Purpose                             |
| -------------------- | ----------------------------------- |
| `DEFAULT_ADMIN_ROLE` | Full control (grants/revokes roles) |
| `ADMIN_ROLE`         | Can update membership price         |

Role management is handled through:

```bash
brownie run scripts/manage_roles.py --network sepolia
```

Functions like `setMembershipPrice()` are protected by:

```solidity
onlyRole(ADMIN_ROLE)
```

---

##  Event Verification

Every renewal emits:

```solidity
event MembershipRenewed(uint256 tokenId, uint256 newExpiry);
```

 View on-chain event:

* Brownie logs: `tx.events`
* Etherscan: [MembershipRenewed (Sepolia)](https://sepolia.etherscan.io/tx/0x93404c7bf8429e12d4c3245435c75c58058781d26c252c8e946c8bcc1e335e3b)

---

## 📊 Gas Benchmarking (Sepolia)

| Action           | Gas Used |   Block | Notes                              |
| ---------------- | -------: | ------: | ---------------------------------- |
| Mint Membership  |   81,576 | 8235918 | ERC-721 mint with expiration logic |
| Renew Membership |   32,790 | 8235933 | Direct call                        |
| Gasless Renewal  |   64,395 | 8236390 | Signature + forwarder call         |

🔗 View Meta-Tx:
[Relayed Transaction on Sepolia](https://sepolia.etherscan.io/tx/0x2b759e67a13566fe4dccee3a7ce646b8004dccaa81e2abf8c6c046979b9654a0)

---

##  Comparative Analysis

| Feature               | **This Project**        | **Unlock Protocol**       | **Lit Protocol**             |
| --------------------- | ----------------------- | ------------------------- | ---------------------------- |
| Expiring NFT          |  Yes                   |  Yes                       | No (gating only)             |
| Meta-Tx support       |  EIP-712 + EIP-2771    |  With relayer              |  SDK-based only              |
| Upgradeable Contracts |  No                    |  Yes (Proxy)               |  No                          |
| Factory Complexity    |  None                  |  Required                  |  Not applicable              |
| Custom Admin Roles    |  Yes (RBAC)            |  Advanced use only         |  No roles                    |
| Gas Cost              |  Low (\~80k–100k)      |  Higher                    |  Varies                      |
| Best Use Case         | DAOs, clubs, classrooms| Marketplaces, paid access  | Token-gated document sharing |

---

##  Run the Project Locally

```bash
# 1. Install Python dependencies
pip install -r requirements.txt

# 2. Create and fill .env file
cp .env.example .env
# Add: INFURA_ID, PRIVATE_KEYs, FORWARDER_ADDRESS, MEMBERSHIP_ADDRESS

# 3. Compile contracts
brownie compile

# 4. Deploy contracts
brownie run scripts/deploy_forwarder.py --network sepolia
brownie run scripts/deploy.py --network sepolia

# 5. Mint a Membership
brownie run scripts/mint_membership.py --network sepolia

# 6. Standard Renewal
brownie run scripts/test_renew.py --network sepolia

# 7. Gasless Flow
brownie run scripts/gasless_renew.py --network sepolia
brownie run scripts/relayer_execute.py --network sepolia

# 8. Role Management
brownie run scripts/manage_roles.py --network sepolia


---

##  License

MIT License © 2025
Author: Ferial Najiantabriz
University of Oklahoma
Professor: Dr.Anindya Maiti

