#!/usr/bin/env python3

from bittensor.core.metagraph import Metagraph

def main():
    # Initialize metagraph for subnet 1
    print("Initializing metagraph for subnet 1...")
    metagraph = Metagraph(netuid=1, network="finney", sync=True)
    
    # Get performance metrics
    ranks = metagraph.R  # Performance ranks
    trust = metagraph.T  # Trust scores
    consensus = metagraph.C  # Consensus scores
    validator_trust = metagraph.Tv  # Validator trust
    uids = metagraph.uids

    # Find top performing neurons
    top_ranked_indices = ranks.argsort()[::-1][:10]
    print("\n=== Top 10 Ranked Neurons ===")
    for i, idx in enumerate(top_ranked_indices):
        uid = uids[idx].item()
        rank = ranks[idx].item()
        trust_score = trust[idx].item()
        consensus_score = consensus[idx].item()
        print(f"  {i+1}. UID {uid}: Rank={rank:.4f}, Trust={trust_score:.4f}, Consensus={consensus_score:.4f}")

    # Analyze trust distribution
    print(f"\n=== Trust Analysis ===")
    print(f"Average trust score: {trust.mean().item():.4f}")
    print(f"Trust score std dev: {trust.std().item():.4f}")
    print(f"Highest trust: {trust.max().item():.4f}")
    print(f"Lowest trust: {trust.min().item():.4f}")

    # Find most trusted validators
    validator_indices = metagraph.validator_permit.nonzero()[0]
    if len(validator_indices) > 0:
        validator_trust_scores = validator_trust[validator_indices]
        top_validators = validator_indices[validator_trust_scores.argsort()[::-1][:5]]
        print("\n=== Top 5 Trusted Validators ===")
        for i, idx in enumerate(top_validators):
            uid = uids[idx].item()
            vtrust = validator_trust[idx].item()
            print(f"  {i+1}. UID {uid}: Validator Trust={vtrust:.4f}")
    else:
        print("\nNo validators found in this subnet.")

if __name__ == "__main__":
    main() 