#!/usr/bin/env python3
"""
Complete Neuron Information Example

This example demonstrates how to access complete neuron objects and their properties.
"""

from bittensor.core.metagraph import Metagraph

def main():
    # Initialize metagraph for subnet 1
    print("Initializing metagraph for subnet 1...")
    metagraph = Metagraph(netuid=1, network="finney", sync=True)
    
    # Get complete neuron objects
    neurons = metagraph.neurons

    print("=== Complete Neuron Information (First 5 Neurons) ===")
    for i, neuron in enumerate(neurons[:5]):  # Show first 5 neurons
        print(f"\nNeuron {i}:")
        print(f"  UID: {neuron.uid}")
        print(f"  Hotkey: {neuron.hotkey}")
        print(f"  Coldkey: {neuron.coldkey}")
        print(f"  Stake: {neuron.stake}")
        print(f"  Rank: {neuron.rank}")
        print(f"  Trust: {neuron.trust}")
        print(f"  Consensus: {neuron.consensus}")
        print(f"  Incentive: {neuron.incentive}")
        print(f"  Emission: {neuron.emission}")
        print(f"  Dividends: {neuron.dividends}")
        print(f"  Active: {neuron.active}")
        print(f"  Last update: {neuron.last_update}")
        print(f"  Validator permit: {neuron.validator_permit}")
        print(f"  Validator trust: {neuron.validator_trust}")
        print(f"  Axon IP: {neuron.axon_info.ip_str()}")
        print(f"  Axon port: {neuron.axon_info.port}")
        print("  ---")

if __name__ == "__main__":
    main() 