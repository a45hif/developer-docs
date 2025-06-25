#!/usr/bin/env python3

from bittensor.core.metagraph import Metagraph
from bittensor.core.subtensor import Subtensor

def main():
    # Initialize metagraph for subnet 1
    print("Initializing metagraph for subnet 1...")
    metagraph = Metagraph(netuid=1, network="finney", sync=True)
    
    # Get basic metagraph metadata
    print("\n=== Basic Metagraph Metadata ===")
    print(f"Network: {metagraph.network}")
    print(f"Subnet UID: {metagraph.netuid}")
    print(f"Total neurons: {metagraph.n.item()}")
    print(f"Current block: {metagraph.block.item()}")
    print(f"Version: {metagraph.version.item()}")

    # Get subnet information
    print("\n=== Subnet Information ===")
    print(f"Subnet name: {metagraph.name}")
    print(f"Subnet symbol: {metagraph.symbol}")
    print(f"Registered at block: {metagraph.network_registered_at}")
    print(f"Max UIDs: {metagraph.max_uids}")
    print(f"Owner: {metagraph.owner_coldkey}")

if __name__ == "__main__":
    main() 