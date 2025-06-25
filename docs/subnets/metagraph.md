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

**Key functions available:**
- `getUidCount(netuid)` - Get total number of neurons in a subnet
- `getStake(netuid, uid)` - Get neuron's total stake
- `getRank(netuid, uid)` - Get neuron's rank score
- `getTrust(netuid, uid)` - Get neuron's trust score
- `getConsensus(netuid, uid)` - Get neuron's consensus score
- `getIncentive(netuid, uid)` - Get neuron's incentive score
- `getEmission(netuid, uid)` - Get neuron's emission value
- `getDividends(netuid, uid)` - Get neuron's dividends
- `getVtrust(netuid, uid)` - Get neuron's validator trust score
- `getValidatorStatus(netuid, uid)` - Check if neuron is a validator
- `getIsActive(netuid, uid)` - Check if neuron is active
- `getLastUpdate(netuid, uid)` - Get last update block
- `getAxon(netuid, uid)` - Get neuron's network connection info
- `getHotkey(netuid, uid)` - Get neuron's hotkey
- `getColdkey(netuid, uid)` - Get neuron's coldkey

:::tip Smart Contract Integration
For detailed smart contract examples and complete ABI, see the [Metagraph Precompile](../evm-tutorials/metagraph-precompile.md) documentation.
:::

### Polkadot Extrinsics

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

## Troubleshooting

### Common Issues

1. **Sync Failures**: Ensure you're connected to the correct network
2. **Historical Data**: Use archive network for data beyond 300 blocks
3. **Memory Usage**: Use lite mode for large subnets
4. **Network Timeouts**: Increase timeout values for slow connections


## Related Documentation

- [Understanding Neurons](../learn/neurons.md) - Neuron architecture overview
- [Subnet Hyperparameters](./subnet-hyperparameters.md) - Subnet configuration
- [Bittensor CLI Reference](../btcli.md) - Complete btcli documentation
- [Metagraph Precompile](../evm-tutorials/metagraph-precompile.md) - Smart contract access and examples 


## Python code examples