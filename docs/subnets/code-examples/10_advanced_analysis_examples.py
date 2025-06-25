#!/usr/bin/env python3
"""
Advanced Analysis Examples

This example demonstrates advanced analysis techniques including correlations, network efficiency, and stake concentration.
"""

import numpy as np
from bittensor.core.metagraph import Metagraph

def main():
    # Initialize metagraph for subnet 1
    print("Initializing metagraph for subnet 1...")
    metagraph = Metagraph(netuid=1, network="finney", sync=True)
    
    # Get basic metrics
    stakes = metagraph.S
    ranks = metagraph.R
    trust = metagraph.T
    uids = metagraph.uids

    # Correlation analysis between metrics
    print("\n=== Metric Correlations ===")
    try:
        # Calculate correlations
        stake_rank_corr = np.corrcoef(stakes, ranks)[0, 1]
        stake_trust_corr = np.corrcoef(stakes, trust)[0, 1]
        rank_trust_corr = np.corrcoef(ranks, trust)[0, 1]

        print("Metric Correlations:")
        print(f"  Stake vs Rank: {stake_rank_corr:.4f}")
        print(f"  Stake vs Trust: {stake_trust_corr:.4f}")
        print(f"  Rank vs Trust: {rank_trust_corr:.4f}")
    except Exception as e:
        print(f"Could not calculate correlations: {e}")

    # Network efficiency analysis (if weights are available)
    if not metagraph.lite and hasattr(metagraph, 'weights') and metagraph.weights.numel() > 0:
        weights = metagraph.W
        
        print("\n=== Network Efficiency Analysis ===")
        # Calculate network efficiency (average path length)
        non_zero_weights = weights[weights > 0]
        if len(non_zero_weights) > 0:
            avg_weight = non_zero_weights.mean().item()
            weight_std = non_zero_weights.std().item()
            print(f"Network efficiency:")
            print(f"  Average non-zero weight: {avg_weight:.4f}")
            print(f"  Weight standard deviation: {weight_std:.4f}")
            print(f"  Weight distribution CV: {weight_std/avg_weight:.4f}")
    else:
        print("\nWeights not available for network efficiency analysis.")

    # Stake concentration analysis
    print("\n=== Stake Concentration Analysis ===")
    total_stake = stakes.sum().item()
    try:
        stake_percentiles = np.percentile(stakes, [25, 50, 75, 90, 95, 99])
        print("Stake distribution percentiles:")
        for p, val in zip([25, 50, 75, 90, 95, 99], stake_percentiles):
            print(f"  {p}th percentile: {val:.2f} τ")

        # Gini coefficient for stake inequality
        sorted_stakes = np.sort(stakes)
        n = len(sorted_stakes)
        cumulative_stakes = np.cumsum(sorted_stakes)
        gini = (n + 1 - 2 * np.sum(cumulative_stakes) / cumulative_stakes[-1]) / n
        print(f"Stake Gini coefficient: {gini:.4f}")
    except Exception as e:
        print(f"Could not calculate stake concentration metrics: {e}")

if __name__ == "__main__":
    main() 