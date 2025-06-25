#!/usr/bin/env python3

from bittensor.core.metagraph import Metagraph

def main():
    # Initialize metagraph for subnet 1
    print("Initializing metagraph for subnet 1...")
    metagraph = Metagraph(netuid=1, network="finney", sync=True)
    
    # Get activity information
    active = metagraph.active  # Activity status
    last_update = metagraph.last_update  # Last update blocks
    validator_permit = metagraph.validator_permit  # Validator permissions
    uids = metagraph.uids
    stakes = metagraph.S
    ranks = metagraph.R

    # Analyze activity
    active_count = active.sum().item()
    total_count = len(active)
    print(f"\n=== Activity Analysis ===")
    print(f"Active neurons: {active_count}/{total_count} ({active_count/total_count:.1%})")

    # Find inactive neurons
    inactive_indices = (active == 0).nonzero()[0]
    if len(inactive_indices) > 0:
        print("\n=== Inactive Neurons (First 10) ===")
        for idx in inactive_indices[:10]:  # Show first 10
            uid = uids[idx].item()
            last_block = last_update[idx].item()
            print(f"  UID {uid}: Last update at block {last_block}")
    else:
        print("\nAll neurons are active.")

    # Analyze validator distribution
    validator_count = validator_permit.sum().item()
    print(f"\n=== Validator Analysis ===")
    print(f"Validators: {validator_count}/{total_count} ({validator_count/total_count:.1%})")

    # Find validators
    validator_indices = validator_permit.nonzero()[0]
    if len(validator_indices) > 0:
        print("\n=== Validators ===")
        for idx in validator_indices:
            uid = uids[idx].item()
            stake = stakes[idx].item()
            rank = ranks[idx].item()
            print(f"  UID {uid}: Stake={stake:.2f}, Rank={rank:.4f}")
    else:
        print("\nNo validators found in this subnet.")

if __name__ == "__main__":
    main() 