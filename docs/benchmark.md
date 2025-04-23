# Gas Usage Benchmark

This document records the actual gas usage measurements for the **NFT Membership** contract, deployed on the **Sepolia** test network. We measure these values to illustrate overhead from features like `AccessControl` and `Ownable`, and to facilitate a future comparison against existing subscription protocols (e.g., Unlock).

---

## 1. Deployment Data

**Tx Hash**: `0xb34d6eb35762db27bd6c668350217306b57b1eab3fd115d9ecc04beae070824a`  
**From (Deployer)**: `0x816ca99BE0ba877bD780332B446D5ABC30285a31`  
**Contract Address**: `0x5eD39cDD92134FC80a1DE928Aad55533BC8eA761`  
**Block**: `8174163`  
**Gas Used**: `1,963,468 / 2,178,239 (90.1%)`

- This contract includes `AccessControl` and `Ownable`, which add overhead for role-based permissions.
- The usage aligns with advanced membership features (RBAC), so a higher deployment cost is expected.

---

## 2. Mint & Renew Transactions

Below are the **mintMembership** and **renewMembership** calls from a single account (`myBrownieAccount`) holding test ETH on Sepolia.

### 2.1 Mint Membership

- **Tx Hash**: `0xd5e81747227fafdf22e9f60d0feda9afb1dd7f0fe27770df9c3b342596aa636a`  
- **Block**: `8175706`  
- **Gas Used**: `115,776 / 128,499 (90.1%)`  
- **Function**: `mintMembership(myacct.address, 3600, {"from": myacct, "value": 0.01 ether})`  
- **Token ID** minted: `1`  

**Notes**:  
- Minting sets the token’s `validUntil` to `block.timestamp + 3600` (1 hour).  
- The call requires 0.01 ETH, matching the contract’s `membershipPrice`.

### 2.2 Renew Membership

- **Tx Hash**: `0x240ef88c07f49a052d4fc0c00dfb8b701f8a17ae557684fe47e1d295a36e919b`  
- **Block**: `8175723`  
- **Gas Used**: `33,016 / 36,709 (89.9%)`  
- **Function**: `renewMembership(1, 3600, {"from": myacct, "value": 0.01 ether})`  
- **New Expiry**: `1745374500` (Unix timestamp)  
- **`isValid(1)`** returned `True`  

**Notes**:  
- Renewing extended the same token (ID = 1) by another hour.  
- The gas usage is lower than mint, likely because `_safeMint` logic is bypassed.

---

## 3. Summary Table

Below is a concise table comparing each action and its gas usage:

| **Action**        | **Tx Hash**                                                   | **Gas Used** | **Block**  | **Notes**                                                          |
|-------------------|---------------------------------------------------------------|-------------:|-----------:|--------------------------------------------------------------------|
| **Deployment**    | `0xb34d6eb3...`                                              | **1,963,468** | 8174163    | AccessControl, Ownable overhead                                    |
| **Mint**          | `0xd5e81747...`                                              | **115,776**  | 8175706    | `_safeMint`; tokenId=1; sets expiration by +3600s                  |
| **Renew**         | `0x240ef88c...`                                              | **33,016**   | 8175723    | Extends tokenId=1 by +3600s; no new NFT minted                     |

---

## 4. Observations & Future Work

1. **Deployment Overhead**  
   - Roughly 1.96 million gas, consistent with advanced contract logic (RBAC, role checks, etc.).

2. **Mint vs. Renew**  
   - Mint requires more gas due to `_safeMint` and event logs, while Renew is cheaper at ~33k gas.

3. **Comparative Analysis**  
   - These measurements will be compared against existing subscription platforms (e.g., Unlock Protocol).  
   - If Unlock’s “purchaseKey” and “extendKey” cost more, we might conclude our system is more efficient—or vice versa.

4. **Future**  
   - Explore meta-transactions for gasless renewals, possibly deploying to a Layer-2 (e.g., Polygon) to reduce cost further.  
   - Document user experience and usability in the final report.

---

## 5. References

- **Sepolia Etherscan**  
  [https://sepolia.etherscan.io/](https://sepolia.etherscan.io/)  
  (For verifying actual transaction data and logs.)

- **Unlock Protocol Docs**  
  [https://docs.unlock-protocol.com/](https://docs.unlock-protocol.com/)  
  (For eventual gas usage comparison.)

---

**Last Updated**: April 2025

