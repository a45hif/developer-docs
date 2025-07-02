---
title: "Glossary"
---

# Glossary

## A 

### Active UID

A UID slot that is considered active within a specific subnet, allowing the associated hotkey to participate as a subnet validator or subnet miner.

**See also:** [Subnet Miners](./miners/), [Subnet Validators](./validators/)

### Archive Node

A type of public subtensor node that stores the entire blockchain history, allowing for full data access and querying capabilities.

**See also:** [Subtensor Nodes](./subtensor-nodes/), [Managing Subtensor Connections](./sdk/managing-subtensor-connections.md)

### Axon

A module in the Bittensor API that uses the FastAPI library to create and run API servers. Axons receive incoming Synapse objects. Typically, an Axon is the entry point advertised by a subnet miner on the Bittensor blockchain, allowing subnet validators to communicate with the miner.

**See also:** [Subnet Miners](./miners/), [Subnet Validators](./validators/)

## B

### Bicameral Legislature

A two-tier legislative system comprising the Triumvirate and the Senate for proposal approval.

**See also:** [Governance](./governance.md), [Senate](./senate.md)

### Bittensor Wallet

A digital wallet that holds the core ownership in the Bittensor network and serves as the user's identity technology underlying all operations.

**See also:** [Wallets](./getting-started/wallets.md), [Working with Keys](./working-with-keys.md)

### Block

A unit of data in the Bittensor blockchain, containing a collection of transactions and a unique identifier (block hash). A single block is processed every 12 seconds in the Bittensor blockchain. 

**See also:** [Subtensor API](./sdk/subtensor-api.md)

## C

### Coldkey

A component of a Bittensor wallet responsible for securely storing funds and performing high-risk operations such as transfers and staking. It is encrypted on the user's device. This is analogous to a private key.

**See also:** [Coldkey-Hotkey Security](./getting-started/coldkey-hotkey-security.md), [Working with Keys](./working-with-keys.md)

### Coldkey-hotkey pair

A combination of two keys, a coldkey for secure storage and high-risk operations, and a hotkey for less secure operations and network interactions.

**See also:** [Coldkey-Hotkey Security](./getting-started/coldkey-hotkey-security.md), [Working with Keys](./working-with-keys.md)

### Commit Reveal

The commit reveal feature is designed to solve the weight-copying problem by giving would-be weight-copiers access only to stale weights. Copying stale weights should result in validators departing from consensus.

**See also:** [Commit Reveal](./subnets/commit-reveal.md)

### Consensus Score

The consensus score is calculated as the stake-weighted median of all weights assigned to a specific neuron by validators. This creates a consensus threshold that filters out outlier weights, ensuring that only weights near the median consensus are used in final rank calculations.

**See also:** [Yuma Consensus](./yuma-consensus.md), [Consensus-Based Weights](./subnets/consensus-based-weights.md)

#### Mathematical Definition:

For each neuron $j$, the consensus score $C_j$ is calculated as:
$$
C_j = \text{weighted\_median}(\{w_{ij} \mid i \in \text{validators}\}, \{s_i \mid i \in \text{validators}\}, \kappa)
$$

Where:
- $w_{ij}$ is the weight assigned by validator $i$ to neuron $j$
- $s_i$ is the stake of validator $i$
- $\kappa$ is the consensus majority ratio (typically 51%)
- $\text{weighted\_median}$ is the stake-weighted median function

Calculation Process:
1. **Weight collection**: Gather all weights assigned to each neuron by validators
2. **Stake weighting**: Apply stake weights to validator opinions
3. **Median calculation**: Find stake-weighted median using κ parameter (typically 51%)
4. **Threshold establishment**: Consensus score becomes clipping threshold for weights

Properties and Interpretation:
- **Range**: [0, 1] normalized values
- **High Consensus**: Values close to 1 indicate strong validator agreement
- **Low Consensus**: Values close to 0 indicate weak validator agreement
- **Outlier Detection**: Weights below consensus score are clipped to 0

Network Security Properties:
- **Anti-Manipulation**: Consensus filtering prevents weight manipulation by outliers
- **Stake-Weighted**: Higher stake validators have more influence in consensus
- **Dynamic Threshold**: Consensus adapts to changing network conditions
- **Majority Rule**: κ parameter controls consensus strictness (typically 51%)

#### Relationship to Other Metrics

**Consensus vs Trust:**
- **Consensus**: Stake-weighted median of weights (consensus threshold)
- **Trust**: Ratio of final rank to pre-rank (consensus alignment impact)
- **Relationship**: Consensus determines weight clipping, Trust measures the impact

**Consensus vs Ranks:**
- **Consensus**: Threshold for weight filtering
- **Ranks**: Final performance scores after consensus filtering
- **Relationship**: Consensus influences rank calculation through weight clipping

**Consensus vs Validator Trust:**
- **Consensus**: Per-neuron consensus thresholds
- **Validator Trust**: Sum of clipped weights set by each validator
- **Relationship**: Validator trust measures validator influence in consensus

