#!/usr/bin/env python3
"""
Weight Matrix Analysis Example

This example demonstrates how to analyze the weight matrix between neurons.
Note: This requires lite=False to access weights.
"""

from bittensor.core.metagraph import Metagraph

def main():
    # Initialize metagraph for subnet 1 with full sync (not lite)
    print("Initializing metagraph for subnet 1 (full sync)...")
    metagraph = Metagraph(netuid=1, network="finney", lite=False, sync=True)
    
    uids = metagraph.uids
    
    # Get weight matrix (requires lite=False)
    if not metagraph.lite and hasattr(metagraph, 'weights') and metagraph.weights.size > 0:
        weights = metagraph.W  # Weight matrix
        
        print(f"\n=== Weight Matrix Analysis ===")
        print(f"Weight matrix shape: {weights.shape}")
        print(f"Total weights: {weights.sum().item():.4f}")
        print(f"Average weight: {weights.mean().item():.4f}")
        print(f"Max weight: {weights.max().item():.4f}")
        
        # Find neurons receiving most weights
        weight_received = weights.sum(axis=0)  # Sum of incoming weights
        top_receivers = weight_received.argsort()[::-1][:10]
        print("\n=== Top 10 Weight Receivers ===")
        for i, idx in enumerate(top_receivers):
            uid = uids[idx].item()
            total_weight = weight_received[idx].item()
            print(f"  {i+1}. UID {uid}: {total_weight:.4f}")
        
        # Find neurons sending most weights
        weight_sent = weights.sum(axis=1)  # Sum of outgoing weights
        top_senders = weight_sent.argsort()[::-1][:10]
        print("\n=== Top 10 Weight Senders ===")
        for i, idx in enumerate(top_senders):
            uid = uids[idx].item()
            total_weight = weight_sent[idx].item()
            print(f"  {i+1}. UID {uid}: {total_weight:.4f}")
        
        # Find strongest connections
        max_weight_idx = weights.argmax()
        sender_idx = max_weight_idx // weights.shape[1]
        receiver_idx = max_weight_idx % weights.shape[1]
        max_weight = weights.max().item()
        print(f"\n=== Strongest Connection ===")
        print(f"UID {uids[sender_idx].item()} -> UID {uids[receiver_idx].item()}: {max_weight:.4f}")
    else:
        print("Weights not available. Make sure to use lite=False when initializing the metagraph.")

if __name__ == "__main__":
    main() 