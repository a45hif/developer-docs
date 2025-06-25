#!/usr/bin/env python3

from bittensor.core.metagraph import Metagraph

def main():
    # Initialize metagraph for subnet 1
    print("Initializing metagraph for subnet 1...")
    metagraph = Metagraph(netuid=1, network="finney", sync=True)
    
    # Get complete neuron information for first 5 neurons
    print("=== Complete Neuron Information (First 5 Neurons) ===")
    
    for i in range(min(5, metagraph.n.item())):
        neuron = metagraph.neurons[i]
        print(f"\nNeuron {i}:")
        print(f"  UID: {neuron.uid}")
        print(f"  Hotkey: {neuron.hotkey}")
        print(f"  Coldkey: {neuron.coldkey}")
        print(f"  Stake: τ{neuron.stake:.9f}")
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
        print(f"  Axon IP: {neuron.axon.ip}")
        print(f"  Axon port: {neuron.axon.port}")
        print(f"  ---")

if __name__ == "__main__":
    main() 