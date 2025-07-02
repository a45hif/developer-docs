---
title: "Understanding Neurons"
---

import ThemedImage from '@theme/ThemedImage';
import useBaseUrl from '@docusaurus/useBaseUrl';

# Understanding Neurons


<!-- This needs to be updated and better, and consoloditated with the description in docstring in bittensor, so there isn't redundancy or inconsistency!!!) 

http://localhost:3000/python-api/html/autoapi/bittensor/core/metagraph/index.html#bittensor.core.metagraph.Metagraph
-->

The design of Bittensor subnets is inspired by the structure of a simple neural network, with each **neuron** being either a miner or validator. Each neuron is identified by a unique UID within its subnet and associated with a hotkey-coldkey pair for authentication and operations.

:::tip Neuron requirements
See [minimum compute requirements](https://github.com/opentensor/bittensor-subnet-template/blob/main/min_compute.yml) for compute, memory, bandwidth and storage requirements for neurons.
:::

## Neuron Architecture Overview

Neurons in a subnet operate within a server-client architecture:

- **Axon (Server)**: Miners deploy Axon servers to receive and process data from validators
- **Dendrite (Client)**: Validators use Dendrite clients to transmit data to miners  
- **Synapse (Data Object)**: Encapsulates and structures data exchanged between neurons

Additionally, the Metagraph serves as a global directory for managing subnet nodes, while the Subtensor connects neurons to the blockchain.

## Neuron Lifecycle and Management

### Registration and UID Assignment

Neurons register with subnets through proof-of-work or burned registration methods, receiving a unique UID (User ID) within their subnet. The registration process follows an append-or-replace algorithm where new neurons either expand the subnet or replace existing low-performing neurons.

### Performance Metrics

Neuron performance is measured through multiple metrics:
- **Rank**: Final performance score after consensus weight clipping
- **Trust**: Consensus alignment ratio measuring impact of consensus filtering  
- **Consensus**: Stake-weighted median of weights serving as clipping threshold
- **Incentive**: Normalized reward allocation for miners
- **Validator Trust**: Specialized trust score for validator neurons

### Validator Permits and Access Control

Top K neurons by stake weight receive validator permits, allowing them to:
- Set weights and participate in consensus
- Form bonds to miners based on performance assessment
- Contribute to active stake calculations

Only permitted neurons can set non-self weights, though all neurons can set self-weights regardless of permit status.

<!-- TODO: Add detailed implementation sections from glossary:
- Neuron Data Structures (NeuronInfo vs NeuronInfoLite)
- Blockchain Storage Implementation (Core Storage Maps, Performance Metrics Storage)
- Registration Process (PoW, Burned, Root registration methods)
- Lifecycle Management (Append vs Replace, Pruning Algorithm, Immunity Period)
- API and Retrieval (Python SDK methods, Blockchain RPC methods)
- State Management (Active Status, Validator Permits, Performance Metrics)
- Network Operations (Weight Setting, Bond Formation)
- Testing and Validation (Registration testing, Lifecycle testing, Mock implementation)
- Mathematical Insights and Security Properties
- Complete Neuron Lifecycle flow
- Neuron vs Subnet/Validator/Miner relationships
-->

## Neuron-to-neuron communication

Neurons exchange information by:

- Encapsulating the information in a Synapse object.
- Instantiating the server (Axon) and client (dendrite) network elements and exchanging Synapse objects using this server-client (Axon-dendrite) protocol. See the below diagram.

<center>
<ThemedImage
alt="Incentive Mechanism Big Picture"
sources={{
    light: useBaseUrl('/img/docs/second-building-blocks.svg'),
    dark: useBaseUrl('/img/docs/dark-second-building-blocks.svg'),
  }}
/>
</center>

### Axon

The `axon` module in the Bittensor API uses the FastAPI library to create and run API servers. For example, when a subnet miner calls,

```python
axon = bt.axon(wallet=self.wallet, config=self.config)
```

then an API server with the name `axon` is created on the subnet miner node. This `axon` API server receives incoming Synapse objects from subnet validators, i.e., the `axon` starts to serve on behalf of the subnet miner.

Similarly, in your subnet miner code you must use the `axon` API to create an API server to receive incoming Synapse objects from the subnet validators.

### Dendrite

Axon is a **server** instance. Hence, a subnet validator will instantiate a `dendrite` **client** on itself to transmit information to axons that are on the subnet miners. For example, when a subnet validator runs the following code fragment:

```python
    responses: List[bt.Synapse] = await self.dendrite(
        axons=axons,
        synapse=synapse,
        timeout=timeout,
    )
```

then the subnet validator:

- Instantiates a `dendrite` client on itself.
- Transmits `synapse` objects to a set of `axons` (that are attached to subnet miners).
- Waits until `timeout` expires.

### Synapse

A synapse is a data object. Subnet validators and subnet miners use Synapse data objects as the main vehicle to exchange information. The `Synapse` class inherits from the `BaseModel` of the Pydantic data validation library.

For example, in the [Text Prompting Subnet](https://github.com/macrocosm-os/prompting/blob/414abbb72835c46ccc5c652e1b1420c0c2be5c03/prompting/protocol.py#L27), the subnet validator creates a `Synapse` object, called `PromptingSynapse`, with three fields—`roles`, `messages`, and `completion`. The fields `roles` and `messages` are set by the subnet validator during the initialization of this Prompting data object, and they cannot be changed after that. A third field, `completion`, is mutable. When a subnet miner receives this Prompting object from the subnet validator, the subnet miner updates this `completion` field. The subnet validator then reads this updated `completion` field.

## The Neuron Metagraph

A metagraph is a data structure that contains comprehensive information about current state of the subnet. When you inspect the metagraph of a subnet, you will find detailed information on all the nodes (neurons) in the subnet. A subnet validator should first sync with a subnet's metagraph to know all the subnet miners that are in the subnet. The metagraph can be inspected without participating in a subnet.

## Implementation Details

<!-- TODO: Expand these sections with detailed code references and implementation specifics -->

### Neuron Data Structures

**NeuronInfo - Complete Neuron Data:**
- Contains comprehensive neuron metadata including weights and bonds
- Key performance metrics stored as normalized float values (0-1 range): rank, emission, incentive, consensus, trust, validator_trust
- Stake information includes both total stake and per-coldkey breakdown
- Network participation data: netuid, validator_permit, weights, bonds

**NeuronInfoLite - Lightweight Neuron Data:**
- Provides essential neuron data without weights and bonds for efficiency
- Used when full weight/bond data is not required, reducing data transfer overhead

**Code References:**
- `bittensor/core/chain_data/neuron_info.py:18` - NeuronInfo class definition
- `bittensor/core/chain_data/neuron_info_lite.py:18` - NeuronInfoLite class definition

### Blockchain Storage Implementation

**Core Storage Maps:**
- **Keys**: Maps (netuid, uid) to hotkey for UID-to-hotkey lookup
- **Uids**: Maps (netuid, hotkey) to uid for hotkey-to-UID lookup  
- **Owner**: Maps hotkey to coldkey for ownership verification

**Performance Metrics Storage:**
- **Rank, Trust, Consensus, Incentive**: Stored as u16 vectors per subnet
- **Emission**: Stored as u64 values representing emission rates
- **ValidatorPermit**: Boolean vector indicating validator permissions

**Code References:**
- `subtensor/pallets/subtensor/src/lib.rs:1533-1542` - Core storage map definitions
- `subtensor/pallets/subtensor/src/lib.rs:1524-1552` - Performance metrics storage

### Registration Process

**Registration Methods:**
- **Proof-of-Work Registration**: Traditional registration requiring computational work
- **Burned Registration**: Registration by burning TAO tokens
- **Root Registration**: Special registration for root network (netuid 0)

**Registration Algorithm:**
- **Append vs Replace Logic**: New neurons either append to subnet or replace existing ones
- **Pruning Selection**: When subnet is full, neuron with lowest pruning score is replaced
- **Immunity Period**: New neurons are protected from pruning for a configurable period

**Code References:**
- `subtensor/pallets/subtensor/src/subnets/registration.rs:214-339` - do_registration() implementation
- `subtensor/pallets/subtensor/src/subnets/registration.rs:54-206` - do_burned_registration() implementation
- `subtensor/pallets/subtensor/src/subnets/registration.rs:405-485` - get_neuron_to_prune() algorithm

### Neuron Lifecycle Management

**Append Neuron Process:**
- **UID Assignment**: New neurons get the next available UID (equal to current subnet size)
- **Storage Expansion**: All metric vectors are expanded to accommodate new neuron
- **Default Values**: New neurons start with zero values for all metrics

**Replace Neuron Process:**
- **Old Neuron Cleanup**: Previous neuron's data is cleared and associations removed
- **New Neuron Setup**: New neuron inherits the UID with fresh default values
- **Bond Clearing**: All bonds are cleared when neurons are replaced

**Code References:**
- `subtensor/pallets/subtensor/src/subnets/uids.rs:75-95` - append_neuron() implementation
- `subtensor/pallets/subtensor/src/subnets/uids.rs:35-75` - replace_neuron() implementation

### API and Retrieval

**Python SDK Methods:**
- **Individual Neuron Retrieval**: Get neuron by UID or hotkey
- **Batch Neuron Retrieval**: Get all neurons in a subnet
- **UID Lookup**: Find UID for a given hotkey on a subnet

**Blockchain RPC Methods:**
- **Runtime API**: Neurons are retrieved via NeuronInfoRuntimeApi
- **Storage Queries**: Direct storage access for UID and hotkey lookups
- **Batch Retrieval**: Efficient retrieval of all neurons in a subnet

**Code References:**
- `bittensor/core/subtensor.py:1369-1411` - get_neuron_for_pubkey_and_subnet() implementation
- `bittensor/core/async_subtensor.py:2183-2229` - Async version of neuron retrieval
- `subtensor/pallets/subtensor/src/rpc_info/neuron_info.rs:155` - get_neuron() RPC method

### State Management

**Active Status:**
- **Active Flag**: Boolean indicating if neuron is currently active
- **Last Update**: Block number of last activity for staleness detection
- **Staleness Filtering**: Neurons with outdated last_update are filtered from consensus

**Validator Permits:**
- **Permit Assignment**: Top K neurons by stake receive validator permits
- **Access Control**: Only permitted neurons can set weights and participate in consensus
- **Dynamic Updates**: Permits are recalculated every epoch based on current stake

**Code References:**
- `bittensor/core/chain_data/neuron_info.py:26` - active status field
- `subtensor/pallets/subtensor/src/epoch/run_epoch.rs:520-523` - Validator permit assignment
- `subtensor/pallets/subtensor/src/subnets/weights.rs:745-748` - Weight setting permission check

### Network Operations

**Weight Setting:**
- **Weight Matrix**: Neurons set weights to other neurons, forming the consensus matrix
- **Permission Control**: Only validator-permitted neurons can set non-self weights
- **Self-Weight Exception**: All neurons can set self-weights regardless of permit status

**Bond Formation:**
- **Bond Investment**: Validators form bonds to miners based on performance assessment
- **EMA Bonds**: Bonds are smoothed using exponential moving average
- **Bond Retention**: Bonds are retained only by neurons with validator permits

**Code References:**
- `subtensor/pallets/subtensor/src/lib.rs:1543-1549` - Weights storage definition
- `subtensor/pallets/subtensor/src/lib.rs:1560-1566` - Bonds storage definition
- `subtensor/pallets/subtensor/src/epoch/run_epoch.rs:687` - EMA bond computation

### Testing and Validation

**Registration Testing:**
- **Successful Registration**: Tests verify proper neuron registration and UID assignment
- **Pruning Scenarios**: Tests verify correct neuron replacement when subnet is full
- **Immunity Period**: Tests verify immunity protection during registration

**Neuron Lifecycle Testing:**
- **Replace Neuron**: Tests verify proper neuron replacement and data clearing
- **Owner Protection**: Tests verify subnet owners are protected from pruning
- **Bond Management**: Tests verify bond clearing during neuron replacement

**Mock Implementation:**
- **Mock Subtensor**: Provides in-memory neuron management for testing
- **Force Registration**: Allows test-specific neuron registration
- **State Management**: Mock maintains neuron state across test scenarios

**Code References:**
- `subtensor/pallets/subtensor/src/tests/registration.rs:102-192` - Registration success tests
- `subtensor/pallets/subtensor/src/tests/uids.rs:15-201` - Neuron replacement tests
- `bittensor/utils/mock/subtensor_mock.py:725-786` - Mock neuron retrieval methods

### Key Mathematical Insights

1. **Neuron = UID + Hotkey + Coldkey**: Each neuron is uniquely identified by its UID and key pair
2. **Registration = Append or Replace**: New neurons either expand the subnet or replace existing ones
3. **Pruning = Lowest Score**: Neurons with lowest pruning scores are replaced when subnet is full
4. **Immunity = Protection Period**: New neurons are protected from pruning for a configurable period
5. **Performance = Multi-Metric**: Neuron performance is measured by rank, trust, consensus, and incentive

### Network Security Properties

- **Economic Barriers**: Registration costs prevent Sybil attacks
- **Performance-Based Pruning**: Low-performing neurons are automatically replaced
- **Stake-Based Permits**: Validator permits require economic stake for consensus participation
- **Dynamic Adjustment**: Neuron state adapts to changing network conditions
- **Owner Protection**: Subnet owners are protected from pruning to ensure network stability

### Complete Neuron Lifecycle

1. **Registration** → Neuron registers via PoW or burned registration
2. **UID Assignment** → Neuron receives unique UID within subnet
3. **Immunity Period** → Neuron is protected from pruning for configurable blocks
4. **Performance Building** → Neuron accumulates rank, trust, consensus, and incentive
5. **Validator Permit** → Top K neurons by stake receive validator permits
6. **Weight Setting** → Permitted neurons can set weights and participate in consensus
7. **Bond Formation** → Validators form bonds to miners based on performance
8. **Emission Distribution** → Neurons receive TAO emissions based on performance
9. **Performance Monitoring** → Neuron performance is continuously evaluated
10. **Pruning Risk** → Low-performing neurons risk replacement by new registrations

### Neuron Relationships

**Neuron vs Subnet Relationship:**
- **Subnet Container**: Neurons exist within specific subnets identified by netuid
- **Subnet Limits**: Each subnet has maximum allowed UIDs (typically 256)
- **Subnet-Specific**: Neuron metrics and state are subnet-specific
- **Cross-Subnet**: Neurons can participate in multiple subnets with different UIDs
- **Subnet Governance**: Subnet owners have special privileges and protection

**Neuron vs Validator/Miner Roles:**
- **Neuron = Container**: Neuron is the container entity that can be either validator or miner
- **Validator = Role**: Neurons with validator permits can set weights and participate in consensus
- **Miner = Role**: Neurons without validator permits perform subnet-specific tasks
- **Role Flexibility**: Neurons can change roles based on permit status and stake
- **Performance Metrics**: Both roles contribute to neuron's overall performance score
