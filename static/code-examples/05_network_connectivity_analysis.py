#!/usr/bin/env python3

from bittensor.core.metagraph import Metagraph

def main():
    # Initialize metagraph for subnet 1
    print("Initializing metagraph for subnet 1...")
    metagraph = Metagraph(netuid=1, network="finney", sync=True)
    
    # Get network information
    axons = metagraph.axons
    uids = metagraph.uids

    # Analyze network addresses
    addresses = [axon.ip for axon in axons]
    unique_addresses = set(addresses)
    unique_hotkeys = set(metagraph.hotkeys)
    unique_coldkeys = set(metagraph.coldkeys)

    print(f"\n=== Network Address Analysis ===")
    print(f"Total unique addresses: {len(unique_addresses)}")
    print(f"Total unique hotkeys: {len(unique_hotkeys)}")
    print(f"Total unique coldkeys: {len(unique_coldkeys)}")

    # Find neurons sharing addresses
    address_to_uids = {}
    for i, address in enumerate(addresses):
        if address not in address_to_uids:
            address_to_uids[address] = []
        address_to_uids[address].append(uids[i].item())

    print(f"\n=== Neurons Sharing Addresses ===")
    for address, uids_list in address_to_uids.items():
        if len(uids_list) > 1:
            print(f"  Address {address}: UIDs {uids_list}")

    # Show axon details for first few neurons
    print(f"\n=== Axon Details (First 5 Neurons) ===")
    for i in range(min(5, len(axons))):
        axon = axons[i]
        uid = uids[i].item()
        hotkey = metagraph.hotkeys[i][:10] + "..."
        print(f"  UID {uid}: IP={axon.ip}, Port={axon.port}, Hotkey={hotkey}")

if __name__ == "__main__":
    main() 