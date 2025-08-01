---
title: "Dynamic TAO FAQ"
---

import ThemedImage from '@theme/ThemedImage';
import useBaseUrl from '@docusaurus/useBaseUrl';

## General

### Will there be a cap on alpha currency?

Yes. There is a hard cap of 21 million for any subnet's alpha token, the same as for TAO itself. Alpha tokens follow a halving schedule as well.

At the time of writing, 2 alpha tokens per subnet will be emitted each block, while only 1 TAO is emitted and shared across the whole network.

## TAO-holders / Stakers

### How has staking changed?

Instead of staking TAO to a validator, in Dynamic TAO, you stake to a validator on a specific subnet. This can be either a mining subnet (most subnets) or the unique root subnet, a.k.a. Subnet Zero.

- When you stake on a mining subnet, you exchange TAO for a dynamic token, the _alpha_ of the subnet on which the validator is working, and stake that into the validator's hotkey.

- When you stake on the root subnet, you stake TAO for TAO. Your emissions are TAO.

### What is the risk/reward profile of staking into a subnet?

Each new subnet has its own token, referred to as its alpha. When you stake into a validator within a given subnet, you exchange TAO for that subnet's alpha. When you unstake from the validator in that subnet, you exchange the alpha for TAO. Staking and unstaking is therefore sensitive to the price of the alpha. This price of a subnet's alpha is the ratio of TAO in its reserve to alpha in reserve.

Staking TAO into a subnet essentially exchanges TAO for that subnet’s alpha token. To exit value, alpha must be exchanged back for TAO at the going rate.

Held stake (alpha tokens) may increase or decrease in TAO value as the price of the alpha changes.

### How do emissions to root subnet/Subnet 0 stakers work?

**Network-wide Impact**: Your stake contributes weight across all subnets where your validator operates. This means your stake extracts emissions from multiple subnets simultaneously. See [Validator stake weight](../subnets/understanding-subnets.md#validator-stake-weight) for more details.

**Proportional emission and TAO weight**: TAO and alpha are emitted to a validator's stakers in proportion to the validators' holdings in each token. See [Emission: Extraction](../emissions.md#extraction)

### Can users transfer alpha tokens (subnet tokens)?

It is up to the subnet creator, and is configured using the `TransferToggle` hyperparameter.

When enabled, a holder of alpha stake can transfer its ownership to another coldkey/wallet using [`btcli stake transfer`](../staking-and-delegation/managing-stake-btcli#transferring-stake) or [`transfer_stake`](pathname:///python-api/html/autoapi/bittensor/core/async_subtensor/index.html#bittensor.core.async_subtensor.AsyncSubtensor.transfer_stake).

### How will Dynamic TAO affect governance of the network?

Dynamic TAO does not directly change Bittensor's on-chain governance mechanism (i.e., proposals and voting).

## Subnets

### Root Subnet/Subnet Zero

In Dynamic TAO, Subnet Zero is a special subnet. It is the only subnet that does not have its own $\alpha$ currency. No miners can register on subnet zero, and no validation work is performed. However validators can register, and $\tau$-holders can stake to those validators, as with any other subnet. This offers a mechanism for $\tau$-holders to stake $\tau$ into validators in a subnet-agnostic way. This works because the weight of a validator in a subnet includes both their share of that subnet's $\alpha$ and their share of staked TAO in Subnet Zero.

Subnet Zero is sometimes called the root subnet, since it sort of replaces the root network in the pre-Dyanmic-TAO architecture. However, Subnet Zero does not perform consensus over subnets, which was the defining function of the root network.

### What will it take to start and manage a subnet in Dyanmic TAO?

The process of registering a subnet in Dynamic TAO will be very similar to the process of registering a submit previously, except that the cost to register the subnet is now burned, rather than being a lock cost returned to the subnet creator on de-registration. This is because subnets are not deregistered in Dynamic TAO.

### What is the cost of creating a subnet?

Subnet registration cost is dynamic. It doubles when a subnet is registered, and decreases at a slow rate such that the price halves after 38,880 blocks&mdash;roughly five and a half days. This implies that, if the demand for new subnets is steady, one should be created roughly every five and a half days.

### How will Dynamic TAO affect subnet governance (weight-setting)?

Each validator’s weight in the subnet is a function of the alpha staked to them on the subnet, plus the TAO staked to them in Subnet Zero, with the value of the TAO being multiplied by the TAO weight, which is between 0 and 1.

See [validator stake weight](../subnets/understanding-subnets.md#validator-stake-weight).

### What happens when a subnet is abandoned?

If no participants use or mine a subnet, its token will likely drop to negligible value. Other subnets and the root remain unaffected. Each subnet’s success or failure is largely self-contained.

:::Note
Currently, the protocol does not automatically deregister subnets. Abandoned subnets may be revived.
:::

### Do subnet creators control emissions for their own tokens?

**No**. Emissions are calculated by protocol logic (e.g., in `run_coinbase.rs`) and are based on network-wide parameters. Subnet founders cannot arbitrarily print tokens&mdash;emission follows the same consistent rules across all subnets.

See [Emissions](../emissions.md)

### What happens to previously locked registration costs from pre-Dynamic-TAO subnets?

They are returned to subnet creators when Dynamic TAO is initiated, on the same coldkey that registered.

## Miners and Validators

### How will miners (and validators) manage the proliferation of subnets?

Miners and validators must now consider the TAO value of the alpha token they are mining.

Miners can and must shift their work among subnets, depending on the value of the subnets and their own ability to compete. More subnets will mean more opportunities for specialized work.

Miners/validators may need to watch markets (token prices, volumes) to optimize their allocations, much as proof-of-work miners in other crypto systems monitor different chains to see which is most profitable to mine.

## Where can I find more technical details right now?

- Codebase: Refer to the Bittensor codebase, especially `run_coinbase.rs`, which calculates emissions logic for subnets and the root network.
- The [Dynamic TAO White Paper](https://drive.google.com/file/d/1vkuxOFPJyUyoY6dQzfIWwZm2_XL3AEOx/view)
