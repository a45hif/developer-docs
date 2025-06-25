---
title: "The Subnet Metagraph"
---

import ThemedImage from '@theme/ThemedImage';
import useBaseUrl from '@docusaurus/useBaseUrl';

# Subnet Metagraph

The **metagraph** is a core on-chain data structure in the Bittensor blockchain that represents the complete state of a subnet at any given block. It contains comprehensive information about all neurons (miners and validators) participating in a subnet, their relationships, and network metrics.

## Overview

The metagraph serves as a dynamic snapshot of a subnet's neural network, capturing:

- **Neuron Information**: UIDs, hotkeys, coldkeys, network addresses
- **Network Metrics**: Stakes, ranks, trust scores, consensus values
- **Economic Data**: Incentives, emissions, dividends, bonds
- **Network State**: Active status, validator permits, last updates
- **Inter-neuronal Relationships**: Weights and bonds between neurons

The metagraph is continuously updated as the blockchain progresses, reflecting the real-time state of the subnet's collective intelligence.

## Accessing the Metagraph

You can access metagraph data through multiple interfaces:

### 1. Bittensor CLI (btcli)

The `btcli` command-line interface provides easy access to metagraph information:

```bash
# View metagraph for a specific subnet
btcli subnets metagraph --netuid 1

# View root network metagraph (netuid 0)
btcli subnets metagraph --netuid 0

# View metagraph on testnet
btcli subnets metagraph --netuid 1 --network test

# Configure metagraph display columns
btcli config metagraph --reset
```

**Available btcli metagraph commands:**
- `btcli subnets metagraph` - Display subnet metagraph
- `btcli subnet metagraph` - Alternative syntax
- `btcli s metagraph` - Short alias
- `btcli config metagraph` - Configure display columns

### 2. Python SDK

The Bittensor Python SDK provides programmatic access to metagraph data:

```python
import bittensor as bt

# Create and sync metagraph
metagraph = bt.metagraph(netuid=1)
metagraph.sync()

# Access metagraph properties
total_stake = metagraph.S
neuron_ranks = metagraph.R
neuron_incentives = metagraph.I
neuron_emissions = metagraph.E
neuron_consensus = metagraph.C
neuron_trust = metagraph.T
neuron_validator_trust = metagraph.Tv
neuron_dividends = metagraph.D
neuron_bonds = metagraph.B
neuron_weights = metagraph.W

# Access neuron information
hotkeys = metagraph.hotkeys
coldkeys = metagraph.coldkeys
addresses = metagraph.addresses
axons = metagraph.axons
neurons = metagraph.neurons
```

### 3. Polkadot Extrinsics

For advanced users, you can query metagraph data directly through Polkadot extrinsics using the Substrate API.

## Metagraph Properties

### Core Network Properties

| Property | Type | Description |
|----------|------|-------------|
| `netuid` | int | Unique subnet identifier |
| `network` | str | Network name (finney, test, local) |
| `version` | Tensor | Bittensor version number |
| `n` | Tensor | Total number of neurons |
| `block` | Tensor | Current blockchain block number |

### Neuron Metrics

| Property | Accessor | Type | Description |
|----------|----------|------|-------------|
| **Stake** | `S` | Tensor | Total stake of each neuron |
| **Alpha Stake** | `AS` | Tensor | Alpha token stake |
| **Tao Stake** | `TS` | Tensor | TAO token stake |
| **Ranks** | `R` | Tensor | Performance ranking scores |
| **Trust** | `T` | Tensor | Trust scores from other neurons |
| **Validator Trust** | `Tv` | Tensor | Validator-specific trust scores |
| **Consensus** | `C` | Tensor | Network consensus alignment |
| **Incentive** | `I` | Tensor | Reward incentive scores |
| **Emission** | `E` | Tensor | Token emission rates |
| **Dividends** | `D` | Tensor | Dividend distributions |
| **Bonds** | `B` | Tensor | Inter-neuronal bonds |
| **Weights** | `W` | Tensor | Weight matrix between neurons |

### Neuron Information

| Property | Type | Description |
|----------|------|-------------|
| `uids` | Tensor | Unique neuron identifiers |
| `hotkeys` | list[str] | Neuron hotkey addresses |
| `coldkeys` | list[str] | Neuron coldkey addresses |
| `addresses` | list[str] | Network IP addresses |
| `axons` | list[AxonInfo] | Network connection details |
| `neurons` | list[NeuronInfo] | Complete neuron objects |

### Network State

| Property | Type | Description |
|----------|------|-------------|
| `active` | Tensor | Neuron activity status |
| `last_update` | Tensor | Last update block numbers |
| `validator_permit` | Tensor | Validator permission flags |

## Metagraph Information

The metagraph also contains subnet-level information:

### Subnet Identity
- `name`: Subnet name
- `symbol`: Subnet token symbol
- `network_registered_at`: Registration block
- `num_uids`: Current number of neurons
- `max_uids`: Maximum allowed neurons
- `identities`: List of chain identities
- `identity`: Subnet identity information
- `pruning_score`: List of pruning scores
- `block_at_registration`: List of registration blocks
- `tao_dividends_per_hotkey`: TAO dividends by hotkey
- `alpha_dividends_per_hotkey`: Alpha dividends by hotkey
- `last_step`: Last step block number
- `tempo`: Block interval for updates
- `blocks_since_last_step`: Blocks since last step
- `owner_coldkey`: Subnet owner coldkey
- `owner_hotkey`: Subnet owner hotkey

### Economic Parameters
- `hparams`: Subnet hyperparameters (MetagraphInfoParams)
- `pool`: Liquidity pool information (MetagraphInfoPool)
- `emissions`: Emission configuration (MetagraphInfoEmissions)

## Working with the Metagraph

