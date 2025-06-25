#!/usr/bin/env python3

import bittensor as bt

def analyze_subnet(netuid):
    """Analyze subnet health"""
    print(f"Analyzing subnet {netuid}...")
    metagraph = bt.metagraph(netuid=netuid)
    metagraph.sync()
    
    total_neurons = metagraph.n.item()
    active_neurons = metagraph.active.sum().item()
    total_stake = metagraph.S.sum().item()
    
    print(f"Subnet {netuid} Analysis:")
    print(f"  Total neurons: {total_neurons}")
    print(f"  Active neurons: {active_neurons}")
    print(f"  Total stake: {total_stake}")
    print(f"  Activity rate: {active_neurons/total_neurons:.2%}")

def get_top_validators(netuid, top_k=10):
    """Find top validators"""
    print(f"Finding top {top_k} validators for subnet {netuid}...")
    metagraph = bt.metagraph(netuid=netuid)
    metagraph.sync()
    
    # Get validator permits
    validator_mask = metagraph.validator_permit
    
    # Get ranks for validators only
    validator_ranks = metagraph.R[validator_mask]
    validator_uids = metagraph.uids[validator_mask]
    
    # Sort by rank
    sorted_indices = validator_ranks.argsort()[::-1]
    top_validators = validator_uids[sorted_indices][:top_k]
    
    print(f"Top {top_k} validators:")
    for i, uid in enumerate(top_validators):
        print(f"  {i+1}. UID {uid.item()}")
    
    return top_validators.tolist()

def analyze_weights(netuid):
    """Analyze weight distribution"""
    print(f"Analyzing weights for subnet {netuid}...")
    metagraph = bt.metagraph(netuid=netuid, lite=False)
    metagraph.sync()
    
    weights = metagraph.W
    print(f"Weight matrix shape: {weights.shape}")
    
    # Find neurons with most incoming weights
    incoming_weights = weights.sum(axis=0)
    top_receivers = incoming_weights.argsort()[::-1][:10]
    print(f"Top 10 weight receivers: {top_receivers.tolist()}")
    
    # Find neurons with most outgoing weights
    outgoing_weights = weights.sum(axis=1)
    top_senders = outgoing_weights.argsort()[::-1][:10]
    print(f"Top 10 weight senders: {top_senders.tolist()}")

def main():
    print("=== Common Use Cases Examples ===")
    
    # Example 1: Subnet Analysis
    print("\n1. Subnet Analysis")
    analyze_subnet(1)
    
    # Example 2: Validator Selection
    print("\n2. Validator Selection")
    get_top_validators(1, top_k=5)
    
    # Example 3: Weight Analysis
    print("\n3. Weight Analysis")
    try:
        analyze_weights(1)
    except Exception as e:
        print(f"Weight analysis failed: {e}")

if __name__ == "__main__":
    main() 