#!/usr/bin/env python3
"""
Bond Analysis Example

This example demonstrates how to analyze the bond matrix between neurons.
Note: This requires lite=False to access bonds.
"""

from bittensor.core.metagraph import Metagraph

def main():
    # Initialize metagraph for subnet 1 with full sync (not lite)
    print("Initializing metagraph for subnet 1 (full sync)...")
    metagraph = Metagraph(netuid=1, network="finney", lite=False, sync=True)
    
    uids = metagraph.uids
    
    # Get bond matrix (requires lite=False)
    if not metagraph.lite and hasattr(metagraph, 'bonds') and metagraph.bonds.size > 0:
        bonds = metagraph.B  # Bond matrix
        
        print(f"\n=== Bond Matrix Analysis ===")
        print(f"Bond matrix shape: {bonds.shape}")
        print(f"Total bonds: {bonds.sum().item():.4f}")
        print(f"Average bond: {bonds.mean().item():.4f}")
        
        # Find neurons with most bonds
        bonds_received = bonds.sum(axis=0)  # Sum of incoming bonds
        top_bonded = bonds_received.argsort()[::-1][:10]
        print("\n=== Top 10 Bonded Neurons ===")
        for i, idx in enumerate(top_bonded):
            uid = uids[idx].item()
            total_bonds = bonds_received[idx].item()
            print(f"  {i+1}. UID {uid}: {total_bonds:.4f}")
    else:
        print("Bonds not available. Make sure to use lite=False when initializing the metagraph.")

if __name__ == "__main__":
    main() 