#!/usr/bin/env python3
"""
Subnet Economic Parameters Example

This example demonstrates how to access subnet hyperparameters, pool information, and emissions.
"""

from bittensor.core.metagraph import Metagraph

def main():
    # Initialize metagraph for subnet 1
    print("Initializing metagraph for subnet 1...")
    metagraph = Metagraph(netuid=1, network="finney", sync=True)
    
    # Get subnet hyperparameters
    hparams = metagraph.hparams
    print("\n=== Subnet Hyperparameters ===")
    print(f"  Activity cutoff: {hparams.activity_cutoff}")
    print(f"  Adjustment alpha: {hparams.adjustment_alpha}")
    print(f"  Adjustment interval: {hparams.adjustment_interval}")
    print(f"  Alpha high: {hparams.alpha_high}")
    print(f"  Alpha low: {hparams.alpha_low}")
    print(f"  Burn rate: {hparams.burn}")
    print(f"  Max burn: {hparams.max_burn}")
    print(f"  Min burn: {hparams.min_burn}")
    print(f"  Difficulty: {hparams.difficulty}")
    print(f"  Max difficulty: {hparams.max_difficulty}")
    print(f"  Min difficulty: {hparams.min_difficulty}")
    print(f"  Max validators: {hparams.max_validators}")
    print(f"  Tempo: {hparams.tempo}")
    print(f"  Weights version: {hparams.weights_version}")

    # Get pool information
    pool = metagraph.pool
    print("\n=== Subnet Pool ===")
    print(f"  Alpha out: {pool.alpha_out}")
    print(f"  Alpha in: {pool.alpha_in}")
    print(f"  TAO in: {pool.tao_in}")
    print(f"  Subnet volume: {pool.subnet_volume}")
    print(f"  Moving price: {pool.moving_price}")

    # Get emission information
    emissions_info = metagraph.emissions
    print("\n=== Subnet Emissions ===")
    print(f"  Alpha out emission: {emissions_info.alpha_out_emission}")
    print(f"  Alpha in emission: {emissions_info.alpha_in_emission}")
    print(f"  Subnet emission: {emissions_info.subnet_emission}")
    print(f"  TAO in emission: {emissions_info.tao_in_emission}")
    print(f"  Pending alpha emission: {emissions_info.pending_alpha_emission}")
    print(f"  Pending root emission: {emissions_info.pending_root_emission}")

if __name__ == "__main__":
    main() 