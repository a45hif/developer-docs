---
title: "Configuring Hardhat"
---

import ThemedImage from '@theme/ThemedImage';
import useBaseUrl from '@docusaurus/useBaseUrl';

# Configuring Hardhat

You can use [Hardhat](https://hardhat.org/) development environment for the EVM feature on subtensor. The Hardhat networks can be configured using the `hardhat.config.ts` file, as shown below. 

The below code configures two subtensor EVM networks for Hardhat: 

1. EVM Localnet with URL: http://127.0.0.1:9944
2. EVM Testnet with URL: https://test.chain.opentensor.ai
3. EVM Mainnet with URL: https://lite.chain.opentensor.ai
4. EVM Version **Cancun** that matches **Solidity 0.8.24**.

:::tip Full example
See [ERC-20 Example Token repository](https://github.com/gztensor/subtensor-erc20) for a complete example of `hardhat.config.ts` configuration.
:::

```js title="Partial snippet of hardhat.config.ts file"
const hardhatConfig: HardhatUserConfig = {
  solidity: "0.8.24",
  defaultNetwork: "subevm",
  networks: {
    subevm: {
      url: "https://test.chain.opentensor.ai",
      accounts: [config.ethPrivateKey]
    },
    mainnet: {
      url: "https://lite.chain.opentensor.ai",
      accounts: [config.ethPrivateKey]
    },
    local: {
      url: "http://127.0.0.1:9944",
      accounts: [config.ethPrivateKey]
    }
  },
  mocha: {
    timeout: 300000
  },
};
```
