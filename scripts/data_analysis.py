from brownie import network, NFTMembership
from datetime import datetime


def main():
    """
    Analyzes 'MembershipRenewed' events for a deployed NFTMembership contract.

    This script:
      - Connects to the active Brownie network (e.g., 'sepolia')
      - Reads logs from a deployed NFTMembership address
      - Scans for 'MembershipRenewed' events over the last N blocks
      - Prints token ID and new expiration in UTC

    Usage:
        brownie run scripts/data_analysis.py --network sepolia
    """

    # 1. Confirm active network
    active_net = network.show_active()
    print(f"\n🔗 Connected to network: {active_net}")

    # 2. Set your deployed NFTMembership contract address
    nft_membership_address = "0xAaf086EC89D311f3fcAB1B17A735d4c8D746DFcF"  # Replace with your deployed address

    try:
        nft = NFTMembership.at(nft_membership_address)
        print(f"📘 Loaded NFTMembership contract at: {nft.address}")
    except Exception as e:
        print(f"❌ Failed to load contract: {e}")
        return

    # 3. Define block range to scan
    web3 = network.web3
    latest_block = web3.eth.block_number
    lookback = 5000
    from_block = max(latest_block - lookback, 0)

    print(f"🔍 Searching for 'MembershipRenewed' events from block {from_block} to {latest_block}...")

    # 4. Fetch events using camelCase (Brownie v1.20.7)
    try:
        events = nft.events.MembershipRenewed.get_logs(fromBlock=from_block, toBlock=latest_block)
    except Exception as e:
        print(f"❌ Could not fetch events: {e}")
        return

    # 5. Print results
    if not events:
        print("⚠️ No 'MembershipRenewed' events found.")
        return

    print(f"\n✅ Found {len(events)} 'MembershipRenewed' event(s):\n")

    for evt in events:
        token_id = evt.args.tokenId
        new_expiry = evt.args.newExpiry
        readable_date = datetime.utcfromtimestamp(new_expiry).strftime("%Y-%m-%d %H:%M:%S UTC")
        print(f" • Token ID: {token_id} | New Expiry: {readable_date}")

    print("\n📊 Event analysis complete.\n")
