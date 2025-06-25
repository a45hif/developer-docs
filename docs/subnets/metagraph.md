---
title: "The Subnet Metagraph"
---

import ThemedImage from '@theme/ThemedImage';
import useBaseUrl from '@docusaurus/useBaseUrl';

# Subnet Metagraph

This page documents the Bittensor subnet metagraph. 

Page Contents:
- [Intro](#intro)
- [Accessing the Metagraph](#accessing-the-metagraph)
- [Metagraph Properties](#metagraph-properties)
- [Data Structures](#data-structures)
- [Performance Considerations](#performance-considerations)
- [Troubleshooting](#troubleshooting)
- [Python Code Examples](#python-code-examples)

Related reading:
- [Understanding Neurons](../learn/neurons.md)
- [Subnet Hyperparameters](./subnet-hyperparameters.md)
- [Bittensor CLI Reference](../btcli.md)
- [Metagraph Precompile](../evm-tutorials/metagraph-precompile.md)

## Intro

The **metagraph** is a core data structure in the Bittensor blockchain that represents the complete state of a subnet at any given block. It contains comprehensive information about all neurons (miners and validators) participating in a subnet, their emissions, bonds, and trust, as well as subnet metrics.

The metagraph serves as a dynamic snapshot of a subnet's neural network, capturing:

- **Neuron Information**: UIDs, hotkeys, coldkeys, network addresses
- **Network Metrics**: Stakes, ranks, trust scores, consensus values
- **Economic Data**: Incentives, emissions, dividends, bonds
- **Network State**: Active status, validator permits, last updates
- **Inter-neuronal Relationships**: Weights and bonds between neurons

The metagraph is continuously updated as the blockchain progresses, reflecting the real-time state of the subnet's collective intelligence.



Related reading:

- [Understanding Neurons](../learn/neurons.md) - Neuron architecture overview
- [Subnet Hyperparameters](./subnet-hyperparameters.md) - Subnet configuration
- [Bittensor CLI Reference](../btcli.md) - Complete btcli documentation
- [Metagraph Precompile](../evm-tutorials/metagraph-precompile.md) - Smart contract access and examples 




## Accessing the Metagraph

You can access metagraph data through multiple interfaces:

### Bittensor CLI (btcli)

The `btcli` command-line interface provides easy access to metagraph information:

```bash
# View metagraph for a specific subnet
btcli subnets metagraph --netuid 14 --network finney
```
```console
                                                    Subnet 14: TAOHash
                                                     Network: finney

 UID ┃ Stake (ξ) ┃ Alpha (ξ) ┃   Tao (τ) ┃ Dividends ┃ Incentive ┃ Emissions (ξ) ┃ Hotk… ┃ Coldkey ┃ Identity
━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━
 29  │ 271.67k ξ │ 254.83k ξ │  τ 16.84k │ 0.129183  │ 0.000000  │  19.122456 ξ  │ 5Cf4… │ 5CKhH8  │ Owner14 (*Owner)
  3  │ 387.08k ξ │  61.46k ξ │ τ 325.62k │ 0.184314  │ 0.000000  │  27.280861 ξ  │ 5C59… │ 5GZSAg  │ 

...
 ```

### Python SDK

The Bittensor Python SDK [Metagraph module](pathname:///python-api/html/autoapi/bittensor/core/metagraph/index.html) provides programmatic access to metagraph data:

```python
from bittensor.core.metagraph import Metagraph
from bittensor.core.subtensor import Subtensor

# Initialize metagraph for subnet 1
metagraph = Metagraph(netuid=1, network="finney", sync=True)
```


### Smart Contract Access (Metagraph Precompile)

For smart contract integration, you can access metagraph data through the **Metagraph Precompile** at address `0x0000000000000000000000000000000000000802`. This provides read-only access to individual neuron metrics and network information.

:::tip Smart Contract Integration
For detailed smart contract examples and complete ABI, see the [Metagraph Precompile](../evm-tutorials/metagraph-precompile.md) documentation.
:::

### Polkadot Extrinsics

Advanced users can query the metagraph directly through Polkadot extrinsics using the PolkadotJS browser application, or with the PolkadotJS JavaScript SDK.

## Metagraph Properties


| Name | Description |
|------|--|
| `netuid`  | Unique subnet identifier |
| `network`  | Network name (finney, test, local) |
| `version`  | Bittensor version number |
| `n`  | Total number of neurons |
| `block`  | Current blockchain block number |
| `total_stake`  | Total stake across all neurons |
| **Stake** / `S` | Total stake of each neuron |
| **Alpha Stake** / `AS` | Alpha token stake |
| **Tao Stake** / `TS` | TAO token stake |
| **Ranks** / `R` | Performance ranking scores |
| **Trust** / `T` | Trust scores from other neurons |
| **Validator Trust** / `Tv` | Validator-specific trust scores |
| **Consensus** / `C` | Network consensus alignment |
| **Incentive** / `I` | Reward incentive scores |
| **Emission** / `E` | Token emission rates |
| **Dividends** / `D` | Dividend distributions |
| **Bonds** / `B` | Inter-neuronal bonds |
| **Weights** / `W` | Weight matrix between neurons |
| `uids` |  Unique neuron identifiers |
| `hotkeys` |  Neuron hotkey addresses |
| `coldkeys` |  Neuron coldkey addresses |
| `addresses` |  Network IP addresses |
| `axons` |  Network connection details |
| `neurons` |  Complete neuron objects |
| `active` |  Neuron activity status |
| `last_update` |  Last update block numbers |
| `validator_permit` |  Bool array indicating whether each neuron can set weights (act as validator) |
| `name` |  Subnet name |
| `symbol` |  Subnet token symbol |
| `network_registered_at` |  Registration block |
| `num_uids` |  Current number of neurons |
| `max_uids` |  Maximum allowed neurons |
| `identities` |  List of chain identities |
| `identity` |  Subnet identity information |
| `pruning_score` |  List of pruning scores |
| `block_at_registration` |  List of registration blocks |
| `tao_dividends_per_hotkey` |  TAO dividends by hotkey |
| `alpha_dividends_per_hotkey` |  Alpha dividends by hotkey |
| `last_step` |  Last step block number |
| `tempo` |  Block interval for updates |
| `blocks_since_last_step` |  Blocks since last step |
| `owner_coldkey` |  Subnet owner coldkey |
| `owner_hotkey` |  Subnet owner hotkey |
| `hparams` |  Subnet hyperparameters (MetagraphInfoParams) |
| `pool` |  Liquidity pool information (MetagraphInfoPool) |
| `emissions` |  Emission configuration (MetagraphInfoEmissions) |

## Data Structures

### Neuron Object

Each neuron in the metagraph contains:

```python
class NeuronInfo:
    uid: int                    # Unique identifier
    hotkey: str                 # Hotkey address
    coldkey: str                # Coldkey address
    stake: float                # Total stake
    rank: float                 # Performance rank
    trust: float                # Trust score
    consensus: float            # Consensus score
    incentive: float            # Incentive score
    emission: float             # Emission rate
    dividends: float            # Dividend amount
    validator_trust: float      # Validator trust
    active: bool                # Activity status
    last_update: int            # Last update block
    validator_permit: bool      # Validator permission
    weights: list               # Weight assignments
    bonds: list                 # Bond investments
    axon_info: AxonInfo         # Network connection
```

### Axon Information

```python
class AxonInfo:
    hotkey: str                 # Neuron hotkey
    coldkey: str                # Neuron coldkey
    ip: int                     # IP address
    port: int                   # Port number
    ip_type: int                # IP type
    version: int                # Protocol version
    placeholder1: int           # Reserved field
    placeholder2: int           # Reserved field
```

:::note AxonInfo vs Smart Contract AxonInfo
The Python SDK `AxonInfo` structure differs from the smart contract version. The smart contract `AxonInfo` includes `block`, `version`, `ip`, `port`, `ip_type`, and `protocol` fields, while the Python SDK version includes additional fields for hotkey, coldkey, and placeholders.
:::

### MetagraphInfoParams

```python
class MetagraphInfoParams:
    activity_cutoff: int        # Activity cutoff threshold
    adjustment_alpha: float     # Adjustment alpha parameter
    adjustment_interval: int    # Adjustment interval
    alpha_high: float           # Alpha high threshold
    alpha_low: float            # Alpha low threshold
    bonds_moving_avg: int       # Bonds moving average
    burn: float                 # Burn amount
    commit_reveal_period: int   # Commit reveal period
    commit_reveal_weights_enabled: bool  # Commit reveal weights enabled
    difficulty: int             # Network difficulty
    immunity_period: int        # Immunity period
    kappa: float                # Kappa parameter
    liquid_alpha_enabled: bool  # Liquid alpha enabled
    max_burn: float             # Maximum burn
    max_difficulty: int         # Maximum difficulty
    max_regs_per_block: int     # Max registrations per block
    max_validators: int         # Maximum validators
    max_weights_limit: int      # Maximum weights limit
    min_allowed_weights: int    # Minimum allowed weights
    min_burn: float             # Minimum burn
    min_difficulty: int         # Minimum difficulty
    pow_registration_allowed: bool  # POW registration allowed
    registration_allowed: bool  # Registration allowed
    rho: float                  # Rho parameter
    serving_rate_limit: int     # Serving rate limit
    target_regs_per_interval: int  # Target registrations per interval
    tempo: int                  # Tempo
    weights_rate_limit: int     # Weights rate limit
    weights_version: int        # Weights version
```

### MetagraphInfoPool

```python
class MetagraphInfoPool:
    alpha_out: float            # Alpha out amount
    alpha_in: float             # Alpha in amount
    tao_in: float               # TAO in amount
    subnet_volume: float        # Subnet volume
    moving_price: float         # Moving price
```

### MetagraphInfoEmissions

```python
class MetagraphInfoEmissions:
    alpha_out_emission: float   # Alpha out emission
    alpha_in_emission: float    # Alpha in emission
    subnet_emission: float      # Subnet emission
    tao_in_emission: float      # TAO in emission
    pending_alpha_emission: float  # Pending alpha emission
    pending_root_emission: float   # Pending root emission
```

## Performance Considerations

### Lite vs Full Sync

- **Lite Mode** (`lite=True`): Faster sync, excludes weights and bonds
- **Full Mode** (`lite=False`): Complete data including weight matrices

### Caching

The metagraph supports local caching:

```python
# Save metagraph for later use
metagraph.save()

# Load cached metagraph
metagraph.load()

# Custom save directory
metagraph.save(root_dir=['/custom', 'path'])
```

## Troubleshooting

### Common Issues

1. **Sync Failures**: Ensure you're connected to the correct network
2. **Historical Data**: Use archive network for data beyond 300 blocks
3. **Memory Usage**: Use lite mode for large subnets
4. **Network Timeouts**: Increase timeout values for slow connections


## Python Code Examples

This section provides practical examples of working with the Bittensor metagraph using the Python SDK. Each example demonstrates different aspects of metagraph analysis and data extraction.

**Prerequisites**:
- Bittensor Python SDK installed (`pip install bittensor`)
- Network connection to access Bittensor blockchain
- Python 3.7+ environment


### 1. Basic Metagraph Information

This example shows how to access basic metagraph metadata and subnet information:

```python title="01_basic_metagraph_info.py"
#!/usr/bin/env python3

from bittensor.core.metagraph import Metagraph
from bittensor.core.subtensor import Subtensor

def main():
    # Initialize metagraph for subnet 1
    print("Initializing metagraph for subnet 1...")
    metagraph = Metagraph(netuid=1, network="finney", sync=True)
    
    # Get basic metagraph metadata
    print("\n=== Basic Metagraph Metadata ===")
    print(f"Network: {metagraph.network}")
    print(f"Subnet UID: {metagraph.netuid}")
    print(f"Total neurons: {metagraph.n.item()}")
    print(f"Current block: {metagraph.block.item()}")
    print(f"Version: {metagraph.version.item()}")

    # Get subnet information
    print("\n=== Subnet Information ===")
    print(f"Subnet name: {metagraph.name}")
    print(f"Subnet symbol: {metagraph.symbol}")
    print(f"Registered at block: {metagraph.network_registered_at}")
    print(f"Max UIDs: {metagraph.max_uids}")
    print(f"Owner: {metagraph.owner_coldkey}")

if __name__ == "__main__":
    main() 
```

[View source file](https://github.com/latent-to/developer-docs/tree/main/static/code-examples/01_basic_metagraph_info.py)

**Key Features:**
- Initialize metagraph for a specific subnet
- Access basic metadata (network, subnet UID, total neurons, current block)
- Retrieve subnet identity information (name, symbol, registration details)

### 2. Neuron Metrics Analysis

This example demonstrates stake distribution and neuron metrics analysis:

```python title="02_neuron_metrics_analysis.py"
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
```

[View source file](https://github.com/latent-to/developer-docs/tree/main/static/code-examples/02_neuron_metrics_analysis.py)

**Key Features:**
- Analyze total, average, highest, and lowest stake across neurons
- Find top 10 staked neurons
- Calculate alpha vs TAO stake distribution ratios
- Handle both alpha and TAO token stakes

### 3. Performance and Ranking Analysis

This example shows how to analyze neuron performance, ranks, and trust scores:

```python title="03_performance_ranking_analysis.py"
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
```

[View source file](https://github.com/latent-to/developer-docs/tree/main/static/code-examples/03_performance_ranking_analysis.py)

**Key Features:**
- Find top performing neurons by rank
- Analyze trust score distribution (mean, std dev, min/max)
- Identify most trusted validators
- Access consensus scores and validator trust metrics

### 4. Economic Analysis

This example demonstrates analysis of economic metrics like incentives, emissions, and dividends:

```python title="04_economic_analysis.py"
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
```

[View source file](https://github.com/latent-to/developer-docs/tree/main/static/code-examples/04_economic_analysis.py)

**Key Features:**
- Calculate total and average incentives across the network
- Find highest incentivized neurons
- Analyze dividend distribution statistics
- Correlate incentives with emissions and dividends

### 5. Network Connectivity Analysis

This example shows how to analyze network addresses and axon information:

```python title="05_network_connectivity_analysis.py"
#!/usr/bin/env python3

from bittensor.core.metagraph import Metagraph

def main():
    # Initialize metagraph for subnet 1
    print("Initializing metagraph for subnet 1...")
    metagraph = Metagraph(netuid=1, network="finney", sync=True)
    
    # Get network information
    axons = metagraph.axons
    uids = metagraph.uids

    # Analyze network addresses
    addresses = [axon.ip for axon in axons]
    unique_addresses = set(addresses)
    unique_hotkeys = set(metagraph.hotkeys)
    unique_coldkeys = set(metagraph.coldkeys)

    print(f"\n=== Network Address Analysis ===")
    print(f"Total unique addresses: {len(unique_addresses)}")
    print(f"Total unique hotkeys: {len(unique_hotkeys)}")
    print(f"Total unique coldkeys: {len(unique_coldkeys)}")

    # Find neurons sharing addresses
    address_to_uids = {}
    for i, address in enumerate(addresses):
        if address not in address_to_uids:
            address_to_uids[address] = []
        address_to_uids[address].append(uids[i].item())

    print(f"\n=== Neurons Sharing Addresses ===")
    for address, uids_list in address_to_uids.items():
        if len(uids_list) > 1:
            print(f"  Address {address}: UIDs {uids_list}")

    # Show axon details for first few neurons
    print(f"\n=== Axon Details (First 5 Neurons) ===")
    for i in range(min(5, len(axons))):
        axon = axons[i]
        uid = uids[i].item()
        hotkey = metagraph.hotkeys[i][:10] + "..."
        print(f"  UID {uid}: IP={axon.ip}, Port={axon.port}, Hotkey={hotkey}")

if __name__ == "__main__":
    main() 
```

[View source file](https://github.com/latent-to/developer-docs/tree/main/static/code-examples/05_network_connectivity_analysis.py)

**Key Features:**
- Count unique network addresses, hotkeys, and coldkeys
- Identify neurons sharing the same network addresses
- Display detailed axon information for neurons
- Analyze network topology and connectivity patterns



### 6. Weight Matrix Analysis

This example demonstrates weight matrix analysis (requires `lite=False`):

```python title="06_weight_matrix_analysis.py"
#!/usr/bin/env python3

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
```

[View source file](https://github.com/latent-to/developer-docs/tree/main/static/code-examples/06_weight_matrix_analysis.py)

**Key Features:**
- Analyze weight matrix shape and statistics
- Find neurons receiving the most weights (incoming connections)
- Find neurons sending the most weights (outgoing connections)
- Identify the strongest connection between neurons
- Requires full sync mode for weight data access

### 7. Bond Analysis

This example shows bond matrix analysis (requires `lite=False`):

```python title="07_bond_analysis.py"
#!/usr/bin/env python3

from bittensor.core.metagraph import Metagraph

def main():
    # Initialize metagraph for subnet 1 with full sync (not lite)
    print("Initializing metagraph for subnet 1 (full sync)...")
    metagraph = Metagraph(netuid=1, network="finney", lite=False, sync=True)
    
    uids = metagraph.uids
    
    # Get bond matrix (requires lite=False)
    if not metagraph.lite and hasattr(metagraph, 'bonds') and metagraph.bonds.size > 0:
        bonds = metagraph.B  # Bond matrix
        
        print(f"\n=== Bond Matrix Analysis ===")
        print(f"Bond matrix shape: {bonds.shape}")
        print(f"Total bonds: {bonds.sum().item():.4f}")
        print(f"Average bond: {bonds.mean().item():.4f}")
        
        # Find neurons with most bonds
        bonds_received = bonds.sum(axis=0)  # Sum of incoming bonds
        top_bonded = bonds_received.argsort()[::-1][:10]
        print("\n=== Top 10 Bonded Neurons ===")
        for i, idx in enumerate(top_bonded):
            uid = uids[idx].item()
            total_bonds = bonds_received[idx].item()
            print(f"  {i+1}. UID {uid}: {total_bonds:.4f}")
    else:
        print("Bonds not available. Make sure to use lite=False when initializing the metagraph.")

if __name__ == "__main__":
    main() 
```

[View source file](https://github.com/latent-to/developer-docs/tree/main/static/code-examples/07_bond_analysis.py)

**Key Features:**
- Analyze bond matrix shape and total bonds
- Find neurons with the most bonds
- Calculate average bond values
- Requires full sync mode for bond data access

### 8. Neuron Activity Analysis

This example demonstrates neuron activity and validator status analysis:

```python title="08_neuron_activity_analysis.py"
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
```

[View source file](https://github.com/latent-to/developer-docs/tree/main/static/code-examples/08_neuron_activity_analysis.py)

**Key Features:**
- Calculate active vs inactive neuron ratios
- Find inactive neurons and their last update blocks
- Analyze validator distribution and permissions
- Display validator details with stake and rank information

### 9. Subnet Economic Parameters

This example shows how to access subnet hyperparameters, pool, and emissions:

```python title="09_subnet_economic_parameters.py"
#!/usr/bin/env python3

from bittensor.core.metagraph import Metagraph

def main():
    # Initialize metagraph for subnet 1
    print("Initializing metagraph for subnet 1...")
    metagraph = Metagraph(netuid=1, network="finney", sync=True)
    
    # Get subnet hyperparameters
    hparams = metagraph.hparams
    print(f"\n=== Subnet Hyperparameters ===")
    print(f"  Activity cutoff: {hparams.activity_cutoff}")
    print(f"  Adjustment alpha: {hparams.adjustment_alpha}")
    print(f"  Adjustment interval: {hparams.adjustment_interval}")
    print(f"  Alpha high: {hparams.alpha_high}")
    print(f"  Alpha low: {hparams.alpha_low}")
    print(f"  Burn rate: {hparams.burn_rate}")
    print(f"  Max burn: {hparams.max_burn}")
    print(f"  Min burn: {hparams.min_burn}")
    print(f"  Difficulty: {hparams.difficulty}")
    print(f"  Max difficulty: {hparams.max_difficulty}")
    print(f"  Min difficulty: {hparams.min_difficulty}")
    print(f"  Max validators: {hparams.max_validators}")
    print(f"  Tempo: {hparams.tempo}")
    print(f"  Weights version: {hparams.weights_version}")

    # Get subnet pool information
    pool = metagraph.pool
    print(f"\n=== Subnet Pool ===")
    print(f"  Alpha out: {pool.alpha_out}")
    print(f"  Alpha in: {pool.alpha_in}")
    print(f"  TAO in: {pool.tao_in}")
    print(f"  Subnet volume: {pool.subnet_volume}")
    print(f"  Moving price: {pool.moving_price}")

    # Get subnet emissions
    emissions = metagraph.emissions
    print(f"\n=== Subnet Emissions ===")
    print(f"  Alpha out emission: {emissions.alpha_out_emission}")
    print(f"  Alpha in emission: {emissions.alpha_in_emission}")
    print(f"  Subnet emission: {emissions.subnet_emission}")
    print(f"  TAO in emission: {emissions.tao_in_emission}")
    print(f"  Pending alpha emission: {emissions.pending_alpha_emission}")
    print(f"  Pending root emission: {emissions.pending_root_emission}")

if __name__ == "__main__":
    main() 
```

[View source file](https://github.com/latent-to/developer-docs/tree/main/static/code-examples/09_subnet_economic_parameters.py)

**Key Features:**
- Access subnet hyperparameters (activity cutoff, adjustment alpha, etc.)
- View liquidity pool information (alpha/TAO amounts, volume, price)
- Analyze emission configuration and pending emissions
- Access economic parameters that control subnet behavior

### 10. Advanced Analysis Examples

This example demonstrates advanced analysis techniques including correlations and Gini coefficient:

```python title="10_advanced_analysis_examples.py"
#!/usr/bin/env python3

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
    if not metagraph.lite and hasattr(metagraph, 'weights') and metagraph.weights.size > 0:
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
```

[View source file](https://github.com/latent-to/developer-docs/tree/main/static/code-examples/10_advanced_analysis_examples.py)

**Key Features:**
- Calculate correlations between stake, rank, and trust metrics
- Analyze network efficiency through weight distribution
- Calculate stake concentration using percentiles
- Compute Gini coefficient for stake inequality measurement
- Handle missing weight data gracefully



### 11. Async Usage

This example demonstrates async metagraph usage:

```python title="11_async_usage.py"
#!/usr/bin/env python3

import asyncio
from bittensor.core.metagraph import async_metagraph

async def analyze_metagraph():
    # Create async metagraph
    print("Creating async metagraph...")
    metagraph = await async_metagraph(netuid=1, network="finney", lite=False)
    
    # Perform analysis
    stakes = metagraph.S
    print(f"Total stake: {stakes.sum().item():.2f}")
    
    # Sync to latest block
    print("Syncing to latest block...")
    await metagraph.sync()
    print(f"Synced to block: {metagraph.block.item()}")

async def use_factory():
    print("Using factory function...")
    metagraph = await async_metagraph(netuid=1, sync=True)
    print(f"Factory metagraph has {metagraph.n.item()} neurons")

async def main():
    print("=== Async Metagraph Analysis ===")
    await analyze_metagraph()
    print("\n=== Factory Function Example ===")
    await use_factory()

if __name__ == "__main__":
    # Run async analysis
    asyncio.run(main()) 
```

[View source file](https://github.com/latent-to/developer-docs/tree/main/static/code-examples/11_async_usage.py)

**Key Features:**
- Use async metagraph for non-blocking operations
- Sync to latest block asynchronously
- Demonstrate factory function usage
- Handle async operations with proper await syntax

### 12. Complete Neuron Information

This example shows how to access complete neuron object information:

```python title="12_complete_neuron_information.py"
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
```

[View source file](https://github.com/latent-to/developer-docs/tree/main/static/code-examples/12_complete_neuron_information.py)

**Key Features:**
- Display comprehensive neuron information for multiple neurons
- Show all available neuron properties in a structured format
- Access complete neuron objects with all metadata
- Format output for easy reading and analysis

### 13. Common Use Cases

This example demonstrates common use cases like subnet analysis and validator selection:

```python title="13_common_use_cases.py"
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
```

[View source file](https://github.com/latent-to/developer-docs/tree/main/static/code-examples/13_common_use_cases.py)

**Key Features:**
- Analyze subnet health and activity rates
- Find top validators by rank
- Analyze weight distribution for network topology
- Provide reusable functions for common analysis tasks
- Handle errors gracefully for missing data

### Running the Examples

All examples can be run directly from the command line:

```bash
# Navigate to the code examples directory
cd docs/subnets/code-examples

# Run individual examples
python3 01_basic_metagraph_info.py
python3 02_neuron_metrics_analysis.py
# ... etc

# Or run all examples in sequence
for script in *.py; do
    echo "Running $script..."
    python3 "$script"
    echo "---"
done
```

