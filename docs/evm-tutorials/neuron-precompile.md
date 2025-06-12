---
title: "Neuron Precompile"
---

import ThemedImage from '@theme/ThemedImage';
import useBaseUrl from '@docusaurus/useBaseUrl';

# Neuron Precompile


This precompile enables full management of neurons (miner and validator nodes) through smart contracts, from registration to weight setting to service configuration. 

See [Understanding Neurons](../learn/neurons.md).

:::info
Payable functions require tokens for execution
:::

## Precompile Address

The neuron precompile is available at address `0x804` (2052 in decimal).

## Available Functions

The neuron precompile provides the following core functions for neuron management:

### Weight Management

#### `setWeights`
Set weights (rankings) for miners on the subnet. See [Requirements for validation](../validators/#requirements-for-validation)

**Parameters:**
- `netuid` (uint16): The subnet ID where the neuron is registered
- `dests` (uint16[]): Array of destination neuron UIDs to assign weights to
- `weights` (uint16[]): Array of weight values corresponding to each destination UID
- `versionKey` (uint64): Version key for weight compatibility and validation

**Description:**
This function allows a neuron to set weights on other neurons in the same subnet. The weights represent how much value or trust this neuron assigns to others, which is crucial for the Bittensor consensus mechanism.

#### `commitWeights`
Commits weights using a hash commitment scheme for privacy and security.

**Parameters:**
- `netuid` (uint16): The subnet ID where the neuron is registered
- `commitHash` (bytes32): Hash commitment of the weights to be revealed later

**Description:**
This function implements a commit-reveal scheme for setting weights. The neuron first commits a hash of their weights, then later reveals the actual weights. This prevents weight-copying.

#### `revealWeights`
Reveals previously committed weights by providing the original data that produces the committed hash.

**Parameters:**
- `netuid` (uint16): The subnet ID where the neuron is registered
- `uids` (uint16[]): Array of neuron UIDs that weights are being set for
- `values` (uint16[]): Array of weight values for each corresponding UID
- `salt` (uint16[]): Salt values used in the original hash commitment
- `versionKey` (uint64): Version key for weight compatibility

**Description:**
This function completes the commit-reveal process by revealing the actual weights that were previously committed. The provided data must hash to the previously committed hash for the transaction to succeed.

### Neuron Registration

Neuron registration is required for joining a subnet as a miner or validator

#### `burnedRegister`
Registers a neuron in a subnet by burning TAO tokens.

**Parameters:**
- `netuid` (uint16): The subnet ID to register the neuron in
- `hotkey` (bytes32): The hotkey public key (32 bytes) of the neuron to register

**Description:**
This function registers a new neuron in the specified subnet by burning a certain amount of TAO tokens. The amount burned depends on the current network conditions and subnet parameters. The hotkey represents the neuron's identity on the network.

### Axon Services

#### `serveAxon`
Configures and serves an axon endpoint for the neuron.

**Parameters:**
- `netuid` (uint16): The subnet ID where the neuron is serving
- `version` (uint32): Version of the axon service
- `ip` (uint128): IP address of the axon service (supports both IPv4 and IPv6)
- `port` (uint16): Port number where the axon is listening
- `ipType` (uint8): Type of IP address (4 for IPv4, 6 for IPv6)
- `protocol` (uint8): Network protocol identifier
- `placeholder1` (uint8): Reserved for future use
- `placeholder2` (uint8): Reserved for future use

**Description:**
This function allows a neuron to announce its axon service endpoint to the network. An axon is the service interface that other neurons can connect to for communication and inference requests using the dendrite-axon protocol.

#### `serveAxonTls`
Configures and serves an axon endpoint with TLS/SSL security.


**Parameters:**
- `netuid` (uint16): The subnet ID where the neuron is serving
- `version` (uint32): Version of the axon service
- `ip` (uint128): IP address of the axon service
- `port` (uint16): Port number where the axon is listening
- `ipType` (uint8): Type of IP address (4 for IPv4, 6 for IPv6)
- `protocol` (uint8): Network protocol identifier
- `placeholder1` (uint8): Reserved for future use
- `placeholder2` (uint8): Reserved for future use
- `certificate` (bytes): TLS/SSL certificate data for secure connections

**Description:**
Similar to `serveAxon`, but includes TLS certificate information for secure encrypted communication. This is recommended for production environments where data privacy and security are important.

#### `servePrometheus`
Configures a Prometheus metrics endpoint for the neuron.



**Parameters:**
- `netuid` (uint16): The subnet ID where the neuron is serving
- `version` (uint32): Version of the Prometheus service
- `ip` (uint128): IP address where Prometheus metrics are served
- `port` (uint16): Port number for the Prometheus endpoint
- `ipType` (uint8): Type of IP address (4 for IPv4, 6 for IPv6)

**Description:**
This function allows a neuron to expose a Prometheus metrics endpoint for monitoring and observability. Prometheus metrics can include performance data, request counts, and other operational metrics.

## Usage Examples

### Setup

Before using the neuron precompile, you'll need to set up the basic infrastructure:

```javascript
import { ethers } from "ethers";

// Neuron precompile address and ABI
// Source: https://raw.githubusercontent.com/opentensor/subtensor/refs/heads/main/evm-tests/src/contracts/neuron.ts
const INEURON_ADDRESS = "0x0000000000000000000000000000000000000804";

const INeuronABI = [
    {
        inputs: [
            {
                internalType: "uint16",
                name: "netuid",
                type: "uint16",
            },
            {
                internalType: "bytes32",
                name: "commitHash",
                type: "bytes32",
            },
        ],
        name: "commitWeights",
        outputs: [],
        stateMutability: "payable",
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
                internalType: "uint16[]",
                name: "uids",
                type: "uint16[]",
            },
            {
                internalType: "uint16[]",
                name: "values",
                type: "uint16[]",
            },
            {
                internalType: "uint16[]",
                name: "salt",
                type: "uint16[]",
            },
            {
                internalType: "uint64",
                name: "versionKey",
                type: "uint64",
            },
        ],
        name: "revealWeights",
        outputs: [],
        stateMutability: "payable",
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
                internalType: "uint16[]",
                name: "dests",
                type: "uint16[]",
            },
            {
                internalType: "uint16[]",
                name: "weights",
                type: "uint16[]",
            },
            {
                internalType: "uint64",
                name: "versionKey",
                type: "uint64",
            },
        ],
        name: "setWeights",
        outputs: [],
        stateMutability: "payable",
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
                name: "ipType",
                type: "uint8",
            },
            {
                internalType: "uint8",
                name: "protocol",
                type: "uint8",
            },
            {
                internalType: "uint8",
                name: "placeholder1",
                type: "uint8",
            },
            {
                internalType: "uint8",
                name: "placeholder2",
                type: "uint8",
            },
        ],
        name: "serveAxon",
        outputs: [],
        stateMutability: "payable",
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
                name: "ipType",
                type: "uint8",
            },
            {
                internalType: "uint8",
                name: "protocol",
                type: "uint8",
            },
            {
                internalType: "uint8",
                name: "placeholder1",
                type: "uint8",
            },
            {
                internalType: "uint8",
                name: "placeholder2",
                type: "uint8",
            },
            {
                internalType: "bytes",
                name: "certificate",
                type: "bytes",
            },
        ],
        name: "serveAxonTls",
        outputs: [],
        stateMutability: "payable",
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
                name: "ipType",
                type: "uint8",
            },
        ],
        name: "servePrometheus",
        outputs: [],
        stateMutability: "payable",
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
                internalType: "bytes32",
                name: "hotkey",
                type: "bytes32",
            },
        ],
        name: "burnedRegister",
        outputs: [],
        stateMutability: "payable",
        type: "function",
    },
];

// Initialize contract instance
const provider = new ethers.JsonRpcProvider("YOUR_RPC_URL");
const wallet = new ethers.Wallet("YOUR_PRIVATE_KEY", provider);
const neuronContract = new ethers.Contract(INEURON_ADDRESS, INeuronABI, wallet);
```

### Neuron Registration

#### Register a Neuron by Burning TAO

```javascript
async function registerNeuron() {
  try {
    const netuid = 1; // Target subnet ID
    const hotkey = "0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"; // 32-byte hotkey
    
    const tx = await neuronContract.burnedRegister(netuid, hotkey);
    await tx.wait();
    
    console.log("Neuron registered successfully!");
    console.log("Transaction hash:", tx.hash);
  } catch (error) {
    console.error("Registration failed:", error);
  }
}
```

### Weight Management

#### Setting Weights Directly

```javascript
async function setNeuronWeights() {
  try {
    const netuid = 1;
    const dests = [1, 2, 3]; // Target neuron UIDs
    const weights = [100, 200, 150]; // Weight values for each target
    const versionKey = 0;
    
    const tx = await neuronContract.setWeights(netuid, dests, weights, versionKey);
    await tx.wait();
    
    console.log("Weights set successfully!");
    console.log("Transaction hash:", tx.hash);
  } catch (error) {
    console.error("Setting weights failed:", error);
  }
}
```

#### Commit-Reveal Weight Setting

For subnets with commit-reveal enabled, you must first commit a hash of your weights, then reveal them later:

```javascript
import { blake2AsU8a } from "@polkadot/util-crypto";
import { Vec, Tuple, VecFixed, u16, u8, u64 } from "@polkadot/types-codec";
import { TypeRegistry } from "@polkadot/types";
import { hexToU8a } from "@polkadot/util";

// Helper function to convert Ethereum address to public key
// Logic adapted from: https://github.com/opentensor/subtensor/blob/main/evm-tests/src/address-utils.ts
function convertH160ToPublicKey(ethAddress) {
  const prefix = "evm:";
  const prefixBytes = new TextEncoder().encode(prefix);
  const addressBytes = hexToU8a(
    ethAddress.startsWith("0x") ? ethAddress : `0x${ethAddress}`
  );
  const combined = new Uint8Array(prefixBytes.length + addressBytes.length);

  // Concatenate prefix and Ethereum address
  combined.set(prefixBytes);
  combined.set(addressBytes, prefixBytes.length);

  // Hash the combined data (the public key)
  const hash = blake2AsU8a(combined);
  return hash;
}

// Helper function to generate commit hash
// Logic adapted from: https://github.com/opentensor/subtensor/blob/main/evm-tests/test/neuron.precompile.reveal-weights.test.ts
function generateCommitHash(netuid, address, uids, values, salt, version_key) {
  const registry = new TypeRegistry();
  
  // Convert Ethereum address to public key format (32 bytes)
  const publicKey = convertH160ToPublicKey(address);
  
  const tupleData = new Tuple(
    registry,
    [
      VecFixed.with(u8, 32), // Public key
      u16,                   // Network UID
      Vec.with(u16),         // UIDs
      Vec.with(u16),         // Values
      Vec.with(u16),         // Salt
      u64,                   // Version key
    ],
    [publicKey, netuid, uids, values, salt, version_key]
  );
  
  return blake2AsU8a(tupleData.toU8a());
}

// Step 1: Commit weights
async function commitWeights() {
  try {
    const netuid = 1;
    const uids = [1];
    const values = [5];
    const salt = [9]; // Random salt values
    const version_key = 0;
    
    // Generate commit hash
    const commitHash = generateCommitHash(netuid, wallet.address, uids, values, salt, version_key);
    
    const tx = await neuronContract.commitWeights(netuid, commitHash);
    await tx.wait();
    
    console.log("Weights committed successfully!");
    console.log("Transaction hash:", tx.hash);
    
    // Store the reveal data for later use
    return { uids, values, salt, version_key };
  } catch (error) {
    console.error("Committing weights failed:", error);
  }
}

// Step 2: Reveal weights (after commit period)
async function revealWeights(revealData) {
  try {
    const netuid = 1;
    const { uids, values, salt, version_key } = revealData;
    
    const tx = await neuronContract.revealWeights(netuid, uids, values, salt, version_key);
    await tx.wait();
    
    console.log("Weights revealed successfully!");
    console.log("Transaction hash:", tx.hash);
  } catch (error) {
    console.error("Revealing weights failed:", error);
  }
}

// Complete commit-reveal process
async function commitRevealWeights() {
  const revealData = await commitWeights();
  
  // Wait for the appropriate time (based on subnet parameters)
  // In production, you'd wait for the reveal period to begin
  
  await revealWeights(revealData);
}
```

:::tip
The commit-reveal mechanism requires generating a proper hash commitment using substrate utilities. Refer to the [test implementation](https://github.com/opentensor/subtensor/blob/main/evm-tests/test/neuron.precompile.reveal-weights.test.ts) for the complete hash generation logic.
:::

### Service Configuration

#### Serve Axon Endpoint

```javascript
async function serveAxon() {
  try {
    const netuid = 1;
    const version = 1;
    const ip = 0x7f000001; // 127.0.0.1 in hex
    const port = 8080;
    const ipType = 4; // IPv4
    const protocol = 0;
    const placeholder1 = 0;
    const placeholder2 = 0;
    
    const tx = await neuronContract.serveAxon(
      netuid,
      version,
      ip,
      port,
      ipType,
      protocol,
      placeholder1,
      placeholder2
    );
    await tx.wait();
    
    console.log("Axon endpoint configured successfully!");
    console.log("Transaction hash:", tx.hash);
  } catch (error) {
    console.error("Serving axon failed:", error);
  }
}
```

#### Serve Axon with TLS

```javascript
async function serveAxonTls() {
  try {
    const netuid = 1;
    const version = 1;
    const ip = 0x7f000001; // 127.0.0.1 in hex
    const port = 8443; // HTTPS port
    const ipType = 4; // IPv4
    const protocol = 0;
    const placeholder1 = 0;
    const placeholder2 = 0;
    
    // Example TLS certificate (in practice, use your actual certificate)
    const certificate = new Uint8Array([
      1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
      21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38,
      39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56,
      57, 58, 59, 60, 61, 62, 63, 64, 65,
    ]);
    
    const tx = await neuronContract.serveAxonTls(
      netuid,
      version,
      ip,
      port,
      ipType,
      protocol,
      placeholder1,
      placeholder2,
      certificate
    );
    await tx.wait();
    
    console.log("Axon TLS endpoint configured successfully!");
    console.log("Transaction hash:", tx.hash);
  } catch (error) {
    console.error("Serving axon TLS failed:", error);
  }
}
```

#### Serve Prometheus Metrics

```javascript
async function servePrometheus() {
  try {
    const netuid = 1;
    const version = 1;
    const ip = 0x7f000001; // 127.0.0.1 in hex
    const port = 9090; // Prometheus default port
    const ipType = 4; // IPv4
    
    const tx = await neuronContract.servePrometheus(
      netuid,
      version,
      ip,
      port,
      ipType
    );
    await tx.wait();
    
    console.log("Prometheus endpoint configured successfully!");
    console.log("Transaction hash:", tx.hash);
  } catch (error) {
    console.error("Serving Prometheus failed:", error);
  }
}
```

### Complete Neuron Setup Example

```javascript
async function setupCompleteNeuron() {
  try {
    const netuid = 1;
    const hotkey = "0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef";
    
    // 1. Register the neuron
    console.log("Registering neuron...");
    await registerNeuron();
    
    // 2. Configure axon service
    console.log("Setting up axon service...");
    await serveAxon();
    
    // 3. Configure Prometheus metrics
    console.log("Setting up Prometheus metrics...");
    await servePrometheus();
    
    // 4. Set initial weights (if validator)
    console.log("Setting weights...");
    await setNeuronWeights();
    
    console.log("Neuron setup complete!");
    
  } catch (error) {
    console.error("Neuron setup failed:", error);
  }
}

// Run complete setup
setupCompleteNeuron();
```

### Error Handling and Best Practices

```javascript
async function robustNeuronOperation() {
  try {
    const netuid = 1;
    const dests = [1, 2, 3];
    const weights = [100, 200, 150];
    const versionKey = 0;
    
    // Always check gas estimates before executing
    const gasEstimate = await neuronContract.setWeights.estimateGas(
      netuid, dests, weights, versionKey
    );
    
    // Add buffer to gas limit
    const gasLimit = gasEstimate * 120n / 100n;
    
    const tx = await neuronContract.setWeights(
      netuid, dests, weights, versionKey,
      { gasLimit }
    );
    
    // Wait for confirmation with timeout
    const receipt = await tx.wait(1);
    
    if (receipt.status === 1) {
      console.log("Operation successful!");
    } else {
      console.error("Transaction failed");
    }
    
  } catch (error) {
    if (error.code === 'INSUFFICIENT_FUNDS') {
      console.error("Insufficient funds for transaction");
    } else if (error.code === 'NETWORK_ERROR') {
      console.error("Network connection issue");
    } else {
      console.error("Unexpected error:", error.message);
    }
  }
}
```

## Test code

https://github.com/opentensor/subtensor/blob/main/evm-tests/test/neuron.precompile.emission-check.test.ts
```
import * as assert from "assert";

import { getAliceSigner, getDevnetApi, getRandomSubstrateKeypair } from "../src/substrate"
import { getPublicClient, } from "../src/utils";
import { ETH_LOCAL_URL } from "../src/config";
import { devnet } from "@polkadot-api/descriptors"
import { PublicClient } from "viem";
import { PolkadotSigner, TypedApi } from "polkadot-api";
import { convertPublicKeyToSs58, } from "../src/address-utils"
import { ethers } from "ethers"
import { INEURON_ADDRESS, INeuronABI } from "../src/contracts/neuron"
import { generateRandomEthersWallet } from "../src/utils"
import { forceSetBalanceToSs58Address, forceSetBalanceToEthAddress, addNewSubnetwork, startCall, setSubtokenEnable } from "../src/subtensor"

describe("Test the Neuron precompile with emission", () => {
    // init eth part
    const wallet = generateRandomEthersWallet();

    // init substrate part
    const hotkey = getRandomSubstrateKeypair();
    const hotkey2 = getRandomSubstrateKeypair();
    const coldkey = getRandomSubstrateKeypair();
    let publicClient: PublicClient;

    let api: TypedApi<typeof devnet>

    // sudo account alice as signer
    let alice: PolkadotSigner;

    before(async () => {
        // init variables got from await and async
        publicClient = await getPublicClient(ETH_LOCAL_URL)
        api = await getDevnetApi()
        alice = await getAliceSigner();
        await forceSetBalanceToSs58Address(api, convertPublicKeyToSs58(hotkey.publicKey))
        await forceSetBalanceToSs58Address(api, convertPublicKeyToSs58(hotkey2.publicKey))

        await forceSetBalanceToSs58Address(api, convertPublicKeyToSs58(coldkey.publicKey))
        await forceSetBalanceToEthAddress(api, wallet.address)

        const netuid = await addNewSubnetwork(api, hotkey2, coldkey)
        await startCall(api, netuid, coldkey)
        console.log("test on subnet ", netuid)
    })

    it("Burned register and check emission", async () => {
        let netuid = (await api.query.SubtensorModule.TotalNetworks.getValue()) - 1
        
        const uid = await api.query.SubtensorModule.SubnetworkN.getValue(netuid)
        const contract = new ethers.Contract(INEURON_ADDRESS, INeuronABI, wallet);

        const tx = await contract.burnedRegister(
            netuid,
            hotkey.publicKey
        );
        await tx.wait();

        const uidAfterNew = await api.query.SubtensorModule.SubnetworkN.getValue(netuid)
        assert.equal(uid + 1, uidAfterNew)

        const key = await api.query.SubtensorModule.Keys.getValue(netuid, uid)
        assert.equal(key, convertPublicKeyToSs58(hotkey.publicKey))

        let i = 0;
        while (i < 10) {
            const emission = await api.query.SubtensorModule.PendingEmission.getValue(netuid)

            console.log("emission is ", emission);
            await new Promise((resolve) => setTimeout(resolve, 2000));
            i += 1;
        }
    })
});
```

https://github.com/opentensor/subtensor/blob/main/evm-tests/test/neuron.precompile.set-weights.test.ts
```
import * as assert from "assert";

import { getDevnetApi, getRandomSubstrateKeypair } from "../src/substrate"
import { devnet } from "@polkadot-api/descriptors"
import { TypedApi } from "polkadot-api";
import { convertH160ToSS58, convertPublicKeyToSs58, } from "../src/address-utils"
import { ethers } from "ethers"
import { INEURON_ADDRESS, INeuronABI } from "../src/contracts/neuron"
import { generateRandomEthersWallet } from "../src/utils"
import {
    forceSetBalanceToSs58Address, forceSetBalanceToEthAddress, addNewSubnetwork, burnedRegister, setCommitRevealWeightsEnabled,
    setWeightsSetRateLimit,
    startCall
} from "../src/subtensor"

describe("Test neuron precompile contract, set weights function", () => {
    // init eth part
    const wallet = generateRandomEthersWallet();

    // init substrate part
    const hotkey = getRandomSubstrateKeypair();
    const coldkey = getRandomSubstrateKeypair();

    let api: TypedApi<typeof devnet>

    before(async () => {
        api = await getDevnetApi()

        await forceSetBalanceToSs58Address(api, convertPublicKeyToSs58(hotkey.publicKey))

        await forceSetBalanceToSs58Address(api, convertPublicKeyToSs58(coldkey.publicKey))
        await forceSetBalanceToEthAddress(api, wallet.address)

        const netuid = await addNewSubnetwork(api, hotkey, coldkey)
        await startCall(api, netuid, coldkey)
        console.log("test on subnet ", netuid)

        await burnedRegister(api, netuid, convertH160ToSS58(wallet.address), coldkey)
        const uid = await api.query.SubtensorModule.Uids.getValue(netuid, convertH160ToSS58(wallet.address))
        assert.notEqual(uid, undefined)
        // disable reveal and enable direct set weights
        await setCommitRevealWeightsEnabled(api, netuid, false)
        await setWeightsSetRateLimit(api, netuid, BigInt(0))
    })

    it("Set weights is ok", async () => {
        let netuid = (await api.query.SubtensorModule.TotalNetworks.getValue()) - 1
        const uid = await api.query.SubtensorModule.Uids.getValue(netuid, convertH160ToSS58(wallet.address))

        const contract = new ethers.Contract(INEURON_ADDRESS, INeuronABI, wallet);
        const dests = [1];
        const weights = [2];
        const version_key = 0;

        const tx = await contract.setWeights(netuid, dests, weights, version_key);

        await tx.wait();
        if (uid === undefined) {
            throw new Error("uid not get on chain")
        } else {
            const weightsOnChain = await api.query.SubtensorModule.Weights.getValue(netuid, uid)

            weightsOnChain.forEach((weight, _) => {
                const uidInWeight = weight[0];
                const value = weight[1];
                assert.equal(uidInWeight, uid)
                assert.ok(value > 0)
            });
        }
    })
});
```

https://github.com/opentensor/subtensor/blob/main/evm-tests/test/neuron.precompile.serve.axon-prometheus.test.ts
```
import * as assert from "assert";
import { getAliceSigner, getDevnetApi, getRandomSubstrateKeypair } from "../src/substrate"
import { devnet } from "@polkadot-api/descriptors"
import { PolkadotSigner, TypedApi } from "polkadot-api";
import { convertPublicKeyToSs58, convertH160ToSS58 } from "../src/address-utils"
import { ethers } from "ethers"
import { INEURON_ADDRESS, INeuronABI } from "../src/contracts/neuron"
import { generateRandomEthersWallet } from "../src/utils"
import { forceSetBalanceToEthAddress, forceSetBalanceToSs58Address, addNewSubnetwork, burnedRegister, startCall } from "../src/subtensor"

describe("Test neuron precompile Serve Axon Prometheus", () => {
    // init eth part
    const wallet1 = generateRandomEthersWallet();
    const wallet2 = generateRandomEthersWallet();
    const wallet3 = generateRandomEthersWallet();

    // init substrate part
    const hotkey = getRandomSubstrateKeypair();
    const coldkey = getRandomSubstrateKeypair();

    let api: TypedApi<typeof devnet>

    // sudo account alice as signer
    let alice: PolkadotSigner;
    before(async () => {
        // init variables got from await and async
        api = await getDevnetApi()
        alice = await getAliceSigner();

        await forceSetBalanceToSs58Address(api, convertPublicKeyToSs58(alice.publicKey))
        await forceSetBalanceToSs58Address(api, convertPublicKeyToSs58(hotkey.publicKey))
        await forceSetBalanceToSs58Address(api, convertPublicKeyToSs58(coldkey.publicKey))
        await forceSetBalanceToEthAddress(api, wallet1.address)
        await forceSetBalanceToEthAddress(api, wallet2.address)
        await forceSetBalanceToEthAddress(api, wallet3.address)
        let netuid = await addNewSubnetwork(api, hotkey, coldkey)
        await startCall(api, netuid, coldkey)

        console.log("test the case on subnet ", netuid)

        await burnedRegister(api, netuid, convertH160ToSS58(wallet1.address), coldkey)
        await burnedRegister(api, netuid, convertH160ToSS58(wallet2.address), coldkey)
        await burnedRegister(api, netuid, convertH160ToSS58(wallet3.address), coldkey)
    })

    it("Serve Axon", async () => {
        let netuid = (await api.query.SubtensorModule.TotalNetworks.getValue()) - 1
        const version = 0;
        const ip = 1;
        const port = 2;
        const ipType = 4;
        const protocol = 0;
        const placeholder1 = 8;
        const placeholder2 = 9;

        const contract = new ethers.Contract(INEURON_ADDRESS, INeuronABI, wallet1);

        const tx = await contract.serveAxon(
            netuid,
            version,
            ip,
            port,
            ipType,
            protocol,
            placeholder1,
            placeholder2
        );
        await tx.wait();

        const axon = await api.query.SubtensorModule.Axons.getValue(
            netuid,
            convertH160ToSS58(wallet1.address)
        )
        assert.notEqual(axon?.block, undefined)
        assert.equal(axon?.version, version)
        assert.equal(axon?.ip, ip)
        assert.equal(axon?.port, port)
        assert.equal(axon?.ip_type, ipType)
        assert.equal(axon?.protocol, protocol)
        assert.equal(axon?.placeholder1, placeholder1)
        assert.equal(axon?.placeholder2, placeholder2)
    });

    it("Serve Axon TLS", async () => {
        let netuid = (await api.query.SubtensorModule.TotalNetworks.getValue()) - 1
        const version = 0;
        const ip = 1;
        const port = 2;
        const ipType = 4;
        const protocol = 0;
        const placeholder1 = 8;
        const placeholder2 = 9;
        // certificate length is 65
        const certificate = new Uint8Array([
            1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
            21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38,
            39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56,
            57, 58, 59, 60, 61, 62, 63, 64, 65,
        ]);

        const contract = new ethers.Contract(INEURON_ADDRESS, INeuronABI, wallet2);

        const tx = await contract.serveAxonTls(
            netuid,
            version,
            ip,
            port,
            ipType,
            protocol,
            placeholder1,
            placeholder2,
            certificate
        );
        await tx.wait();

        const axon = await api.query.SubtensorModule.Axons.getValue(
            netuid,
            convertH160ToSS58(wallet2.address))

        assert.notEqual(axon?.block, undefined)
        assert.equal(axon?.version, version)
        assert.equal(axon?.ip, ip)
        assert.equal(axon?.port, port)
        assert.equal(axon?.ip_type, ipType)
        assert.equal(axon?.protocol, protocol)
        assert.equal(axon?.placeholder1, placeholder1)
        assert.equal(axon?.placeholder2, placeholder2)
    });

    it("Serve Prometheus", async () => {
        let netuid = (await api.query.SubtensorModule.TotalNetworks.getValue()) - 1
        const version = 0;
        const ip = 1;
        const port = 2;
        const ipType = 4;

        const contract = new ethers.Contract(INEURON_ADDRESS, INeuronABI, wallet3);

        const tx = await contract.servePrometheus(
            netuid,
            version,
            ip,
            port,
            ipType
        );
        await tx.wait();

        const prometheus = (
            await api.query.SubtensorModule.Prometheus.getValue(
                netuid,
                convertH160ToSS58(wallet3.address)
            )
        )

        assert.notEqual(prometheus?.block, undefined)
        assert.equal(prometheus?.version, version)
        assert.equal(prometheus?.ip, ip)
        assert.equal(prometheus?.port, port)
        assert.equal(prometheus?.ip_type, ipType)
    });
});
```

https://github.com/opentensor/subtensor/blob/main/evm-tests/test/neuron.precompile.reveal-weights.test.ts
```
import * as assert from "assert";
import { getAliceSigner, getDevnetApi, getRandomSubstrateKeypair } from "../src/substrate"
import { devnet } from "@polkadot-api/descriptors"
import { PolkadotSigner, TypedApi } from "polkadot-api";
import { convertPublicKeyToSs58, convertH160ToSS58 } from "../src/address-utils"
import { Vec, Tuple, VecFixed, u16, u8, u64 } from "@polkadot/types-codec";
import { TypeRegistry } from "@polkadot/types";
import { ethers } from "ethers"
import { INEURON_ADDRESS, INeuronABI } from "../src/contracts/neuron"
import { generateRandomEthersWallet } from "../src/utils"
import { convertH160ToPublicKey } from "../src/address-utils"
import { blake2AsU8a } from "@polkadot/util-crypto"
import {
    forceSetBalanceToEthAddress, forceSetBalanceToSs58Address, addNewSubnetwork, setCommitRevealWeightsEnabled, setWeightsSetRateLimit, burnedRegister,
    setTempo, setCommitRevealWeightsInterval,
    startCall
} from "../src/subtensor"

// hardcode some values for reveal hash
const uids = [1];
const values = [5];
const salt = [9];
const version_key = 0;

function getCommitHash(netuid: number, address: string) {
    const registry = new TypeRegistry();
    let publicKey = convertH160ToPublicKey(address);

    const tupleData = new Tuple(
        registry,
        [
            VecFixed.with(u8, 32),
            u16,
            Vec.with(u16),
            Vec.with(u16),
            Vec.with(u16),
            u64,
        ],
        [publicKey, netuid, uids, values, salt, version_key]
    );

    const hash = blake2AsU8a(tupleData.toU8a());
    return hash;
}

describe("Test neuron precompile reveal weights", () => {
    // init eth part
    const wallet = generateRandomEthersWallet();

    // init substrate part
    const hotkey = getRandomSubstrateKeypair();
    const coldkey = getRandomSubstrateKeypair();

    let api: TypedApi<typeof devnet>

    // sudo account alice as signer
    let alice: PolkadotSigner;
    before(async () => {
        // init variables got from await and async
        api = await getDevnetApi()
        alice = await getAliceSigner();

        await forceSetBalanceToSs58Address(api, convertPublicKeyToSs58(alice.publicKey))
        await forceSetBalanceToSs58Address(api, convertPublicKeyToSs58(hotkey.publicKey))
        await forceSetBalanceToSs58Address(api, convertPublicKeyToSs58(coldkey.publicKey))
        await forceSetBalanceToEthAddress(api, wallet.address)
        let netuid = await addNewSubnetwork(api, hotkey, coldkey)
        await startCall(api, netuid, coldkey)

        console.log("test the case on subnet ", netuid)

        // enable commit reveal feature
        await setCommitRevealWeightsEnabled(api, netuid, true)
        // set it as 0, we can set the weight anytime
        await setWeightsSetRateLimit(api, netuid, BigInt(0))

        const ss58Address = convertH160ToSS58(wallet.address)
        await burnedRegister(api, netuid, ss58Address, coldkey)

        const uid = await api.query.SubtensorModule.Uids.getValue(
            netuid,
            ss58Address
        )
        // eth wallet account should be the first neuron in the subnet
        assert.equal(uid, uids[0])
    })

    it("EVM neuron commit weights via call precompile", async () => {
        let totalNetworks = await api.query.SubtensorModule.TotalNetworks.getValue()
        const subnetId = totalNetworks - 1
        const commitHash = getCommitHash(subnetId, wallet.address)
        const contract = new ethers.Contract(INEURON_ADDRESS, INeuronABI, wallet);
        const tx = await contract.commitWeights(subnetId, commitHash)
        await tx.wait()

        const ss58Address = convertH160ToSS58(wallet.address)

        const weightsCommit = await api.query.SubtensorModule.WeightCommits.getValue(subnetId, ss58Address)
        if (weightsCommit === undefined) {
            throw new Error("submit weights failed")
        }
        else { assert.ok(weightsCommit.length > 0) }
    })

    // Temporarily disable it, there is a type error in CI.
    it("EVM neuron reveal weights via call precompile", async () => {
        let totalNetworks = await api.query.SubtensorModule.TotalNetworks.getValue()
        const netuid = totalNetworks - 1
        const contract = new ethers.Contract(INEURON_ADDRESS, INeuronABI, wallet);
        // set tempo or epoch large, then enough time to reveal weight
        await setTempo(api, netuid, 60000)
        // set interval epoch as 0, we can reveal at the same epoch
        await setCommitRevealWeightsInterval(api, netuid, BigInt(0))

        const tx = await contract.revealWeights(
            netuid,
            uids,
            values,
            salt,
            version_key
        );
        await tx.wait()
        const ss58Address = convertH160ToSS58(wallet.address)

        // check the weight commit is removed after reveal successfully
        const weightsCommit = await api.query.SubtensorModule.WeightCommits.getValue(netuid, ss58Address)
        assert.equal(weightsCommit, undefined)

        // check the weight is set after reveal with correct uid
        const neuron_uid = await api.query.SubtensorModule.Uids.getValue(
            netuid,
            ss58Address
        )

        if (neuron_uid === undefined) {
            throw new Error("neuron_uid not available onchain or invalid type")
        }

        const weights = await api.query.SubtensorModule.Weights.getValue(netuid, neuron_uid)

        if (weights === undefined || !Array.isArray(weights)) {
            throw new Error("weights not available onchain or invalid type")
        }

        for (const weight of weights) {
            assert.equal(weight[0], neuron_uid)
            assert.ok(weight[1] !== undefined)
        }
    })
});
```







## Source Code
https://github.com/opentensor/subtensor/blob/main/precompiles/src/neuron.rs
```
use core::marker::PhantomData;

use frame_support::dispatch::{GetDispatchInfo, PostDispatchInfo};
use frame_system::RawOrigin;
use pallet_evm::{AddressMapping, PrecompileHandle};
use precompile_utils::{EvmResult, prelude::UnboundedBytes};
use sp_core::H256;
use sp_runtime::traits::Dispatchable;
use sp_std::vec::Vec;

use crate::{PrecompileExt, PrecompileHandleExt};

pub struct NeuronPrecompile<R>(PhantomData<R>);

impl<R> PrecompileExt<R::AccountId> for NeuronPrecompile<R>
where
    R: frame_system::Config + pallet_evm::Config + pallet_subtensor::Config,
    R::AccountId: From<[u8; 32]>,
    <R as frame_system::Config>::RuntimeCall: From<pallet_subtensor::Call<R>>
        + GetDispatchInfo
        + Dispatchable<PostInfo = PostDispatchInfo>,
    <R as pallet_evm::Config>::AddressMapping: AddressMapping<R::AccountId>,
{
    const INDEX: u64 = 2052;
}

#[precompile_utils::precompile]
impl<R> NeuronPrecompile<R>
where
    R: frame_system::Config + pallet_evm::Config + pallet_subtensor::Config,
    R::AccountId: From<[u8; 32]>,
    <R as frame_system::Config>::RuntimeCall: From<pallet_subtensor::Call<R>>
        + GetDispatchInfo
        + Dispatchable<PostInfo = PostDispatchInfo>,
    <R as pallet_evm::Config>::AddressMapping: AddressMapping<R::AccountId>,
{
    #[precompile::public("setWeights(uint16,uint16[],uint16[],uint64)")]
    #[precompile::payable]
    pub fn set_weights(
        handle: &mut impl PrecompileHandle,
        netuid: u16,
        dests: Vec<u16>,
        weights: Vec<u16>,
        version_key: u64,
    ) -> EvmResult<()> {
        let call = pallet_subtensor::Call::<R>::set_weights {
            netuid,
            dests,
            weights,
            version_key,
        };

        handle.try_dispatch_runtime_call::<R, _>(
            call,
            RawOrigin::Signed(handle.caller_account_id::<R>()),
        )
    }

    #[precompile::public("commitWeights(uint16,bytes32)")]
    #[precompile::payable]
    pub fn commit_weights(
        handle: &mut impl PrecompileHandle,
        netuid: u16,
        commit_hash: H256,
    ) -> EvmResult<()> {
        let call = pallet_subtensor::Call::<R>::commit_weights {
            netuid,
            commit_hash,
        };

        handle.try_dispatch_runtime_call::<R, _>(
            call,
            RawOrigin::Signed(handle.caller_account_id::<R>()),
        )
    }

    #[precompile::public("revealWeights(uint16,uint16[],uint16[],uint16[],uint64)")]
    #[precompile::payable]
    pub fn reveal_weights(
        handle: &mut impl PrecompileHandle,
        netuid: u16,
        uids: Vec<u16>,
        values: Vec<u16>,
        salt: Vec<u16>,
        version_key: u64,
    ) -> EvmResult<()> {
        let call = pallet_subtensor::Call::<R>::reveal_weights {
            netuid,
            uids,
            values,
            salt,
            version_key,
        };

        handle.try_dispatch_runtime_call::<R, _>(
            call,
            RawOrigin::Signed(handle.caller_account_id::<R>()),
        )
    }

    #[precompile::public("burnedRegister(uint16,bytes32)")]
    #[precompile::payable]
    fn burned_register(
        handle: &mut impl PrecompileHandle,
        netuid: u16,
        hotkey: H256,
    ) -> EvmResult<()> {
        let coldkey = handle.caller_account_id::<R>();
        let hotkey = R::AccountId::from(hotkey.0);
        let call = pallet_subtensor::Call::<R>::burned_register { netuid, hotkey };

        handle.try_dispatch_runtime_call::<R, _>(call, RawOrigin::Signed(coldkey))
    }

    #[precompile::public("serveAxon(uint16,uint32,uint128,uint16,uint8,uint8,uint8,uint8)")]
    #[precompile::payable]
    #[allow(clippy::too_many_arguments)]
    fn serve_axon(
        handle: &mut impl PrecompileHandle,
        netuid: u16,
        version: u32,
        ip: u128,
        port: u16,
        ip_type: u8,
        protocol: u8,
        placeholder1: u8,
        placeholder2: u8,
    ) -> EvmResult<()> {
        let call = pallet_subtensor::Call::<R>::serve_axon {
            netuid,
            version,
            ip,
            port,
            ip_type,
            protocol,
            placeholder1,
            placeholder2,
        };

        handle.try_dispatch_runtime_call::<R, _>(
            call,
            RawOrigin::Signed(handle.caller_account_id::<R>()),
        )
    }

    #[precompile::public(
        "serveAxonTls(uint16,uint32,uint128,uint16,uint8,uint8,uint8,uint8,bytes)"
    )]
    #[precompile::payable]
    #[allow(clippy::too_many_arguments)]
    fn serve_axon_tls(
        handle: &mut impl PrecompileHandle,
        netuid: u16,
        version: u32,
        ip: u128,
        port: u16,
        ip_type: u8,
        protocol: u8,
        placeholder1: u8,
        placeholder2: u8,
        certificate: UnboundedBytes,
    ) -> EvmResult<()> {
        let call = pallet_subtensor::Call::<R>::serve_axon_tls {
            netuid,
            version,
            ip,
            port,
            ip_type,
            protocol,
            placeholder1,
            placeholder2,
            certificate: certificate.into(),
        };

        handle.try_dispatch_runtime_call::<R, _>(
            call,
            RawOrigin::Signed(handle.caller_account_id::<R>()),
        )
    }

    #[precompile::public("servePrometheus(uint16,uint32,uint128,uint16,uint8)")]
    #[precompile::payable]
    #[allow(clippy::too_many_arguments)]
    fn serve_prometheus(
        handle: &mut impl PrecompileHandle,
        netuid: u16,
        version: u32,
        ip: u128,
        port: u16,
        ip_type: u8,
    ) -> EvmResult<()> {
        let call = pallet_subtensor::Call::<R>::serve_prometheus {
            netuid,
            version,
            ip,
            port,
            ip_type,
        };

        handle.try_dispatch_runtime_call::<R, _>(
            call,
            RawOrigin::Signed(handle.caller_account_id::<R>()),
        )
    }
}