**Source**: 
- [`bittensor/bittensor/core/metagraph.py:360-372`](https://github.com/opentensor/bittensor/blob/main/bittensor/core/metagraph.py#L360-372)
- [`subtensor/pallets/subtensor/src/epoch/run_epoch.rs:595`](https://github.com/opentensor/subtensor/blob/main/pallets/subtensor/src/epoch/run_epoch.rs#L595)


## D

### Delegate

A subnet validator that receives staked TAO tokens from delegators and performs validation tasks in one or more subnets.

**See also:** [Delegation](./staking-and-delegation/delegation.md), [Managing Stake with btcli](./staking-and-delegation/managing-stake-btcli.md)

### Delegate Stake

The amount of TAO staked by the delegate themselves.

**See also:** [Managing Stake with btcli](./staking-and-delegation/managing-stake-btcli.md), [Managing Stake with SDK](./staking-and-delegation/managing-stake-sdk.md)



### Delegation

Also known as staking, delegating TAO to a validator (who is thereby the delegate), increases the validator's stake and secure a validator permit.

**See also:** [Delegation](./staking-and-delegation/delegation.md), [Managing Stake with btcli](./staking-and-delegation/managing-stake-btcli.md)

### Dendrite  

A client instance used by subnet validators and subnet miners to transmit information to axons on subnet miners and subnet validators. Dendrites communicate with axons using the server-client (Axon-dendrite) protocol.

**See also:** [Subnet Miners](./miners/), [Subnet Validators](./validators/)

### Deregistration

The process of removing a subnet miner or a subnet validator from the subnet due to poor performance.

**See also:** [Miner Deregistration](./miners/#miner-deregistration), [Subnet Miners](./miners/)

## E 

### EdDSA Cryptographic Keypairs

A cryptographic algorithm used to generate public and private key pairs for coldkeys and hotkeys in the Bittensor wallet.

**See also:** [Working with Keys](./working-with-keys.md), [Coldkey-Hotkey Security](./getting-started/coldkey-hotkey-security.md)

### Effective stake

The total staked TAO amount of a delegate, including their own TAO tokens and those delegated by nominators.

**See also:** [Managing Stake with btcli](./staking-and-delegation/managing-stake-btcli.md), [Managing Stake with SDK](./staking-and-delegation/managing-stake-sdk.md)

### Emission

Every block, currency is injected into each subnet in Bittensor, and every tempo (or 360 blocks), it is extracted by participants (miners, validators, stakers, and subnet creators).

Emission is this process of generating and allocating currency to participants. The amount allocated to a given participant over some duration of time is also often referred to as 'their emissions' for the period.

**See also:** [Emissions](./emissions.md)

### Encrypting the Hotkey

An optional security measure for the hotkey.

**See also:** [Coldkey-Hotkey Security](./getting-started/coldkey-hotkey-security.md), [Working with Keys](./working-with-keys.md)

### External Wallet

A Bittensor wallet created through the Bittensor website or using a tool like [subkey](https://docs.substrate.io/reference/command-line-tools/subkey/), allowing users to use TAO without installing Bittensor.

**See also:** [Wallets](./getting-started/wallets.md), [Installation](./getting-started/installation.md)

## H 

### Hotkey

A component of a Bittensor wallet responsible for less secure operations such as signing messages into the network, secure a UID slot in a subnet, running subnet miners and subnet validators in a subnet. It can be encrypted or unencrypted, but is unencrypted by default. The terms "account" and "hotkey" are used synonymously.

**See also:** [Coldkey-Hotkey Security](./getting-started/coldkey-hotkey-security.md), [Working with Keys](./working-with-keys.md)

### Hotkey-Coldkey Pair

Authentication mechanism for delegates and nominators and for delegates participating in the Senate.

**See also:** [Coldkey-Hotkey Security](./getting-started/coldkey-hotkey-security.md), [Working with Keys](./working-with-keys.md)

## I 

### Immunity Period

A grace period granted to a newly registered subnet miner or subnet validator, during which they will not be deregistered due to performance. Allows a miner or validator new to the subnet to adapt and improve their performance, in order to avoid deregistration once the immunity period expires.

**See also:** [Subnet Miners](./miners/), [Subnet Validators](./validators/)

Code References and Implementation Details

**Immunity Period as Protection Mechanism:**
- Immunity period provides a grace period for new neurons to establish themselves without immediate deregistration risk
  - `subtensor/pallets/subtensor/src/utils/misc.rs:442-448` - `get_neuron_is_immune()` implementation
- Immunity status is calculated dynamically based on registration block and current block
  - `subtensor/pallets/subtensor/src/utils/misc.rs:442-448` - `current_block.saturating_sub(registered_at) < u64::from(immunity_period)`
- Immunity period is configurable per subnet and can be adjusted by subnet owners
  - `subtensor/pallets/subtensor/src/lib.rs:1369-1371` - `pub type ImmunityPeriod<T> = StorageMap<_, Identity, u16, u16, ValueQuery, DefaultImmunityPeriod<T>>;`

**Storage and Configuration:**

**Core Storage Implementation:**
- **ImmunityPeriod Storage**: Maps netuid to immunity period value in blockchain state
  - `subtensor/pallets/subtensor/src/lib.rs:1369-1371` - `pub type ImmunityPeriod<T> = StorageMap<_, Identity, u16, u16, ValueQuery, DefaultImmunityPeriod<T>>;`
- **Default Values**: Network-wide configuration for immunity period
  - `subtensor/pallets/subtensor/src/lib.rs:660-662` - `DefaultImmunityPeriod<T>()` - Default 4096 blocks
  - `subtensor/runtime/src/lib.rs:1077` - `pub const SubtensorInitialImmunityPeriod: u16 = 4096;`
- **BlockAtRegistration Storage**: Tracks registration block for each neuron
  - `subtensor/pallets/subtensor/src/lib.rs:1580-1588` - `pub type BlockAtRegistration<T: Config> = StorageDoubleMap<_, Identity, u16, Identity, u16, u64, ValueQuery, DefaultBlockAtRegistration<T>>;`

**Immunity Status Calculation:**

**Dynamic Immunity Check:**
- **Registration Block Retrieval**: Gets the block number when neuron was registered
  - `subtensor/pallets/subtensor/src/utils/misc.rs:442-448` - `let registered_at = Self::get_neuron_block_at_registration(netuid, uid);`
- **Current Block Retrieval**: Gets the current blockchain block number
  - `subtensor/pallets/subtensor/src/utils/misc.rs:442-448` - `let current_block = Self::get_current_block_as_u64();`
- **Immunity Period Retrieval**: Gets the configured immunity period for the subnet
  - `subtensor/pallets/subtensor/src/utils/misc.rs:442-448` - `let immunity_period = Self::get_immunity_period(netuid);`
- **Immunity Formula**: `is_immune = (current_block - registered_at) < immunity_period`
  - `subtensor/pallets/subtensor/src/utils/misc.rs:442-448` - `current_block.saturating_sub(registered_at) < u64::from(immunity_period)`

**Pruning Algorithm Integration:**

**Pruning Score Calculation:**
- **Score-Based Selection**: Neuron with lowest pruning score is selected for replacement
  - `subtensor/pallets/subtensor/src/subnets/registration.rs:409-485` - `get_neuron_to_prune()` implementation
- **Immunity Priority**: Non-immune neurons are prioritized over immune neurons for pruning
  - `subtensor/pallets/subtensor/src/subnets/registration.rs:439-485` - Immunity status check in pruning algorithm
- **Tie-Breaking**: When scores are equal, earliest registered neuron is pruned
  - `subtensor/pallets/subtensor/src/subnets/registration.rs:440-485` - Registration time tie-breaking

**Pruning Algorithm Logic:**

**Two-Tier Selection Process:**
- **Non-Immune Neurons**: First priority for pruning when available
  - `subtensor/pallets/subtensor/src/subnets/registration.rs:454-465` - Non-immune neuron selection logic
- **Immune Neurons**: Second priority, only pruned when all neurons are immune
  - `subtensor/pallets/subtensor/src/subnets/registration.rs:440-453` - Immune neuron selection logic
- **Owner Protection**: Subnet owner hotkey is protected from pruning regardless of immunity status
  - `subtensor/pallets/subtensor/src/subnets/registration.rs:425-433` - Owner protection check

**Score Comparison Logic:**
- **Lower Score Priority**: Neurons with lower pruning scores are selected first
  - `subtensor/pallets/subtensor/src/subnets/registration.rs:440-485` - Score comparison in pruning algorithm
- **Registration Time Tie-Breaking**: When scores are equal, earlier registration wins
  - `subtensor/pallets/subtensor/src/subnets/registration.rs:440-485` - Registration time comparison
- **UID Tie-Breaking**: When registration times are equal, lower UID wins
  - `subtensor/pallets/subtensor/src/subnets/registration.rs:440-485` - UID-based tie-breaking

**Registration Process Integration:**

**Registration Block Recording:**
- **Block Storage**: Registration block is recorded when neuron is registered
  - `subtensor/pallets/subtensor/src/subnets/registration.rs:214-339` - Registration block storage in `do_registration()`
- **Timestamp Tracking**: Each neuron's registration time is tracked for immunity calculation
  - `subtensor/pallets/subtensor/src/lib.rs:1580-1588` - `BlockAtRegistration` storage definition
- **Dynamic Updates**: Immunity status updates automatically as blocks progress

**Registration Methods:**
- **Proof-of-Work Registration**: Traditional registration with block recording
  - `subtensor/pallets/subtensor/src/subnets/registration.rs:214-339` - `do_registration()` implementation
- **Burned Registration**: Registration by burning TAO with block recording
  - `subtensor/pallets/subtensor/src/subnets/registration.rs:54-206` - `do_burned_registration()` implementation

**Python SDK Integration:**

**Immunity Period Retrieval:**
- **Synchronous Method**: `subtensor.immunity_period()` retrieves immunity period for subnet
  - `bittensor/bittensor/core/subtensor.py:1998-2025` - `immunity_period()` implementation
- **Asynchronous Method**: `async_subtensor.immunity_period()` for async operations
  - `bittensor/bittensor/core/async_subtensor.py:2931-2970` - Async `immunity_period()` implementation
- **Block-Specific Queries**: Immunity period can be queried at specific block numbers
  - `bittensor/bittensor/core/subtensor.py:1998-2025` - Block parameter support

**Testing and Validation:**

**Comprehensive Test Coverage:**
- **Immunity Status Testing**: Tests verify correct immunity calculation
  - `subtensor/pallets/subtensor/src/tests/registration.rs:621-675` - Immunity status validation tests
- **Pruning Algorithm Testing**: Tests verify immunity-aware pruning
  - `subtensor/pallets/subtensor/src/tests/registration.rs:583-701` - Pruning algorithm tests
- **Edge Case Testing**: Tests verify behavior when all neurons are immune
  - `subtensor/pallets/subtensor/src/tests/registration.rs:1261-1311` - All-immune scenarios

**Test Scenarios:**
- **Mixed Immunity**: Tests with both immune and non-immune neurons
  - `subtensor/pallets/subtensor/src/tests/registration.rs:583-701` - Mixed immunity test scenarios
- **All Immune**: Tests when all neurons are in immunity period
  - `subtensor/pallets/subtensor/src/tests/registration.rs:1261-1311` - All-immune test scenarios
- **Tie-Breaking**: Tests for score and registration time tie-breaking
  - `subtensor/pallets/subtensor/src/tests/registration.rs:583-701` - Tie-breaking validation

**Network Configuration:**

**Default Network Parameters:**
- **SubtensorInitialImmunityPeriod**: 4096 blocks (default for mainnet)
  - `subtensor/runtime/src/lib.rs:1077` - Default immunity period value
- **Test Immunity Period**: 2 blocks (for testing environments)
  - `subtensor/pallets/subtensor/src/tests/mock.rs:161` - Test immunity period value
- **Subnet-Specific**: Each subnet can have different immunity periods
  - `subtensor/pallets/subtensor/src/lib.rs:1369-1371` - Per-subnet immunity period storage

**Configuration Management:**
- **Subnet Owner Control**: Subnet owners can adjust immunity period
  - `subtensor/pallets/subtensor/src/utils/misc.rs:442-448` - Immunity period management functions
- **Dynamic Adjustment**: Immunity period can be changed during subnet operation
  - `subtensor/pallets/subtensor/src/utils/misc.rs:442-448` - `set_immunity_period()` function
- **Event Emission**: Immunity period changes emit blockchain events
  - `subtensor/pallets/subtensor/src/utils/misc.rs:442-448` - Event emission for immunity changes

**Key Mathematical Insights:**
1. **Immunity Formula**: `is_immune = (current_block - registered_at) < immunity_period`
2. **Block Duration**: Each block is 12 seconds, so 4096 blocks = ~13.7 hours
3. **Dynamic Status**: Immunity status updates every block automatically
4. **Pruning Priority**: Non-immune neurons are pruned before immune neurons
5. **Owner Protection**: Subnet owners are protected regardless of immunity status

**Network Security Properties:**
- **Grace Period**: New neurons have time to establish performance
- **Performance Pressure**: Immunity eventually expires, creating performance incentives
- **Owner Stability**: Subnet owners are protected from immediate pruning
- **Dynamic Adjustment**: Immunity periods can be tuned per subnet needs
- **Fair Competition**: Immunity prevents immediate replacement of new participants

**Complete Immunity Period Flow:**
1. **Registration** → Neuron registers and registration block is recorded
2. **Immunity Calculation** → System calculates immunity status every block
3. **Performance Building** → Neuron has immunity_period blocks to improve performance
4. **Immunity Expiration** → Neuron becomes eligible for pruning after immunity expires
5. **Pruning Evaluation** → Non-immune neurons are prioritized for pruning
6. **Owner Protection** → Subnet owners are protected regardless of immunity status
7. **Dynamic Updates** → Immunity status updates automatically with each block

**Immunity Period vs Other Protection Mechanisms:**
- **Immunity Period**: Temporary protection for new neurons (4096 blocks)
- **Owner Protection**: Permanent protection for subnet owners
- **Validator Permits**: Performance-based validation rights
- **Stake Requirements**: Economic barriers to participation
- **Rate Limiting**: Transaction frequency restrictions

**Economic Implications:**
- **Performance Incentives**: Immunity creates pressure to improve performance
- **Network Stability**: Prevents rapid turnover of new participants
- **Owner Commitment**: Protects subnet owners from immediate replacement
- **Competition Balance**: Balances protection with performance requirements
- **Dynamic Governance**: Allows subnet-specific immunity tuning

**Python SDK Usage:**

**Getting Immunity Period:**
```python
import bittensor as bt

# Initialize subtensor connection
subtensor = bt.subtensor()

# Get immunity period for a subnet
immunity_period = subtensor.immunity_period(netuid=1)
print(f"Immunity period: {immunity_period} blocks")  # e.g., "Immunity period: 4096 blocks"

# Get immunity period at specific block
immunity_period_at_block = subtensor.immunity_period(netuid=1, block=1000000)
print(f"Immunity period at block 1000000: {immunity_period_at_block}")
```

**Async Usage:**
```python
async def get_immunity_period():
    async with bt.subtensor() as subtensor:
        immunity_period = await subtensor.immunity_period(netuid=1)
        return immunity_period

# Usage
immunity_period = await get_immunity_period()
print(f"Immunity period: {immunity_period} blocks")
```

**Error Handling:**
- **Subnet Not Found**: Returns `None` if subnet doesn't exist
  - `bittensor/bittensor/core/subtensor.py:1998-2025` - Error handling in immunity_period()
- **Block Not Found**: Returns `None` if specified block doesn't exist
  - `bittensor/bittensor/core/subtensor.py:1998-2025` - Block validation
- **Network Issues**: Handles connection and RPC errors gracefully
  - `bittensor/bittensor/core/subtensor.py:1998-2025` - Network error handling

**Testing Examples:**
- **E2E Tests**: `bittensor/tests/e2e_tests/test_root_set_weights.py:63-115` - Immunity period testing
- **Unit Tests**: `bittensor/tests/unit_tests/test_subtensor_extended.py` - SDK method testing
- **Async Tests**: `bittensor/tests/unit_tests/test_async_subtensor.py` - Async method testing

**Immunity Period Calculation Examples:**
- **Block 1000 Registration**: Immunity until block 5096 (1000 + 4096)
- **Block 5000 Registration**: Immunity until block 9096 (5000 + 4096)
- **Current Block 8000**: Neuron registered at block 3000 is no longer immune
- **Current Block 6000**: Neuron registered at block 2000 is no longer immune

**Network Configuration Examples:**
- **Subnet 1**: 7200 blocks immunity period (24 hours)
- **Default Subnets**: 4096 blocks immunity period (~13.7 hours)
- **Test Networks**: 2 blocks immunity period (24 seconds)
- **Custom Subnets**: Configurable immunity periods based on subnet needs

### Incentives

A portion of the TAO emission received by the subnet miners when they provide valuable services and compete for UID slots in a subnet.

**See also:** [Emissions](./emissions.md), [Anatomy of Incentive Mechanism](./learn/anatomy-of-incentive-mechanism.md)

### Incentive Mechanism

A system that drives the behavior of subnet miners and governs consensus among subnet validators in a Bittensor subnet. Each subnet has its own incentive mechanism, which should be designed carefully to promote desired behaviors and penalize undesired ones.

**See also:** [Anatomy of Incentive Mechanism](./learn/anatomy-of-incentive-mechanism.md), [Understanding Subnets](./subnets/understanding-subnets.md)

## L 

### Lite Node

A type of public subtensor node that stores limited blockchain data and relies on archive nodes for full historical data.

**See also:** [Subtensor Nodes](./subtensor-nodes/), [Managing Subtensor Connections](./sdk/managing-subtensor-connections.md)

### Local Blockchain

A private blockchain used for developing and testing subnet incentive mechanisms. A local blockchain is not public and is isolated from any Bittensor network.

**See also:** [Local Build](./local-build/deploy), [Create a Subnet](./local-build/create-subnet.md)

### Local Wallet

A Bittensor wallet created on the user's machine, requiring the installation of Bittensor.

**See also:** [Wallets](./getting-started/wallets.md), [Installation](./getting-started/installation.md)

### Loss Function

In the context of machine learning, a mathematical function that measures the difference between the predicted output and the ground truth. In Bittensor, incentive mechanisms act as loss functions that steer subnet miners towards desirable outcomes.

**See also:** [Anatomy of Incentive Mechanism](./learn/anatomy-of-incentive-mechanism.md), [Understanding Subnets](./subnets/understanding-subnets.md)

## M 

### Mainchain

The primary Bittensor blockchain network, used for production purposes and connected to lite or archive nodes.

**See also:** [Bittensor Networks](./bittensor-networks.md), [Subtensor Nodes](./subtensor-nodes/)

### Metagraph

A data structure that contains comprehensive information about the current state of a subnet, including detailed information on all the nodes (neurons) such as subnet validator stakes and subnet weights in the subnet. Metagraph aids in calculating emissions.

**See also:** [Subtensor API](./sdk/subtensor-api.md), [Understanding Subnets](./subnets/understanding-subnets.md)

### Miner Deregistration

The process of removing a poor-performing subnet miner from a UID slot, making room for a newly registered miner.

**See also:** [Miner Deregistration](./miners/#miner-deregistration)

### Mnemonic

A sequence of words used to regenerate keys, in case of loss, and restore coldkeys and hotkeys in the Bittensor wallet.

**See also:** [Handle Seed Phrase](./keys/handle-seed-phrase.md), [Working with Keys](./working-with-keys.md)

## N 

### NaCl Format

A secure encryption format, using the [NaCl](https://nacl.cr.yp.to/) library, used for updating legacy Bittensor wallets to improve security.

**See also:** [Working with Keys](./working-with-keys.md), [Coldkey-Hotkey Security](./getting-started/coldkey-hotkey-security.md)

### Netuid

A unique identifier assigned to a subnet within the Bittensor network.

**See also:** [Understanding Subnets](./subnets/understanding-subnets.md), [Working with Subnets](./subnets/working-with-subnets.md)

### Neuron

The basic computing node in a Bittensor subnet, representing a node in a neural network. Neurons can be either subnet validators or subnet miners, each identified by a unique UID within their subnet and associated with a hotkey-coldkey pair for authentication and operations.

Neurons participate in the network through axon servers (miners) and dendrite clients (validators), exchanging synapse objects to perform subnet-specific tasks. Their performance is measured through metrics like rank, trust, consensus, and incentive scores, which determine emissions and validator permits.

**See also:** [Understanding Neurons](./learn/neurons.md), [Subnet Validators](./validators/), [Subnet Miners](./miners/), [NeuronInfo class](pathname:///python-api/html/autoapi/bittensor/core/chain_data/neuron_info/index.html)


## N 

### Nominate

The process of a delegate registering themselves as a candidate for others to stake their $TAO to.

### Nominator

Another term for a delegator. A subnet validator who nominates their own hotkey as a delegate, allowing others to delegate their TAO to the nominator's hotkey.

### Nominator (Delegator)

A TAO holder who delegates their stake.

## O 

### Objective Function

In the context of machine learning and subnet operations, this refers to the goal that the subnet is continuously optimizing for, through its incentive mechanism.

**See also:** [Anatomy of Incentive Mechanism](./learn/anatomy-of-incentive-mechanism.md), [Understanding Subnets](./subnets/understanding-subnets.md)

## P 

### Private Key

A private component of the cryptographic key pair, crucial for securing and authorizing transactions and operations within the Bittensor network.

**See also:** [Working with Keys](./working-with-keys.md), [Coldkey-Hotkey Security](./getting-started/coldkey-hotkey-security.md)

### Proposal

A suggestion or plan put forward by the Triumvirate for the Senate to vote on.

**See also:** [Governance](./governance.md), [Senate](./senate.md)

### Proposal hash

A unique identifier for a proposal used in the voting process.

**See also:** [Governance](./governance.md), [Senate](./senate.md)

### Public Key

A cryptographic key that is publicly available and used for verifying signatures, encrypting messages, and identifying accounts in the Bittensor network. This is the publicly shareable part of the cryptographic key pair associated with both the coldkey and hotkey, allowing others to securely interact with the wallet.

**See also:** [Working with Keys](./working-with-keys.md), [Coldkey-Hotkey Security](./getting-started/coldkey-hotkey-security.md)

### Public Subtensor

A publicly accessible node in the Bittensor network that can be run as a lite node or an archive node and synchronized with either the mainchain or testchain.

**See also:** [Subtensor Nodes](./subtensor-nodes/), [Managing Subtensor Connections](./sdk/managing-subtensor-connections.md)

## R 

### RAO

A denomination of TAO, representing one billionth (10<sup>-9</sup>) of a TAO.

**See also:** [Emissions](./emissions.md)

### Rank

This metagraph property represents the final aggregate judgment of a each miner, computed by Yuma Consensus alogirithm operating over the miner-ratings submitted by a subnet's validators each tempo. The final `rank` score represent a miner's performance after any outlier weights set by validators have been removed through consensus clipping. This ensures that only weights near the median consensus are used in final calculations.

Ranks are calculated as the stake-weighted sum of consensus-clipped weights and directly determine emissions to miners.


**See also:** [Emissions](./emissions.md), [Yuma Consensus](./yuma-consensus.md), [Subnet Metagraph](./subnets/metagraph.md)

**Relationship to Other Metrics:**
- **Ranks vs Consensus**: Ranks are calculated using consensus-clipped weights
- **Ranks vs Trust**: Trust measures how much consensus clipping affected the rank
- **Ranks vs Incentive**: Ranks are normalized to become incentive values
- **Ranks vs Validator Trust**: Validator trust measures validator influence in consensus

**Calculation Process:**
1. **Pre-ranks**: Initial stake-weighted sum of all weights before consensus filtering
2. **Consensus calculation**: Stake-weighted median of weights per neuron (consensus threshold)
3. **Weight clipping**: Weights clipped at consensus threshold to remove outliers
4. **Final ranks**: Stake-weighted sum of clipped weights (the rank value)

**Properties and Interpretation:**
- **Range**: [0, 1] normalized values after final normalization
- **High Rank**: Values close to 1 indicate strong consensus-based performance
- **Low Rank**: Values close to 0 indicate weak consensus-based performance
- **Incentive Distribution**: Ranks directly determine incentive allocation to miner neurons

**Network Security Properties:**
- **Consensus-Based**: Ranks reflect network consensus rather than individual validator opinions
- **Outlier Protection**: Consensus clipping prevents manipulation by outlier weights
- **Stake-Weighted**: Higher stake validators have more influence in rank calculation
- **Dynamic Updates**: Ranks are recalculated every epoch based on current network state

**Mathematical Definition:**
For each neuron $j$, the rank $R_j$ is calculated as:
$$R_j = \sum_{i \in \text{validators}} S_i \cdot \overline{W_{ij}}$$

Where:
- $S_i$ is the stake of validator $i$
- $\overline{W_{ij}}$ is the consensus-clipped weight from validator $i$ to neuron $j$
- The sum is taken over all validators in the subnet

**Source**: 
- [`bittensor/bittensor/core/metagraph.py:325-331`](https://github.com/opentensor/bittensor/blob/main/bittensor/core/metagraph.py#L325-331)
- [`subtensor/pallets/subtensor/src/epoch/run_epoch.rs:605`](https://github.com/opentensor/subtensor/blob/main/pallets/subtensor/src/epoch/run_epoch.rs#L605)


### Recycling, burning, and locking

"Recycling TAO" means that this TAO is put back into the Bittensor emissions system. Instead of minting new TAO this recycled TAO that is in the recycle bin will be used again in the new emissions.

This happens in two cases:

- When you register either as a subnet validator or a subnet miner and get a `UID` in return, the registration cost TAO you pay is recycled. 
- Emissions are recycled for those subnets that have registration turned off or paused.

When TAO is burned it is permanently removed from circulation, reducing total supply.

Locked TAO is neither recycled nor burned, but held unspent, without the ability to move it until it is unlocked. The cost for subnet registration is locked and returned if the subnet is deregistered.

**See also:** [Emissions](./emissions.md), [Subnet Miners](./miners/), [Subnet Validators](./validators/)

### Regenerating a Key

The process of recreating a lost or deleted coldkey or hotkey using the associated mnemonic.

**See also:** [Handle Seed Phrase](./keys/handle-seed-phrase.md), [Working with Keys](./working-with-keys.md)

### Register

The process of registering keys with a subnet and purchasing a UID slot.

**See also:** [Subnet Miners](./miners/), [Subnet Validators](./validators/), [Working with Subnets](./subnets/working-with-subnets.md)

## S 

### SS58 Encoded

A compact representation of public keys corresponding to the wallet's coldkey and hotkey, used as wallet addresses for secure TAO transfers.

**See also:** [Working with Keys](./working-with-keys.md), [Wallets](./getting-started/wallets.md)

### Senate

A group of elected delegates formed from the top K delegate hotkeys, responsible for approving or disapproving proposals made by the Triumvirate.

**See also:** [Senate](./senate.md), [Governance](./governance.md)

### Stake

The amount of currency tokens delegated to a validator UID in a subnet. Includes both self-stake (from the validator's own cold-key) and stake delegated from others. 

Stake determines a validator's weight in consensus as well as their emissions.

**See also:** [Managing Stake with btcli](./staking-and-delegation/managing-stake-btcli.md), [Managing Stake with SDK](./staking-and-delegation/managing-stake-sdk.md), [Delegation](./staking-and-delegation/delegation.md)



### Stake Weight

The computed total stake value for a validator that determines their consensus power and emissions in a subnet. Stake weight combines a validator's alpha stake and TAO stake using the TAO weight parameter to calculate their total influence in the network.

**See also:** [TAO Weight](#tao-weight), [Understanding Subnets](./subnets/understanding-subnets.md)


**Mathematical Definition:**
For a validator with alpha stake $\alpha$ and TAO stake $\tau$, the stake weight $W$ is calculated as:
$$
W = {\alpha + \tau \ \times w_{\tau}}
$$

Where $w_{\tau}$ is the global TAO weight parameter (currently 0.18)

A validator's relative influence in a subnet is calculated as:
$$
\text{Relative Stake Weight} = \frac{\text{Stake Weight}_i}{\sum_{v \in \text{validators}} \text{Stake Weight}_v}
$$

**Consensus Power:**
- **Weight Setting**: Higher stake weight means more influence when setting weights
- **Validator Permits**: Stake weight determines eligibility for validator permits
- **Bond Formation**: Stake weight influences bond calculations and retention

**Validator Emissions:**
- **Relative Distribution**: Higher stake weight -> higher emission share

**Code References:**

- **Yuma Consensus**: [`subtensor/pallets/subtensor/src/epoch/run_epoch.rs:530`](https://github.com/opentensor/subtensor/blob/main/pallets/subtensor/src/epoch/run_epoch.rs#L530)
- **Validator dividend distribution**: [`subtensor/pallets/subtensor/src/coinbase/run_coinbase.rs:165`](https://github.com/opentensor/subtensor/blob/main/pallets/subtensor/src/coinbase/run_coinbase.rs#L165)


### Staking

The process of attaching TAO to a hotkey, i.e., locking TAO to a hotkey, to participate as a subnet validator, and to secure a validator permit.

**See also:** [Managing Stake with btcli](./staking-and-delegation/managing-stake-btcli.md), [Managing Stake with SDK](./staking-and-delegation/managing-stake-sdk.md), [Delegation](./staking-and-delegation/delegation.md)

### Subnet

A Bittensor subnet is an incentive-based competition market that produces a specific kind of digital commodity. It consists of a community of miners that produce the commodity, and a community of validators that measures the miners' work to ensure its quality.

**See also:** [Understanding Subnets](./subnets/understanding-subnets.md), [Working with Subnets](./subnets/working-with-subnets.md), [Create a Subnet](./subnets/create-a-subnet.md)

### Subnet Incentive Mechanism

The framework that governs the behavior of subnet miners and ensures consensus among subnet validators by promoting desirable actions and penalizing undesired ones.

**See also:** [Anatomy of Incentive Mechanism](./learn/anatomy-of-incentive-mechanism.md), [Understanding Subnets](./subnets/understanding-subnets.md)

### Subnet Miner

The task-performing entity within a Bittensor subnet. A subnet miner is a type of node in a Bittensor subnet that is connected only to subnet validators. Subnet miners are isolated from the external world and communicate bidirectionally with subnet validators. A subnet miner is responsible for performing tasks given to them by the subnet validators in that subnet. 

**See also:** [Subnet Miner Documentation](./miners/)

### Subnet Creator

The individual or entity responsible for defining the specific digital task to be performed by subnet miners, implementing an incentive mechanism, and providing sufficient documentation for participation in the subnet.

**See also:** [Create a Subnet](./subnets/create-a-subnet.md), [Subnet Creators btcli Guide](./subnets/subnet-creators-btcli-guide.md)

### Subnet Protocol

A unique set of rules defining interactions between subnet validators and miners, including how tasks are queried and responses are provided.

**See also:** [Understanding Subnets](./subnets/understanding-subnets.md), [Working with Subnets](./subnets/working-with-subnets.md)

### Subnet scoring model

A component of the incentive mechanism that defines how subnet miners' responses are evaluated, aiming to align subnet miner behavior with the subnet's goals and user preferences. It is a mathematical object that converts miner responses into numerical scores, enabling continuous improvement and competition among miners.

**See also:** [Anatomy of Incentive Mechanism](./learn/anatomy-of-incentive-mechanism.md), [Understanding Subnets](./subnets/understanding-subnets.md)

### Subnet Task

A key component of any incentive mechanism that defines the work the subnet miners will perform. The task should be chosen to maximize subnet miner effectiveness at the intended use case for the subnet.

**See also:** [Understanding Subnets](./subnets/understanding-subnets.md), [Anatomy of Incentive Mechanism](./learn/anatomy-of-incentive-mechanism.md)

### Subnet Weights

The importance assigned to each subnet determined by relative price among subnets and used to determine the percentage emissions to subnets.

**See also:** [Emissions](./emissions.md), [Consensus-Based Weights](./subnets/consensus-based-weights.md)

### Subtensor

[Subtensor](https://github.com/opentensor/subtensor) is Bittensor's layer 1 blockchain based on substrate (now PolkadotSDK). This serves Bittensor as a system of record for transactions and rankings, operates Yuma Consensus, and emits liquidity to participants to incentivize their participation in network activities.

The Bittensor SDK offers the [`bittensor.core.subtensor`](pathname:///python-api/html/autoapi/bittensor/core/subtensor/index.html) and [`bittensor.core.async_subtensor`](pathname:///python-api/html/autoapi/bittensor/core/async_subtensor/index.html) modules to handle Subtensor blockchain interactions.

**See also:** [Subtensor API](./sdk/subtensor-api.md), [Subtensor Nodes](./subtensor-nodes/), [Managing Subtensor Connections](./sdk/managing-subtensor-connections.md)

### Sudo

A privileged key for administrative actions, replaced by governance protocol for enhanced security.

**See also:** [Governance](./governance.md), [btcli Permissions](./btcli-permissions.md)

### Synapse

A data object used by subnet validators and subnet miners as the main vehicle to exchange information. Synapse objects are based on the BaseModel of the Pydantic data validation library.

**See also:** [Subnet Miners](./miners/), [Subnet Validators](./validators/)

## T 

### TAO ($\tau$)

The cryptocurrency of the Bittensor network, used to incentivize participation in network activities (mining, validation, subnet creation and management). A single TAO is newly created (i.e., minted) every 12 seconds on the Bittensor blockchain.

**See also:** [Emissions](./emissions.md), [Wallets](./getting-started/wallets.md)

### TAO Weight

A global parameter (currently set to 0.18) that determines the relative influence of TAO stake versus alpha stake when calculating a validator's total stake weight, a critical value that influence's a validator's consensus power and emissions.

**See also:** [Stake Weight](#stake-weight)
### Tempo

A 360-block period during which the Yuma Consensus calculates emissions to subnet participants based on the latest available ranking weight matrix. A single block is processed every 12 seconds, hence a 360-block tempo occurs every 4320 seconds or 72 minutes. 

**See also:** [Yuma Consensus](./yuma-consensus.md), [Emissions](./emissions.md)

### Transfer

The process of sending TAO tokens from one wallet address to another in the Bittensor network.

**See also:** [Wallets](./getting-started/wallets.md), [Working with Keys](./working-with-keys.md)

### Triumvirate

A group of three Opentensor Foundation employees responsible for creating proposals.

**See also:** [Governance](./governance.md), [Senate](./senate.md)

### Trust

In the Yuma Consensus algorithm, trust represents how much a miner's rank was affected by consensus clipping. Trust is calculated as the ratio of final rank to pre-rank. It represents how much of the original validator support survived the consensus clipping process, providing insight into whether a neuron received controversial or outlier weight assignments.

**See also:** [Yuma Consensus](./yuma-consensus.md), [Subnet Metagraph](./subnets/metagraph.md)


**Mathematical Definition:**
For each neuron $j$, the trust $T_j$ is calculated as:
$$
T_j = \frac{R_j}{P_j}
$$

Where:
- $R_j$ is the final rank after consensus clipping
- $P_j$ is the pre-rank before consensus clipping
- The ratio indicates the proportion of original support that survived consensus filtering

Interpretation:
- **Range**: [0, 1] where 1.0 indicates perfect consensus alignment
- **`Trust = 1.0`**: Neuron's rank unchanged by consensus (high consensus alignment)
- **`Trust < 1.0`**: Neuron's rank reduced by consensus clipping (lower value means more reduction)
- **`Trust = 0.0`**: Neuron's rank eliminated by consensus (no consensus support)

Calculation Process:
1. **Pre-ranks calculation**: $P_j = \sum_{i} S_i \cdot W_{ij}$ (stake-weighted sum of all weights)
2. **Consensus filtering**: Weights clipped at consensus threshold to remove outliers
3. **Final ranks calculation**: $R_j = \sum_{i} S_i \cdot \overline{W_{ij}}$ (stake-weighted sum of clipped weights)
4. **Trust calculation**: $T_j = R_j / P_j$ (ratio of final to pre-rank)

**Relationship to Other Metrics:**
- **Trust vs Consensus**: Trust measures the impact of consensus filtering
- **Trust vs Ranks**: Trust is the ratio of final rank to pre-rank
- **Trust vs Validator Trust**: Trust is per-neuron, Validator Trust is per-validator
- **Trust vs Incentive**: Trust influences incentive through consensus mechanisms

**Metric Comparison Table**

| Metric | Purpose | Calculation | Range | Interpretation |
|--------|---------|-------------|-------|----------------|
| **Consensus** | Consensus threshold | Stake-weighted median of weights per neuron | [0, 1] | Higher = stronger validator agreement |
| **Ranks** | Performance scoring | Stake-weighted sum of clipped weights | [0, 1] | Higher = better performance after consensus |
| **Trust** | Consensus alignment | Final rank / Pre-rank | [0, 1] | 1.0 = no clipping, < 1.0 = some clipping |
| **Validator Trust** | Validator influence | Sum of clipped weights per validator | [0, 1] | Higher = more consensus-aligned validator |

**Source**: 
- [`bittensor/bittensor/core/metagraph.py:380-393`](https://github.com/opentensor/bittensor/blob/main/bittensor/core/metagraph.py#L380-393)
- [`subtensor/pallets/subtensor/src/epoch/run_epoch.rs:608`](https://github.com/opentensor/subtensor/blob/main/pallets/subtensor/src/epoch/run_epoch.rs#L608)





The relationship between these metrics creates a feedback loop: consensus determines weight clipping, which affects ranks and trust, which influences validator trust, which feeds back into future consensus calculations. This system ensures that the network rewards neurons with strong validator agreement while penalizing those with controversial or outlier weight assignments, creating a robust mechanism for maintaining network quality and security.



## U 

### UID Slot

A position occupied by a subnet miner or subnet validator within a subnet, identified by a unique UID. The UID is assigned to a hotkey when it is registered in a subnet, allowing the hotkey to participate as a subnet validator or subnet miner.

**See also:** [Subnet Miners](./miners/), [Subnet Validators](./validators/), [Working with Subnets](./subnets/working-with-subnets.md)

## V 

### Validator Permit

A boolean flag indicating whether a specific neuron has validation rights within a subnet. Validator permits are awarded to the top K neurons by stake weight and are required for setting weights and participating in consensus.

**See also:** [VPermit](#vpermit), [Validator Requirements](./validators/index.md#requirements-for-validation), [Stake Weight](#stake-weight)

### VPermit

A list of subnet IDs (netuids) indicating which subnets a delegate is authorized to validate on. VPermits are delegate-level permissions that aggregate individual validator permits across multiple subnets, allowing delegates to participate in validation activities on specific subnets.

**See also:** [Validator Permits](#validator-permit), [Delegation](./staking-and-delegation/delegation.md), [Validator Requirements](./validators/index.md#requirements-for-validation)


### Validator

A type of node in a subnet that creates tasks, evaluates the performance of subnet miners and sets weights based on their output. A subnet validator is connected only to subnet miners and to the external world. Subnet validators receive inputs from the external world and communicate bidirectionally with subnet miners. 

**See also:** [Subnet Validators](./validators/), [Validators btcli Guide](./validators/validators-btcli-guide.md)

### Validator Trust

A specialized trust metric for validator neurons that measures their influence in the consensus process. Validator trust is calculated as the sum of all clipped weights set by each validator across all neurons, indicating how much weight a validator successfully contributed to consensus.

**See also:** [Yuma Consensus](./yuma-consensus.md), [Subnet Metagraph](./subnets/metagraph.md), [Validator-Miner Bonds](#validator-miner-bonds)

**Basic Concept:**
Validator trust specifically measures validator neurons' influence in the consensus process. It represents how much weight each validator successfully contributed to the consensus after weight clipping, providing insight into validator alignment with network consensus.

**Mathematical Definition:**
For each validator $i$, the validator trust $T_{vi}$ is calculated as:
$$T_{vi} = \sum_{j \in \text{neurons}} \overline{W_{ij}}$$

Where:
- $\overline{W_{ij}}$ is the consensus-clipped weight from validator $i$ to neuron $j$
- The sum is taken over all neurons in the subnet
- Validator trust measures the total influence a validator has in consensus

**Calculation Process:**
1. **Weight setting**: Validators set weights to all neurons in the subnet
2. **Consensus calculation**: Stake-weighted median of weights per neuron (consensus threshold)
3. **Weight clipping**: Weights clipped at consensus threshold to remove outliers
4. **Validator trust calculation**: Sum of all clipped weights set by each validator

**Properties and Interpretation:**
- **Range**: [0, 1] normalized values
- **High Validator Trust**: Values close to 1 indicate strong consensus alignment
- **Low Validator Trust**: Values close to 0 indicate outlier weight assignments
- **Validator Influence**: Higher validator trust means more influence in consensus decisions

**Network Security Properties:**
- **Consensus Alignment**: Validator trust measures how well validators align with consensus
- **Outlier Detection**: Low validator trust indicates potential manipulation attempts
- **Validator Quality**: High validator trust indicates quality validation services
- **Economic Incentives**: Validator trust influences validator rewards and bond retention

**Source**: 
- [`bittensor/bittensor/core/metagraph.py:397-409`](https://github.com/opentensor/bittensor/blob/main/bittensor/core/metagraph.py#L397-409)
- [`subtensor/pallets/subtensor/src/epoch/run_epoch.rs:600`](https://github.com/opentensor/subtensor/blob/main/pallets/subtensor/src/epoch/run_epoch.rs#L600)

**Relationship to Other Metrics:**
- **Validator Trust vs Trust**: Validator trust is per-validator, Trust is per-neuron
- **Validator Trust vs Consensus**: Validator trust measures validator influence in consensus
- **Validator Trust vs Ranks**: Validator trust influences rank calculation through consensus
- **Validator Trust vs Bonds**: Validator trust affects bond retention and validator permits


### Validator-Miner Bonds

A mechanism in the Bittensor network that represents the investment relationship between validators and miners, used to calculate validator emissions and incentivize consistent, honest evaluation of miner performance.

**Core Concept:**
Bonds represent the "investment" a validator has made in evaluating a specific miner. This bonding mechanism is integral to the network's market-based approach to measuring and rewarding machine intelligence through the Yuma Consensus algorithm.

**Bond Formation Process:**

**1. Instant Bond Calculation:**
The instant bond $\Delta B_{ij}$ of validator $i$ to miner $j$ is calculated as:
$$\Delta B_{ij} = \frac{S_i \cdot \widetilde{W_{ij}}}{\sum_{k \in \mathbb{V}} S_k \cdot \widetilde{W_{kj}}}$$

Where:
- $S_i$ is validator $i$'s stake
- $\widetilde{W_{ij}}$ is the bond-weight (penalty-adjusted weight)
- The denominator normalizes by the total bond-weight for miner $j$ across all validators

**2. Bond-Weight Calculation:**
Bond-weights are penalized when validators overstate miner performance:
$$\widetilde{W_{ij}} = (1-\beta)W_{ij} + \beta\overline{W_{ij}}$$

Where:
- $W_{ij}$ is the original weight set by validator $i$ for miner $j$
- $\overline{W_{ij}}$ is the consensus-clipped weight
- $\beta$ is the bonds penalty factor (configurable hyperparameter)

**3. Exponential Moving Average (EMA) Bonds:**
Instant bonds are smoothed over time using EMA to prevent abrupt changes:
$$B_{ij}^{(t)} = \alpha \Delta B_{ij} + (1-\alpha)B_{ij}^{(t-1)}$$

Where $\alpha$ is the EMA smoothing factor (typically around 10%).

**Bond Mechanics and Incentives:**

**Consensus Alignment:**
- Validators who stay near consensus build stronger EMA bonds
- Bonds are penalized when validators overstate miner performance
- The EMA smooths out abrupt swings in validator behavior
- Bonds incentivize consistent alignment with consensus

**Validator Emissions:**
Each validator's share of validator emissions (41% of subnet emissions) is calculated as:
$$V_i = \sum_{j \in \mathbb{M}} (B_{ij} \times M_j)$$

Where $M_j$ is miner $j$'s share of miner emissions.

**Bond Management:**

**Bond Retention:**
- Neurons retain bonds only if they keep validator permits
- Bonds are cleared when neurons lose validator permits
- Bonds are stored as sparse matrices in blockchain state

**Bond Decay:**
- Bonds decay over time based on the `bonds_moving_avg` parameter
- Higher decay rates make bonds more responsive to recent performance
- Lower decay rates allow bonds to persist longer

**Network Security Properties:**

**Anti-Manipulation:**
- Bonds prevent weight manipulation through economic penalties
- Validators must "put skin in the game" to influence consensus
- Bond penalties discourage collusive over-evaluation of miners

**Economic Alignment:**
- Bonds create long-term relationships between validators and miners
- Validators are incentivized to discover and support promising miners early
- Bond strength reflects validator confidence in miner performance

**Dynamic Adjustment:**
- Bonds adapt to changing network conditions and consensus
- EMA smoothing prevents exploitation of rapid bond changes
- Bonds provide stability while allowing for network evolution

**Retrieval:**
- Bonds can be queried via the `bonds()` method in the Subtensor API
- Metagraph includes bonds matrix accessible via `metagraph.B` property
- Bonds are included in neuron information structures

**Related hyperparameters:**
- `bonds_penalty`: Controls penalty for out-of-consensus weights (0-65535)
- `bonds_moving_avg`: Controls bond decay rate (typically 900,000)
- `liquid_alpha_enabled`: Enables dynamic alpha adjustment for bonds

**Relationship to Other Network Components:**

**Trust and Consensus:**
- Bonds influence trust calculation through consensus mechanisms
- High bond values indicate strong validator-miner relationships
- Trust creates feedback loop: high trust → better consensus → higher bonds

**Validator Permits:**
- Bonds are retained only by neurons with validator permits
- Loss of validator permit clears all bonds for that neuron
- Bonds align with permit retention for economic security

**Emission Distribution:**
- Bonds directly determine validator emission shares
- Strong bonds lead to higher validator rewards
- Bonds create market-based incentive alignment

**Code References:**
- `pallets/subtensor/src/epoch/run_epoch.rs:631` - Bond calculation in epoch execution
- `pallets/subtensor/src/epoch/math.rs:1475` - EMA bond computation
- `bittensor/core/async_subtensor.py:931` - Bonds API method
- `pallets/subtensor/src/lib.rs:1560` - Bonds storage definition

**See also:** [Yuma Consensus](./yuma-consensus), [Emissions](./emissions), [Trust](#trust), [Validator Permits](#vpermit)


### Validator Take %

The percentage of emissions a validator takes, of the portion that depends on delegated stake (not including their emissions in proportion to their own self-stake), before the remainder is extracted back to the stakers.

Effectively, this represents the fee percentage that validators charge delegators for validation services.

**See also:** [Emissions](./emissions.md)


## W 

### Wallet Address

A unique identifier derived from the public key, used as a destination for sending and receiving TAO tokens in the Bittensor network.

**See also:** [Wallets](./getting-started/wallets.md), [Working with Keys](./working-with-keys.md)

### Wallet Location

The directory path where the generated Bittensor wallets are stored locally on the user's machine.

**See also:** [Wallets](./getting-started/wallets.md), [Installation](./getting-started/installation.md)

### Weight Matrix

A matrix formed from the ranking weight vectors of all subnet validators in a subnet, used as input for the Yuma Consensus module to calculate emissions to that subnet.

**See also:** [Yuma Consensus](./yuma-consensus.md), [Consensus-Based Weights](./subnets/consensus-based-weights.md)

### Weight Vector

A vector maintained by each subnet validator, with each element representing the weight assigned to a subnet miner based on its performance.

The ranking weight vectors for each subnet are transmitted to the blockchain, where they combine to form the [weight matrix](#weight-matrix) that is input for Yuma Consensus.

**See also:** [Consensus-Based Weights](./subnets/consensus-based-weights.md), [Yuma Consensus](./yuma-consensus.md)

## Y 

### Yuma Consensus

The consensus mechanism in the Bittensor blockchain that computes emissions to participants. 

**See also:** [Yuma Consensus](./yuma-consensus.md)