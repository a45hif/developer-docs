#!/usr/bin/env python3
"""
Network Connectivity Analysis Example

This example demonstrates how to analyze network addresses and axon information.
"""

from bittensor.core.metagraph import Metagraph

def main():
    # Initialize metagraph for subnet 1
    print("Initializing metagraph for subnet 1...")
    metagraph = Metagraph(netuid=1, network="finney", sync=True)
    
    # Get network connection information
    hotkeys = metagraph.hotkeys
    coldkeys = metagraph.coldkeys
    addresses = metagraph.addresses
    axons = metagraph.axons
    uids = metagraph.uids

    # Analyze network addresses
    print(f"\n=== Network Address Analysis ===")
    print(f"Total unique addresses: {len(set(addresses))}")
    print(f"Total unique hotkeys: {len(set(hotkeys))}")
    print(f"Total unique coldkeys: {len(set(coldkeys))}")

    # Find neurons by address
    address_to_uids = {}
    for i, addr in enumerate(addresses):
        if addr not in address_to_uids:
            address_to_uids[addr] = []
        address_to_uids[addr].append(uids[i].item())

    print("\n=== Neurons Sharing Addresses ===")
    shared_addresses = False
    for addr, uid_list in address_to_uids.items():
        if len(uid_list) > 1:
            shared_addresses = True
            print(f"  Address {addr}: UIDs {uid_list}")
    
    if not shared_addresses:
        print("  No neurons sharing addresses found.")

    # Analyze axon information
    print(f"\n=== Axon Details (First 5 Neurons) ===")
    for i in range(min(5, len(axons))):
        axon = axons[i]
        print(f"  UID {uids[i].item()}: IP={axon.ip_str()}, Port={axon.port}, Hotkey={axon.hotkey[:8]}...")

if __name__ == "__main__":
    main() 