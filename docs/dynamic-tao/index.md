---
title: "Dynamic TAO"
---

import { HiOutlineCommandLine } from "react-icons/hi2";
import { HiAcademicCap } from "react-icons/hi2";

# Dynamic TAO

Dynamic TAO is a recent major evolution of Bittensor's integrated tokenomic and governance model, representing a significant step in Bittensor's trajectory toward more thorough decentralization.

It was introduced by proposal, approved by senate vote, and introduced as an upgrade to Bittensor main network on February 13, 2025 after a year of research, development, and testing.

See the [Dynamic TAO White Paper](https://drive.google.com/file/d/1vkuxOFPJyUyoY6dQzfIWwZm2_XL3AEOx/view) for a full explanation.

## What to expect with Dynamic TAO

Most operations will remain unchanged, including the main workflows for miners (e.g., registering on subnets) and validators (e.g., setting weights on miners).
Simply update the Bittensor SDK and/or `btcli`, and you will be prepared to work with the Dynamic TAO-enabled Bittensor test network.

:::danger
The migration to Dynamic TAO includes breaking changes. Older versions of the SDK and `btcli` are not compatible with Dynamic TAO. If a participant on your subnet does not upgrade their tooling, they will fall out of consensus.

The changes to `btcli` and the Bittensor SDK are not backwards compatible.
:::

## Using Dynamic TAO

To use Dynamic TAO, make sure you upgrade to the most recent stable versions of the Bittensor SDK and `btcli`.

See:

- [Bittensor SDK release page](https://pypi.org/project/bittensor/)
- [Bittensor CLI release page](https://pypi.org/project/bittensor-cli/)
- [Upgrade the Bittensor SDK](../getting-started/installation.md#upgrade)

### Subnet tokens/liquidity pools

The most visible difference introduced with Dynamic TAO is the addition of one new token per subnet in the Bittensor network.

Run `btcli subnet list` to view information about the subnets and their currency reserves:

For example:

```txt
                                                                Subnets
                                                               Network: rao


        ┃               ┃ Price       ┃ Market Cap  ┃              ┃                         ┃               ┃              ┃
 Netuid ┃ Name          ┃ (τ_in/α_in) ┃ (α * Price) ┃ Emission (τ) ┃ P (τ_in, α_in)          ┃ Stake (α_out) ┃ Supply (α)   ┃ Tempo (k/n)
━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━
   0    │ τ root        │ 1.00 τ/Τ    │ τ 5.93m     │ τ 0.0000     │ -, -                    │ Τ 5.93m       │ 5.93m Τ /21M │ -/-
   3    │ γ templar     │ 0.02 τ/γ    │ τ 57.32     │ τ 0.0197     │ τ 31.44, 1.43k γ        │ 1.18k γ       │ 2.61k γ /21M │ 67/99
   9    │ ι pretrain    │ 0.02 τ/ι    │ τ 55.38     │ τ 0.0194     │ τ 30.91, 1.46k ι        │ 1.16k ι       │ 2.61k ι /21M │ 73/99
   1    │ α apex        │ 0.02 τ/α    │ τ 54.45     │ τ 0.0192     │ τ 30.65, 1.47k α        │ 1.14k α       │ 2.61k α /21M │ 65/99
   2    │ β omron       │ 0.02 τ/β    │ τ 54.45     │ τ 0.0192     │ τ 30.65, 1.47k β        │ 1.14k β       │ 2.61k β /21M │ 66/99
   4    │ δ targon      │ 0.02 τ/δ    │ τ 54.45     │ τ 0.0192     │ τ 30.65, 1.47k δ        │ 1.14k δ       │ 2.61k δ /21M │ 68/99
   ...
```

### Gradual impact on consensus dynamics

The rollout of Dynamic TAO is calculated to have a gradual impact. When Dynamic TAO is first released, the weight of all validators (in terms of stake) will remain unchanged, because a biasing variable known as _TAO weight_, which controls the relative weight of TAO and alpha currencies, will heavily favor TAO&mdash;which currently has 100% weight since alpha currencies don't exist. Over time (an estimated 100 days), this _TAO Weight_ will shift to favor alpha currencies over TAO.
