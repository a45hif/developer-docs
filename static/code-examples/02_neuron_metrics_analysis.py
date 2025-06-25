#!/usr/bin/env python3

from bittensor.core.metagraph import Metagraph

def main():
    # Initialize metagraph for subnet 1
    print("Initializing metagraph for subnet 1...")
    metagraph = Metagraph(netuid=1, network="finney", sync=True)
    
    # Get all neuron UIDs
    uids = metagraph.uids
    print(f"\nNeuron UIDs: {uids.tolist()}")

    # Analyze stake distribution
    stakes = metagraph.S  # Total stake
    alpha_stakes = metagraph.AS  # Alpha token stake
    tao_stakes = metagraph.TS  # TAO token stake

    print(f"\n=== Stake Analysis ===")
    print(f"Total stake across all neurons: {stakes.sum().item():.2f}")
    print(f"Average stake per neuron: {stakes.mean().item():.2f}")
    print(f"Highest stake: {stakes.max().item():.2f}")
    print(f"Lowest stake: {stakes.min().item():.2f}")

    # Find top staked neurons
    top_staked_indices = stakes.argsort()[::-1][:10]
    print("\nTop 10 staked neurons:")
    for i, idx in enumerate(top_staked_indices):
        uid = uids[idx].item()
        stake = stakes[idx].item()
        print(f"  {i+1}. UID {uid}: {stake:.2f} τ")

    # Analyze alpha vs tao stake distribution
    alpha_ratio = alpha_stakes / (alpha_stakes + tao_stakes)
    print(f"\nAverage alpha stake ratio: {alpha_ratio.mean().item():.2%}")

if __name__ == "__main__":
    main() 