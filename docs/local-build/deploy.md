---
title: "Build and Deploy the Blockchain"
toc_max_heading_level: 2
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';
import Heading from '@theme/Heading';

# Deploy a Local Bittensor Blockchain Instance

This tutorial will guide the user through deploying a local instance of Subtensor, Bittensor's L1 blockchain. This is useful in general Bittensor development, as it gives you more freedom over chain state than when working against mainnet or even testnet. For example, it is much easier to create subnets without having to wait for registration availability.

Each local chain is provisioned with an `alice` account with one million $\tau$.

In the following tutorial, we will also provision several wallets to serve as subnet creator, miner, and validator.

<Tabs queryString="local-chain">
<TabItem value="docker" label="Using Docker (Recommended)">
Docker is the easiest way to set up a local Bittensor blockchain instance. It only takes a few minutes to get up and running with Docker.

The steps in this guide assume that you are running the command from the machine you intend to host from.

### Prerequisites

Before you begin, make sure you have installed the following on your machine:

- [Docker](https://docs.docker.com/desktop/use-desktop/)
- [Bittensor SDK](../getting-started/installation.md)
- [Bittensor CLI](../getting-started/install-btcli.md)

The Bittensor SDK and Bittensor CLI are required to interact with the local blockchain instance.

### 1. Pull the Docker image

You can pull the official subtensor Docker image used to create the local blockchain instance from the [GitHub Container Repository](ghcr.io/opentensor/subtensor-localnet). To do this, run the following command in your terminal:

```bash
docker pull ghcr.io/opentensor/subtensor-localnet:devnet-ready
```

This command downloads the `subtensor-localnet` Docker image, making it available on your device.

### 2. Run the container

There are many ways to run the `subtensor-localnet` Docker image, depending on your development and testing needs. The two most common approaches involve running the chain with either _fast blocks_ or _non-fast blocks_. Each approach offers different trade-offs in speed, realism, and network behavior.
Below are examples of how to run the container using each mode:

- Fast blocks: Fast block mode reduces block processing time to _250ms per block_, enabling rapid chain progression. It allows faster feedback cycles for operations such as staking, subnet creation, and registration, making them ideal for local testing scenarios. To run the container in fast block mode, run the following command in your terminal:

  ```bash
  docker run --rm --name test_local_chain_ -p 9944:9944 -p 9945:9945 ghcr.io/opentensor/subtensor-localnet:devnet-ready
  ```

- Non-fast blocks: Non-fast block mode uses the default _12-second block time_, aligning with subtensor block intervals. While this mode utilizes the default block processing time, it also incorporates some enhancements—for example, subnets become eligible to start one minute after creation. To run the container in non-fast block mode, run the following command in your terminal:

  ```bash
  docker run --rm --name test_local_chain_ -p 9944:9944 -p 9945:9945 ghcr.io/opentensor/subtensor-localnet:devnet-ready False
  ```

### 3. Verify your setup

You can verify your local blockchain instance by checking the list of subnets available on your local blockchain. To do this, run the following command in the terminal:

```bash
btcli subnet list --network ws://127.0.0.1:9944
```

If the local blockchain is running correctly, you should see the following output:

```console
                                                           Subnets
                                                         Network: custom


        ┃        ┃ Price       ┃ Market Cap  ┃              ┃                        ┃               ┃              ┃
 Netuid ┃ Name   ┃ (τ_in/α_in) ┃ (α * Price) ┃ Emission (τ) ┃ P (τ_in, α_in)         ┃ Stake (α_out) ┃ Supply (α)   ┃ Tempo (k/n)
━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━
   0    │ τ root │ 1.0000 τ/Τ  │ τ 0.00      │ τ 0.0000     │ -, -                   │ Τ 0.00        │ 0.00 Τ /21M  │ -/-
   1    │ α apex │ 1.0000 τ/α  │ τ 11.00     │ τ 0.0000     │ τ 10.00, 10.00 α       │ 1.00 α        │ 11.00 α /21M │ 77/100
────────┼────────┼─────────────┼─────────────┼──────────────┼────────────────────────┼───────────────┼──────────────┼─────────────
   2    │        │ τ 1.0       │             │ τ 0.0        │ τ 10.00/175.00 (5.71%) │               │              │

```

</TabItem>
<TabItem value="local" label="Running a local build">

### Prerequisites

- Update your Mac or Linux workstation using your package manager
- Install [Bittensor SDK](../getting-started/installation) and [BTCLI](../getting-started/install-btcli)

### Build your local Subtensor

#### Install Rust/Cargo

To run locally, Substrate requires an up-to-date install of Cargo and Rust

Install from Rust's website:

```shell
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

Update your shell's source to include Cargo's path by running the following command:

```shell
. "$HOME/.cargo/env"
```

#### Clone and tweak the Subtensor source

We will clone the source and make a small modification to the state configuration with which the chain is deployed.

Normally, the creation of new subnets is limited to one per day. This is inconvenient for local subnet development, so we will limit this restriction.

1. Fetch the subtensor codebase to your local machine.

   ```bash
   git clone https://github.com/opentensor/subtensor.git
   ```

2. Open the source file `subtensor/runtime/src/lib.rs` in the your editor of choice, and find where the variable `SubtensorInitialNetworkRateLimit` is set. It is normally configured to `7200`, which is the number of blocks per day written to the chain, i.e. the seconds in a day divided by 12, since a Subtensor block is written every twelve seconds.

   In otherwords, this setting limits the number of new subnets that can be created to one per day.

3. Change the value of this variable to `1`, so we can create a new subnet every 12 seconds if we want to.

#### Setup Rust

This step ensures that you have the nightly toolchain and the WebAssembly (wasm) compilation target. Note that this step will run the Subtensor chain on your terminal directly, hence we advise that you run this as a background process using PM2 or other software.

Update to the nightly version of Rust:

```bash
./subtensor/scripts/init.sh
```

#### Build

These steps initialize your local subtensor chain in development mode. These commands will set up and run a local subtensor.

Build the binary:

```bash
cd subtensor
cargo build -p node-subtensor --profile release
```

#### Run

Next, run the localnet script and turn off the attempt to build the binary (as we have already done this above):

```bash
BUILD_BINARY=0 ./scripts/localnet.sh
```

:::info troubleshooting
If you see errors to the effect that the release cannot be found in `targets/fast-blocks`, you may need to move the build artifacts from `targets/release` to `targets/fast-blocks/release`.
:::

### Validate

Ensure your local chain is working by checking the list of subnets.

Note the use of the `--chain_endpoint` flag to target the local chain, rather than, say, test network

```shell
 btcli subnet list --network ws://127.0.0.1:9945
 btcli subnet list --network test
```

```console
                                                           Subnets
                                                         Network: custom


        ┃        ┃ Price       ┃ Market Cap  ┃              ┃                        ┃               ┃              ┃
 Netuid ┃ Name   ┃ (τ_in/α_in) ┃ (α * Price) ┃ Emission (τ) ┃ P (τ_in, α_in)         ┃ Stake (α_out) ┃ Supply (α)   ┃ Tempo (k/n)
━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━
   0    │ τ root │ 1.0000 τ/Τ  │ τ 0.00      │ τ 0.0000     │ -, -                   │ Τ 0.00        │ 0.00 Τ /21M  │ -/-
   1    │ α apex │ 1.0000 τ/α  │ τ 11.00     │ τ 0.0000     │ τ 10.00, 10.00 α       │ 1.00 α        │ 11.00 α /21M │ 77/100
────────┼────────┼─────────────┼─────────────┼──────────────┼────────────────────────┼───────────────┼──────────────┼─────────────
   2    │        │ τ 1.0       │             │ τ 0.0        │ τ 10.00/175.00 (5.71%) │               │              │

```

```shell

```

```console

                                                                        Subnets
                                                                     Network: test


        ┃                        ┃ Price        ┃ Market Cap  ┃              ┃                          ┃               ┃                 ┃
 Netuid ┃ Name                   ┃ (τ_in/α_in)  ┃ (α * Price) ┃ Emission (τ) ┃ P (τ_in, α_in)           ┃ Stake (α_out) ┃ Supply (α)      ┃ Tempo (k/n)
━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━
   0    │ τ root                 │ 1.0000 τ/Τ   │ τ 5.01m     │ τ 0.0000     │ -, -                     │ Τ 3.10m       │ 5.01m Τ /21M    │ -/-
  277   │ इ muv                  │ 0.4008 τ/इ   │ τ 536.06k   │ τ 0.4154     │ τ 199.85k, 498.63k इ     │ 838.83k इ     │ 1.34m इ /21M    │ 39/99
   3    │ γ templar              │ 0.1534 τ/γ   │ τ 219.03k   │ τ 0.1690     │ τ 110.74k, 722.13k γ     │ 706.14k γ     │ 1.43m γ /21M    │ 65/99
  119   │ Ⲃ vida                 │ 0.0748 τ/Ⲃ   │ τ 94.83k    │ τ 0.1321     │ τ 44.77k, 598.65k Ⲃ      │ 669.45k Ⲃ     │ 1.27m Ⲃ /21M    │ 81/99
   1    │ α apex                 │ 0.0587 τ/α   │ τ 70.03k    │ τ 0.0405     │ τ 30.27k, 515.71k α      │ 677.20k α     │ 1.19m α /21M    │ 63/99
   13   │ ν dataverse            │ 0.0467 τ/ν   │ τ 63.12k    │ τ 0.0645     │ τ 26.93k, 576.17k ν      │ 774.11k ν     │ 1.35m ν /21M    │ 75/99
  255   │ ዉ ethiopic_wu          │ 0.0181 τ/ዉ   │ τ 21.94k    │ τ 0.0133     │ τ 10.72k, 592.40k ዉ      │ 619.73k ዉ     │ 1.21m ዉ /21M    │ 17/99

...
```

</TabItem>
</Tabs>
