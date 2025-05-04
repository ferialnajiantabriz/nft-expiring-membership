
# 🧾 Decentralized NFT Membership Pass with Expiring Access (Gasless Renewal)

## 📽️ Project Demo Video

Watch the 17-minute demo explaining the project goals, approach, and key features:

▶️ [Watch on YouTube](https://youtu.be/Bupw9KAw7IM)

*Note: This video demonstrates the prototype, architecture, meta-transactions, relayer flow, and RBAC implementation.*

---

This project implements a decentralized NFT-based subscription system with **on-chain expiration**, **renewal**, and **gasless transactions** using EIP-712 meta-transactions. It is designed to be a lightweight, forkable alternative to platforms like Unlock or Lit Protocol — ideal for DAOs, online communities, or Web3-based memberships.

> ✅ Deployed and verified on Sepolia Testnet  
> ✅ Integrated with EIP-2771 MinimalForwarder  
> ✅ Event logs, gas benchmarks, and full relayer flow tested  
> ✅ Developed using Brownie and Web3.py (Python)

---

## 📦 Features

- 🪪 **ERC-721 NFT** with expiration logic
- 🔁 **On-chain renewal** via normal or meta-transactions  
- 📤 **Meta-transaction support** via EIP-712 (gasless for user)  
- 🧾 Emits `MembershipRenewed` event  
- 🔐 **Role-Based Access Control (RBAC)** for secure, permissioned administration  
- 🧪 Full Brownie-based deployment, testing, and benchmarking  
- 📂 Modular, readable Python scripts for minting, renewal, and relaying  

---

## 🔐 Role-Based Access Control (RBAC)

This project implements robust role-based permissions using OpenZeppelin’s `AccessControl`:

- 👤 **Default Admin Role** — Full privileges, initially granted to the deployer.
- 💵 **PRICE_MANAGER Role** — Only addresses with this role can update the renewal price.
- 🔒 Roles can only be granted/revoked by Admins using `grantRole()` and `revokeRole()` functions.
- 🧠 **Least privilege principle** enforced — limits who can mutate contract state.

**Smart Contract Snippet:**
```solidity
function setPrice(uint256 _newPrice) external onlyRole(PRICE_MANAGER) {
    ...
}
````

✅ This protects against unauthorized economic changes, supports DAO-safe governance, and improves transparency in shared deployments.

---

## 🧠 Motivation

Platforms like Unlock and Lit Protocol offer powerful subscription models but can be **overly complex** or **heavyweight** for small groups or individual developers.

This project offers a **minimal and gas-efficient** alternative that supports:

* NFT-based gated access
* Automatic expiration logic
* Optional gasless renewals
* Full control via local deployment
* Transparent, auditable architecture

---

## ⚙️ Technologies Used

* **Solidity** – Smart contract logic
* **Brownie** – Python-based Ethereum development framework
* **Web3.py** – Blockchain interaction via Python
* **Infura** – Ethereum RPC access for Sepolia
* **Etherscan** – Contract verification and log inspection
* **OpenZeppelin** – Security-vetted contract libraries (ERC-721, AccessControl)

---

## 🔗 Deployment Summary

| Contract             | Address                                      |
| -------------------- | -------------------------------------------- |
| **NFTMembership**    | `0x4b4b4e1F3787a2A3C907BF7d751008f0e9b25971` |
| **MinimalForwarder** | `0x523A5FaF22E7696a53C7C1c1412770E859A685E6` |

---

## 🔍 Workflow Summary

### 🪪 Minting

* `mint_membership.py`: Mints an ERC-721 NFT with an embedded expiration timestamp.

### 🔁 Standard Renewal

* `test_renew.py`: Renews membership via a direct Ethereum transaction.

### ⛽ Gasless Renewal (Meta-Transaction)

1. User signs a `metaRenewMembership()` request via `gasless_renew.py`.
2. Signature saved to `signed_request.json`.
3. A trusted **relayer** calls `relayer_execute.py` to forward it on-chain.
4. The contract verifies the signature, and renews the NFT **without user paying gas**.

---

## 🧪 Event Verification

Every successful renewal (standard or gasless) emits the following event:

```solidity
event MembershipRenewed(uint256 tokenId, uint256 newExpiry);
```

### 🔍 How to verify:

* In **Brownie**, use `tx.events`
* On **Etherscan**, review logs:
  ▶️ [MembershipRenewed – Sepolia](https://sepolia.etherscan.io/tx/0x93404c7bf8429e12d4c3245435c75c58058781d26c252c8e946c8bcc1e335e3b)

---

## 📊 Gas Benchmarking (Sepolia)

| Action           | Gas Used | Block   | Description                        |
| ---------------- | -------- | ------- | ---------------------------------- |
| Mint Membership  | 81,576   | 8235918 | Basic ERC-721 mint                 |
| Renew Membership | 32,790   | 8235933 | Simple expiry update               |
| Relayed Meta-Tx  | 64,395   | 8236390 | Signature verification via EIP-712 |

🔗 [View Meta-Tx on Etherscan](https://sepolia.etherscan.io/tx/0x2b759e67a13566fe4dccee3a7ce646b8004dccaa81e2abf8c6c046979b9654a0)

---

## 🔍 Comparative Analysis

| Feature                  | **This Project**                 | **Unlock Protocol**           | **Lit Protocol**            |
| ------------------------ | -------------------------------- | ----------------------------- | --------------------------- |
| Expiring NFT             | ✅ Yes                            | ✅ Yes                         | ❌ No (focus on gating)      |
| Meta-transaction support | ✅ EIP-712 + MinimalForwarder     | ✅ Built-in relayer            | ⚠️ Custom integration       |
| Customization            | ✅ Full Solidity control          | ❌ Complex proxy architecture  | ⚠️ JavaScript-based gating  |
| Gas cost                 | ✅ Low (single contract, \~100k)  | ❌ Higher (multi-contract)     | ⚠️ Varies                   |
| Best For                 | DAOs, study groups, self-hosters | Larger platforms/marketplaces | Content access & encryption |

---

## 🚀 Run Locally

```bash
# Step 1: Install Python dependencies
pip install -r requirements.txt

# Step 2: Create .env file
cp .env.example .env
# Fill in INFURA_ID, PRIVATE_KEY, FORWARDER_ADDRESS, MEMBERSHIP_ADDRESS

# Step 3: Compile contracts
brownie compile

# Step 4: Deploy contracts
brownie run scripts/deploy_forwarder.py --network sepolia
brownie run scripts/deploy.py --network sepolia

# Step 5: Mint NFT
brownie run scripts/mint_membership.py --network sepolia

# Step 6: Standard Renewal
brownie run scripts/test_renew.py --network sepolia

# Step 7: Gasless - User signs meta-tx
brownie run scripts/gasless_renew.py --network sepolia

# Step 8: Gasless - Relayer sends signed tx
brownie run scripts/relayer_execute.py --network sepolia
```

---

## 📫 Contact

For questions or contributions, feel free to open an issue or contact me directly.

---

```

Let me know if you'd like me to generate a corresponding Overleaf LaTeX section for the RBAC part or a PDF export of this `README.md`.
```
