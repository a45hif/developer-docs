---
title: "Metagraph Precompile"
---

import ThemedImage from '@theme/ThemedImage';
import useBaseUrl from '@docusaurus/useBaseUrl';


# Metagraph Precompile

The metagraph precompile allows you to query information about neurons, their relationships, and network state in the Bittensor network. This precompile provides read-only access to the metagraph data through smart contracts at precompile address `2050`.

## Overview

The metagraph precompile is a powerful tool that enables smart contracts to interact with the Bittensor network's metagraph data. It provides access to various metrics and information about neurons including stakes, ranks, trust scores, consensus values, and more.

All functions in this precompile are view-only operations that don't modify state and consume minimal gas.

## Source Code and Tests

- **Source Code**: [metagraph.rs](https://github.com/opentensor/subtensor/blob/main/precompiles/src/metagraph.rs)
- **Test Examples**: [metagraph precompile tests](https://github.com/opentensor/developer-docs/blob/main/evm-tutorials/test/metagraph.test.ts)

## Function Reference

### Network Information

#### `getUidCount(uint16 netuid) → uint16`

Returns the total number of UIDs (neurons) in a specific subnetwork.

**Parameters:**
- `netuid` (uint16): The subnetwork ID to query

**Returns:**
- `uint16`: Total count of neurons in the subnetwork


### Token and Consensus Metrics

#### `getStake(uint16 netuid, uint16 uid) → uint64`

Retrieves the total stake amount for a specific neuron.

**Parameters:**
- `netuid` (uint16): The subnetwork ID
- `uid` (uint16): The unique identifier of the neuron

**Returns:**
- `uint64`: Total stake amount for the neuron's hotkey

**Errors:**
- Reverts with `InvalidRange` if the UID doesn't exist in the network



#### `getEmission(uint16 netuid, uint16 uid) → uint64`

Gets the emission value for a specific neuron, representing its reward allocation.

**Parameters:**
- `netuid` (uint16): The subnetwork ID
- `uid` (uint16): The unique identifier of the neuron

**Returns:**
- `uint64`: Emission value for the neuron


#### `getRank(uint16 netuid, uint16 uid) → uint16`

Returns the rank score of a neuron, indicating its performance relative to others.

**Parameters:**
- `netuid` (uint16): The subnetwork ID
- `uid` (uint16): The unique identifier of the neuron

**Returns:**
- `uint16`: Rank score of the neuron


#### `getTrust(uint16 netuid, uint16 uid) → uint16`

Retrieves the trust score of a neuron, representing how much other neurons trust its outputs.

**Parameters:**
- `netuid` (uint16): The subnetwork ID
- `uid` (uint16): The unique identifier of the neuron

**Returns:**
- `uint16`: Trust score of the neuron



#### `getConsensus(uint16 netuid, uint16 uid) → uint16`

Gets the consensus score of a neuron, indicating agreement with network consensus.

**Parameters:**
- `netuid` (uint16): The subnetwork ID
- `uid` (uint16): The unique identifier of the neuron

**Returns:**
- `uint16`: Consensus score of the neuron


#### `getIncentive(uint16 netuid, uint16 uid) → uint16`

Returns the incentive score of a neuron, representing its contribution to the network.

**Parameters:**
- `netuid` (uint16): The subnetwork ID
- `uid` (uint16): The unique identifier of the neuron

**Returns:**
- `uint16`: Incentive score of the neuron


#### `getDividends(uint16 netuid, uint16 uid) → uint16`

Retrieves the dividends score of a neuron, indicating its reward distribution.

**Parameters:**
- `netuid` (uint16): The subnetwork ID
- `uid` (uint16): The unique identifier of the neuron

**Returns:**
- `uint16`: Dividends score of the neuron


### Validator-Specific Functions

#### `getVtrust(uint16 netuid, uint16 uid) → uint16`

Gets the validator trust score for a neuron, specific to validator operations.

**Parameters:**
- `netuid` (uint16): The subnetwork ID
- `uid` (uint16): The unique identifier of the neuron

**Returns:**
- `uint16`: Validator trust score



#### `getValidatorStatus(uint16 netuid, uint16 uid) → bool`

Checks if a neuron has validator permit status.

**Parameters:**
- `netuid` (uint16): The subnetwork ID
- `uid` (uint16): The unique identifier of the neuron

**Returns:**
- `bool`: True if the neuron has validator permissions, false otherwise


### Neuron State Information

#### `getLastUpdate(uint16 netuid, uint16 uid) → uint64`

Returns the block number of the last update for a neuron.

**Parameters:**
- `netuid` (uint16): The subnetwork ID
- `uid` (uint16): The unique identifier of the neuron

**Returns:**
- `uint64`: Block number of the last update



#### `getIsActive(uint16 netuid, uint16 uid) → bool`

Checks if a neuron is currently active in the network.

**Parameters:**
- `netuid` (uint16): The subnetwork ID
- `uid` (uint16): The unique identifier of the neuron

**Returns:**
- `bool`: True if the neuron is active, false otherwise



### Network Connection Information

#### `getAxon(uint16 netuid, uint16 uid) → AxonInfo`

Retrieves the axon information for a neuron, including network connection details.

**Parameters:**
- `netuid` (uint16): The subnetwork ID
- `uid` (uint16): The unique identifier of the neuron

**Returns:**
- `AxonInfo`: Struct containing axon connection information

**AxonInfo Structure:**
```solidity
struct AxonInfo {
    uint64 block;      // Block number when axon was registered
    uint32 version;    // Protocol version
    uint128 ip;        // IP address (IPv4 or IPv6)
    uint16 port;       // Port number
    uint8 ip_type;     // IP type (4 for IPv4, 6 for IPv6)
    uint8 protocol;    // Protocol type
}
```

**Errors:**
- Reverts with "hotkey not found" if the neuron doesn't exist


### Key Management

#### `getHotkey(uint16 netuid, uint16 uid) → bytes32`

Returns the hotkey (public key) associated with a neuron.

**Parameters:**
- `netuid` (uint16): The subnetwork ID
- `uid` (uint16): The unique identifier of the neuron

**Returns:**
- `bytes32`: The hotkey as a 32-byte hash

**Errors:**
- Reverts with `InvalidRange` if the UID doesn't exist

#### `getColdkey(uint16 netuid, uint16 uid) → bytes32`

Returns the coldkey (owner key) associated with a neuron's hotkey.

**Parameters:**
- `netuid` (uint16): The subnetwork ID
- `uid` (uint16): The unique identifier of the neuron

**Returns:**
- `bytes32`: The coldkey as a 32-byte hash

**Errors:**
- Reverts with `InvalidRange` if the UID doesn't exist


## Usage Examples

### Setup

First, set up your client to interact with the metagraph precompile:

```javascript
import { getPublicClient } from "viem";

// Source: https://github.com/opentensor/subtensor/blob/main/evm-tests/src/contracts/metagraph.ts
const IMETAGRAPH_ADDRESS = "0x0000000000000000000000000000000000000802";

const IMetagraphABI = [
    {
        inputs: [
            {
                internalType: "uint16",
                name: "netuid",
                type: "uint16",
            },
            {
                internalType: "uint16",
                name: "uid",
                type: "uint16",
            },
        ],
        name: "getAxon",
        outputs: [
            {
                components: [
                    {
                        internalType: "uint64",
                        name: "block",
                        type: "uint64",
                    },
                    {
                        internalType: "uint32",
                        name: "version",
                        type: "uint32",
                    },
                    {
                        internalType: "uint128",
                        name: "ip",
                        type: "uint128",
                    },
                    {
                        internalType: "uint16",
                        name: "port",
                        type: "uint16",
                    },
                    {
                        internalType: "uint8",
                        name: "ip_type",
                        type: "uint8",
                    },
                    {
                        internalType: "uint8",
                        name: "protocol",
                        type: "uint8",
                    },
                ],
                internalType: "struct AxonInfo",
                name: "",
                type: "tuple",
            },
        ],
        stateMutability: "view",
        type: "function",
    },
    {
        inputs: [
            {
                internalType: "uint16",
                name: "netuid",
                type: "uint16",
            },
            {
                internalType: "uint16",
                name: "uid",
                type: "uint16",
            },
        ],
        name: "getColdkey",
        outputs: [
            {
                internalType: "bytes32",
                name: "",
                type: "bytes32",
            },
        ],
        stateMutability: "view",
        type: "function",
    },
    {
        inputs: [
            {
                internalType: "uint16",
                name: "netuid",
                type: "uint16",
            },
            {
                internalType: "uint16",
                name: "uid",
                type: "uint16",
            },
        ],
        name: "getConsensus",
        outputs: [
            {
                internalType: "uint16",
                name: "",
                type: "uint16",
            },
        ],
        stateMutability: "view",
        type: "function",
    },
    {
        inputs: [
            {
                internalType: "uint16",
                name: "netuid",
                type: "uint16",
            },
            {
                internalType: "uint16",
                name: "uid",
                type: "uint16",
            },
        ],
        name: "getDividends",
        outputs: [
            {
                internalType: "uint16",
                name: "",
                type: "uint16",
            },
        ],
        stateMutability: "view",
        type: "function",
    },
    {
        inputs: [
            {
                internalType: "uint16",
                name: "netuid",
                type: "uint16",
            },
            {
                internalType: "uint16",
                name: "uid",
                type: "uint16",
            },
        ],
        name: "getEmission",
        outputs: [
            {
                internalType: "uint64",
                name: "",
                type: "uint64",
            },
        ],
        stateMutability: "view",
        type: "function",
    },
    {
        inputs: [
            {
                internalType: "uint16",
                name: "netuid",
                type: "uint16",
            },
            {
                internalType: "uint16",
                name: "uid",
                type: "uint16",
            },
        ],
        name: "getHotkey",
        outputs: [
            {
                internalType: "bytes32",
                name: "",
                type: "bytes32",
            },
        ],
        stateMutability: "view",
        type: "function",
    },
    {
        inputs: [
            {
                internalType: "uint16",
                name: "netuid",
                type: "uint16",
            },
            {
                internalType: "uint16",
                name: "uid",
                type: "uint16",
            },
        ],
        name: "getIncentive",
        outputs: [
            {
                internalType: "uint16",
                name: "",
                type: "uint16",
            },
        ],
        stateMutability: "view",
        type: "function",
    },
    {
        inputs: [
            {
                internalType: "uint16",
                name: "netuid",
                type: "uint16",
            },
            {
                internalType: "uint16",
                name: "uid",
                type: "uint16",
            },
        ],
        name: "getIsActive",
        outputs: [
            {
                internalType: "bool",
                name: "",
                type: "bool",
            },
        ],
        stateMutability: "view",
        type: "function",
    },
    {
        inputs: [
            {
                internalType: "uint16",
                name: "netuid",
                type: "uint16",
            },
            {
                internalType: "uint16",
                name: "uid",
                type: "uint16",
            },
        ],
        name: "getLastUpdate",
        outputs: [
            {
                internalType: "uint64",
                name: "",
                type: "uint64",
            },
        ],
        stateMutability: "view",
        type: "function",
    },
    {
        inputs: [
            {
                internalType: "uint16",
                name: "netuid",
                type: "uint16",
            },
            {
                internalType: "uint16",
                name: "uid",
                type: "uint16",
            },
        ],
        name: "getRank",
        outputs: [
            {
                internalType: "uint16",
                name: "",
                type: "uint16",
            },
        ],
        stateMutability: "view",
        type: "function",
    },
    {
        inputs: [
            {
                internalType: "uint16",
                name: "netuid",
                type: "uint16",
            },
            {
                internalType: "uint16",
                name: "uid",
                type: "uint16",
            },
        ],
        name: "getStake",
        outputs: [
            {
                internalType: "uint64",
                name: "",
                type: "uint64",
            },
        ],
        stateMutability: "view",
        type: "function",
    },
    {
        inputs: [
            {
                internalType: "uint16",
                name: "netuid",
                type: "uint16",
            },
            {
                internalType: "uint16",
                name: "uid",
                type: "uint16",
            },
        ],
        name: "getTrust",
        outputs: [
            {
                internalType: "uint16",
                name: "",
                type: "uint16",
            },
        ],
        stateMutability: "view",
        type: "function",
    },
    {
        inputs: [
            {
                internalType: "uint16",
                name: "netuid",
                type: "uint16",
            },
        ],
        name: "getUidCount",
        outputs: [
            {
                internalType: "uint16",
                name: "",
                type: "uint16",
            },
        ],
        stateMutability: "view",
        type: "function",
    },
    {
        inputs: [
            {
                internalType: "uint16",
                name: "netuid",
                type: "uint16",
            },
            {
                internalType: "uint16",
                name: "uid",
                type: "uint16",
            },
        ],
        name: "getValidatorStatus",
        outputs: [
            {
                internalType: "bool",
                name: "",
                type: "bool",
            },
        ],
        stateMutability: "view",
        type: "function",
    },
    {
        inputs: [
            {
                internalType: "uint16",
                name: "netuid",
                type: "uint16",
            },
            {
                internalType: "uint16",
                name: "uid",
                type: "uint16",
            },
        ],
        name: "getVtrust",
        outputs: [
            {
                internalType: "uint16",
                name: "",
                type: "uint16",
            },
        ],
        stateMutability: "view",
        type: "function",
    },
];

// Initialize the public client
const publicClient = await getPublicClient("YOUR_RPC_URL");
const METAGRAPH_ADDRESS = "0x0000000000000000000000000000000000000802"; // Precompile address 2050
```

### Getting Network Information

```javascript
// Get the total number of neurons in a subnetwork
const subnetId = 1; // Example subnet ID
const uidCount = await publicClient.readContract({
    abi: IMetagraphABI,
    address: METAGRAPH_ADDRESS,
    functionName: "getUidCount",
    args: [subnetId]
});

console.log(`Total neurons in subnet ${subnetId}: ${uidCount}`);
```

### Querying Neuron Metrics

```javascript
const subnetId = 14;
const uid = 26; // Example neuron UID

// Get stake amount
const stake = await publicClient.readContract({
    abi: IMetagraphABI,
    address: METAGRAPH_ADDRESS,
    functionName: "getStake",
    args: [subnetId, uid]
});

// Get emission value
const emission = await publicClient.readContract({
    abi: IMetagraphABI,
    address: METAGRAPH_ADDRESS,
    functionName: "getEmission",
    args: [subnetId, uid]
});

// Get trust score
const trust = await publicClient.readContract({
    abi: IMetagraphABI,
    address: METAGRAPH_ADDRESS,
    functionName: "getTrust",
    args: [subnetId, uid]
});

console.log(`Neuron ${uid} - Stake: ${stake}, Emission: ${emission}, Trust: ${trust}`);
```

### Getting Neuron Connection Information

```javascript
// Get axon information for network connectivity
const axon = await publicClient.readContract({
    abi: IMetagraphABI,
    address: METAGRAPH_ADDRESS,
    functionName: "getAxon",
    args: [subnetId, uid]
});

console.log("Axon Info:", {
    block: axon.block,
    version: axon.version,
    ip: axon.ip,
    port: axon.port,
    ipType: axon.ip_type,
    protocol: axon.protocol
});
```

### Checking Validator Status

```javascript
// Check if a neuron is a validator
const isValidator = await publicClient.readContract({
    abi: IMetagraphABI,
    address: METAGRAPH_ADDRESS,
    functionName: "getValidatorStatus",
    args: [subnetId, uid]
});

// Get validator trust score
const vtrust = await publicClient.readContract({
    abi: IMetagraphABI,
    address: METAGRAPH_ADDRESS,
    functionName: "getVtrust",
    args: [subnetId, uid]
});

console.log(`Neuron ${uid} - Is Validator: ${isValidator}, VTrust: ${vtrust}`);
```

### Getting Key Information

```javascript
// Get hotkey and coldkey for a neuron
const hotkey = await publicClient.readContract({
    abi: IMetagraphABI,
    address: METAGRAPH_ADDRESS,
    functionName: "getHotkey",
    args: [subnetId, uid]
});

const coldkey = await publicClient.readContract({
    abi: IMetagraphABI,
    address: METAGRAPH_ADDRESS,
    functionName: "getColdkey",
    args: [subnetId, uid]
});

console.log(`Neuron ${uid} - Hotkey: ${hotkey}, Coldkey: ${coldkey}`);
```

### Comprehensive Neuron Analysis

```javascript
async function analyzeNeuron(subnetId, uid) {
    try {
        // Get all key metrics for a neuron
        const [
            stake,
            emission,
            rank,
            trust,
            consensus,
            incentive,
            dividends,
            lastUpdate,
            isActive,
            validatorStatus
        ] = await Promise.all([
            publicClient.readContract({
                abi: IMetagraphABI,
                address: METAGRAPH_ADDRESS,
                functionName: "getStake",
                args: [subnetId, uid]
            }),
            publicClient.readContract({
                abi: IMetagraphABI,
                address: METAGRAPH_ADDRESS,
                functionName: "getEmission",
                args: [subnetId, uid]
            }),
            publicClient.readContract({
                abi: IMetagraphABI,
                address: METAGRAPH_ADDRESS,
                functionName: "getRank",
                args: [subnetId, uid]
            }),
            publicClient.readContract({
                abi: IMetagraphABI,
                address: METAGRAPH_ADDRESS,
                functionName: "getTrust",
                args: [subnetId, uid]
            }),
            publicClient.readContract({
                abi: IMetagraphABI,
                address: METAGRAPH_ADDRESS,
                functionName: "getConsensus",
                args: [subnetId, uid]
            }),
            publicClient.readContract({
                abi: IMetagraphABI,
                address: METAGRAPH_ADDRESS,
                functionName: "getIncentive",
                args: [subnetId, uid]
            }),
            publicClient.readContract({
                abi: IMetagraphABI,
                address: METAGRAPH_ADDRESS,
                functionName: "getDividends",
                args: [subnetId, uid]
            }),
            publicClient.readContract({
                abi: IMetagraphABI,
                address: METAGRAPH_ADDRESS,
                functionName: "getLastUpdate",
                args: [subnetId, uid]
            }),
            publicClient.readContract({
                abi: IMetagraphABI,
                address: METAGRAPH_ADDRESS,
                functionName: "getIsActive",
                args: [subnetId, uid]
            }),
            publicClient.readContract({
                abi: IMetagraphABI,
                address: METAGRAPH_ADDRESS,
                functionName: "getValidatorStatus",
                args: [subnetId, uid]
            })
        ]);

        return {
            uid,
            stake,
            emission,
            rank,
            trust,
            consensus,
            incentive,
            dividends,
            lastUpdate,
            isActive,
            isValidator: validatorStatus
        };
    } catch (error) {
        console.error(`Error analyzing neuron ${uid}:`, error);
        throw error;
    }
}

// Usage
const neuronData = await analyzeNeuron(1, 0);
console.log("Neuron Analysis:", neuronData);
```

### Error Handling

```javascript
async function safeGetStake(subnetId, uid) {
    try {
        const stake = await publicClient.readContract({
            abi: IMetagraphABI,
            address: METAGRAPH_ADDRESS,
            functionName: "getStake",
            args: [subnetId, uid]
        });
        return stake;
    } catch (error) {
        if (error.message.includes("InvalidRange")) {
            console.error(`UID ${uid} does not exist in subnet ${subnetId}`);
            return null;
        }
        throw error;
    }
}
```