### Basic Usage

```python
import bittensor as bt

# Initialize metagraph
metagraph = bt.metagraph(netuid=1, network='finney')

# Sync with latest block
metagraph.sync()

# Access basic information
print(f"Subnet has {metagraph.n.item()} neurons")
print(f"Current block: {metagraph.block.item()}")

# Get neuron stakes
stakes = metagraph.S
print(f"Total stake: {stakes.sum().item()}")

# Find top-ranked neurons
ranks = metagraph.R
top_neurons = ranks.argsort(descending=True)[:5]
print(f"Top 5 neurons: {top_neurons.tolist()}")
```

### Historical Analysis

```python
# Sync to specific block for historical analysis
metagraph.sync(block=100000)

# Save metagraph state
metagraph.save()

# Load saved metagraph
metagraph.load()

# Load from specific directory
metagraph.load_from_path("/path/to/metagraphs/")
```

### Advanced Usage

```python
# Use lite mode for faster syncing (excludes weights/bonds)
metagraph = bt.metagraph(netuid=1, lite=True)

# Full sync with weights and bonds
metagraph.sync(lite=False)

# Access weight matrix
weights = metagraph.W
print(f"Weight matrix shape: {weights.shape}")

# Get neuron connections
for i, neuron_weights in enumerate(weights):
    connections = (neuron_weights > 0).sum()
    print(f"Neuron {i} has {connections} connections")

# Access axon information
for axon in metagraph.axons:
    print(f"Neuron at {axon.ip_str()}:{axon.port}")
```

### Async Usage

```python
import asyncio
import bittensor as bt

async def analyze_metagraph():
    # Create async metagraph
    metagraph = bt.AsyncMetagraph(netuid=1)
    
    async with metagraph as mg:
        # Metagraph is automatically synced
        print(f"Synced metagraph with {mg.n.item()} neurons")
        
        # Perform analysis
        total_stake = mg.S.sum().item()
        print(f"Total subnet stake: {total_stake}")

# Run async analysis
asyncio.run(analyze_metagraph())

# Alternative: Use factory function
async def use_factory():
    metagraph = await bt.async_metagraph(netuid=1, sync=True)
    print(f"Factory metagraph has {metagraph.n.item()} neurons")
```

## Metagraph Data Structure

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
    difficulty: int             # Network difficulty
    immunity_period: int        # Immunity period
    kappa: float                # Kappa parameter
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

### Archive Network

For historical data beyond 300 blocks:

```python
# Use archive network for historical analysis
subtensor = bt.subtensor(network='archive')
metagraph = bt.metagraph(netuid=1, subtensor=subtensor)
metagraph.sync(block=historical_block)
```

## Common Use Cases

### 1. Subnet Analysis

```python
# Analyze subnet health
def analyze_subnet(netuid):
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
```

### 2. Validator Selection

```python
# Find top validators
def get_top_validators(netuid, top_k=10):
    metagraph = bt.metagraph(netuid=netuid)
    metagraph.sync()
    
    # Get validator permits
    validator_mask = metagraph.validator_permit
    
    # Get ranks for validators only
    validator_ranks = metagraph.R[validator_mask]
    validator_uids = metagraph.uids[validator_mask]
    
    # Sort by rank
    sorted_indices = validator_ranks.argsort(descending=True)
    top_validators = validator_uids[sorted_indices][:top_k]
    
    return top_validators.tolist()
```

### 3. Network Monitoring

```python
# Monitor network changes
def monitor_network(netuid, interval=60):
    import time
    
    while True:
        metagraph = bt.metagraph(netuid=netuid)
        metagraph.sync()
        
        print(f"Block {metagraph.block.item()}: {metagraph.n.item()} neurons")
        time.sleep(interval)
```

### 4. Weight Analysis

```python
# Analyze weight distribution
def analyze_weights(netuid):
    metagraph = bt.metagraph(netuid=netuid, lite=False)
    metagraph.sync()
    
    weights = metagraph.W
    print(f"Weight matrix shape: {weights.shape}")
    
    # Find neurons with most incoming weights
    incoming_weights = weights.sum(dim=0)
    top_receivers = incoming_weights.argsort(descending=True)[:10]
    print(f"Top 10 weight receivers: {top_receivers.tolist()}")
    
    # Find neurons with most outgoing weights
    outgoing_weights = weights.sum(dim=1)
    top_senders = outgoing_weights.argsort(descending=True)[:10]
    print(f"Top 10 weight senders: {top_senders.tolist()}")
```

## Troubleshooting

### Common Issues

1. **Sync Failures**: Ensure you're connected to the correct network
2. **Historical Data**: Use archive network for data beyond 300 blocks
3. **Memory Usage**: Use lite mode for large subnets
4. **Network Timeouts**: Increase timeout values for slow connections

### Error Handling

```python
try:
    metagraph = bt.metagraph(netuid=1)
    metagraph.sync()
except Exception as e:
    print(f"Failed to sync metagraph: {e}")
    # Handle error appropriately
```

### Debugging

```python
# Get metagraph metadata
metadata = metagraph.metadata()
print(f"Metagraph metadata: {metadata}")

# Get state dictionary
state = metagraph.state_dict()
print(f"State keys: {list(state.keys())}")

# String representation
print(str(metagraph))  # e.g., "metagraph(netuid:1, n:100, block:500, network:finney)"
```

## Related Documentation

- [Understanding Neurons](../learn/neurons.md) - Neuron architecture overview
- [Subnet Hyperparameters](./subnet-hyperparameters.md) - Subnet configuration
- [Bittensor CLI Reference](../btcli.md) - Complete btcli documentation
- [Metagraph Precompile](../evm-tutorials/metagraph-precompile.md) - Smart contract access 