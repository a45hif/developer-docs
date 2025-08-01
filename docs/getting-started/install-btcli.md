---
title: "Install BTCLI"
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Install BTCLI

This page contains installation details for `btcli`, the Bittensor CLI.

## Prerequisite

To install `btcli`, you must have Python version 3.9-3.12. See config file on [GitHub](https://github.com/opentensor/btcli/blob/main/pyproject.toml#L57-L60).

## Developer reference

For a full developer reference, see the [Bittensor CLI reference document](../btcli.md).

## Install on macOS and Linux

You can install the Bittensor CLI on macOS and Linux using any of the following methods:

<Tabs>
  <TabItem value="pypi" label="Python Package Indexer" default>

Check for the latest release at the Python Package Index: [https://pypi.org/project/bittensor-cli/](https://pypi.org/project/bittensor-cli/).

Use pip to install the desired version:

```shell
pip install bittensor-cli # Use latest or desired version
```

Verify your installation and its version by running:

```shell
btcli --version
```

Example output:

```console
BTCLI version: 9.2.0
```

:::warning Update frequently!
Check frequently to make sure you are using the latest version of `btcli`.
:::
</TabItem>
<TabItem value="homebrew" label="Homebrew">
To install the Bittensor CLI using Homebrew, run the following command in your terminal:

```shell
brew install btcli
```

Next, verify your installation and its version by running:

```shell
btcli --version
```

:::warning Update frequently!
Check frequently to make sure you are using the latest version of `btcli`.
:::

</TabItem>
<TabItem value="source" label="Install from source">

1. Create and activate a virtual environment.
   :::tip Create and activate a virtual environment

   - Create Python virtual environment. Follow [this guide on python.org](https://docs.python.org/3/library/venv.html#creating-virtual-environments).

   - Activate the new environment. Follow [this guide on python.org](https://docs.python.org/3/library/venv.html#how-venvs-work)
     :::
     :::warning For Ubuntu-Linux users
     If you are using Ubuntu-Linux, the script will prompt for `sudo` access to install all required apt-get packages.
     :::

   ```bash
   python3 -m venv btcli_venv
   source btcli_venv/bin/activate
   ```

2. Clone the Bittensor CLI repo.

   ```bash
   git clone https://github.com/opentensor/btcli.git
   ```

3. `cd` into `btcli` directory.

   ```bash
   cd btcli
   ```

4. Install

   ```bash
   pip3 install .
   ```

</TabItem>
   </Tabs>

## Install on Windows

To install and run Bittensor SDK on Windows you must install [**WSL 2** (Windows Subsystem for Linux)](https://learn.microsoft.com/en-us/windows/wsl/about) on Windows and select [Ubuntu Linux distribution](https://github.com/ubuntu/WSL/blob/main/docs/guides/install-ubuntu-wsl2.md).

After you installed the above, follow the same installation steps described above in [Install on macOS and Linux](#install-on-macos-and-linux).

:::danger Limited support on Windows
While wallet transactions like delegating, transfer, registering, staking can be performed on a Windows machine using WSL 2, the mining and validating operations are not recommended and are not supported on Windows machines.
:::

## Verify the installation

```bash
btcli --version
```

which will give you the below output:

```bash
BTCLI version: <version number>
```

You will see the version number you installed in place of `<version number>`.

## Configuration

You can set the commonly used values, such as your hotkey and coldkey names, the default chain URL or the network name you use, and more, in `config.yml`. You can override these values by explicitly passing them in the command line for any `btcli` command.

### Example config file

The default location of the config file is: `~/.bittensor/config.yml`. An example of a `config.yml` is shown below:

```yaml
chain: ws://127.0.0.1:9945
network: local
no_cache: False
wallet_hotkey: hotkey-user1
wallet_name: coldkey-user1
wallet_path: ~/.bittensor/wallets
metagraph_cols:
  ACTIVE: true
  AXON: true
  COLDKEY: true
  CONSENSUS: true
  DIVIDENDS: true
  EMISSION: true
  GLOBAL_STAKE: true
  HOTKEY: true
  INCENTIVE: true
  LOCAL_STAKE: true
  RANK: true
  STAKE_WEIGHT: true
  TRUST: true
  UID: true
  UPDATED: true
  VAL: true
  VTRUST: true
```

:::caution alert
If both `chain` and `network` config values are present in the `config.yml`, then `chain` has the higher precedence. The the `btcli` command uses the `chain` value.
:::

**For more help:**

```bash
btcli config --help
```
