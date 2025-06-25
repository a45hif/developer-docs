#!/usr/bin/env python3

from bittensor.core.metagraph import Metagraph

def main():
    # Initialize metagraph for subnet 1
    print("Initializing metagraph for subnet 1...")
    metagraph = Metagraph(netuid=1, network="finney", sync=True)
    
    # Get economic metrics
    incentives = metagraph.I  # Incentive scores
    emissions = metagraph.E  # Emission rates
    dividends = metagraph.D  # Dividend distributions
    uids = metagraph.uids

    # Analyze incentive distribution
    print(f"\n=== Incentive Analysis ===")
    print(f"Total incentives: {incentives.sum().item():.4f}")
    print(f"Average incentive: {incentives.mean().item():.4f}")
    print(f"Highest incentive: {incentives.max().item():.4f}")

    # Find highest incentivized neurons
    top_incentive_indices = incentives.argsort()[::-1][:10]
    print("\n=== Top 10 Incentivized Neurons ===")
    for i, idx in enumerate(top_incentive_indices):
        uid = uids[idx].item()
        incentive = incentives[idx].item()
        emission = emissions[idx].item()
        dividend = dividends[idx].item()
        print(f"  {i+1}. UID {uid}: Incentive={incentive:.4f}, Emission={emission:.4f}, Dividend={dividend:.4f}")

    # Analyze dividend distribution
    print(f"\n=== Dividend Analysis ===")
    print(f"Total dividends: {dividends.sum().item():.4f}")
    print(f"Average dividend: {dividends.mean().item():.4f}")
    print(f"Dividend std dev: {dividends.std().item():.4f}")

if __name__ == "__main__":
    main() 