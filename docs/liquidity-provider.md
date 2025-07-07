---
title: Provisioning Liquidity to Subnets
---

# Provisioning Liquidity to Subnets

## Overview

The Liquidity Provider (LP) feature allows users to become providers of trading liquidity for specific subnets, within specified price ranges for the subnet $\alpha$ token. This system is based on Uniswap V3's concentrated liquidity model and enables users to earn fees from trading activity.

### Key Concepts

#### Liquidity Positions
A liquidity position represents a user's contribution to a trading pool within a specific price range. Each position has:
- **Price Range**: Defined by `price_low` and `price_high` in TAO
- **Liquidity Amount**: The total liquidity provided (in RAO)
- **Position ID**: Unique identifier for the position
- **Fee Tracking**: Separate tracking for TAO and Alpha fees earned

#### Price Ranges and Ticks
The system uses a tick-based pricing mechanism based on Uniswap V3:
- **Ticks**: Discrete price points with 0.01% spacing (PRICE_STEP = 1.0001)
- **Price Range**: Each position covers a range of ticks
- **Concentrated Liquidity**: Liquidity is only active within the specified range

### Use case

#### For TAO holders
- Provide liquidity in expected price ranges
- Earn fees from trading activity
- Participate in market making

#### For subnet creators
- Enable user liquidity provision
- Increase trading volume and liquidity
- Improve price discovery

:::note
Subnet creators can enable and disable user liquidity provision via the `toggle_user_liquidity` function.
:::

[See source code](https://github.com/opentensor/bittensor/blob/staging/bittensor/core/extrinsics/asyncex/liquidity.py#L187-L232)


## Tokenomics

### Fees

Liquidity providers earn fees from trading activity within their price range: 

- **TAO Fees**: Fees earned in TAO tokens
- **Alpha Fees**: Fees earned in Alpha tokens
- **Fee Distribution**: Proportional to liquidity provided and trading volume

The `calculate_fees()` function calculates both TAO and Alpha fees based on global fee data and position liquidity.

[See source code](https://github.com/opentensor/bittensor/blob/staging/bittensor/utils/liquidity.py#L130-L158)

### Dynamic token composition

A liquidity position (LP) can hold TAO, alpha, or both. This depends on the subnet's current token price relative to the range specified for the LP when it was created.

**Price Below Range** (`current_price < price_low`):
   - Position becomes **100% Alpha tokens**
   - `amount_alpha = liquidity * (1/sqrt_price_low - 1/sqrt_price_high)`
   - `amount_tao = 0`

**Price Above Range** (`current_price > price_high`):
   - Position becomes **100% TAO tokens**
   - `amount_alpha = 0`
   - `amount_tao = liquidity * (sqrt_price_high - sqrt_price_low)`

**Price Within Range** (`price_low <= current_price <= price_high`):
   - Position maintains **mixed token composition**
   - `amount_alpha = liquidity * (1/sqrt_current_price - 1/sqrt_price_high)`
   - `amount_tao = liquidity * (sqrt_current_price - sqrt_price_low)`

<details>
  <summary>See how it's computed</summary>

The `LiquidityPosition.to_token_amounts()` method shows how token composition changes based on current price vs. range boundaries.

```python
def to_token_amounts(
        self, current_subnet_price: Balance
    ) -> tuple[Balance, Balance]:
    sqrt_price_low = math.sqrt(self.price_low)
    sqrt_price_high = math.sqrt(self.price_high)
    sqrt_current_subnet_price = math.sqrt(current_subnet_price)

    if sqrt_current_subnet_price < sqrt_price_low:
        amount_alpha = self.liquidity * (1 / sqrt_price_low - 1 / sqrt_price_high)
        amount_tao = 0
    elif sqrt_current_subnet_price > sqrt_price_high:
        amount_alpha = 0
        amount_tao = self.liquidity * (sqrt_price_high - sqrt_price_low)
    else:
        amount_alpha = self.liquidity * (
            1 / sqrt_current_subnet_price - 1 / sqrt_price_high
        )
        amount_tao = self.liquidity * (sqrt_current_subnet_price - sqrt_price_low)
    return Balance.from_rao(int(amount_alpha), self.netuid), Balance.from_rao(
        int(amount_tao)
    )

```
[See source code](https://github.com/opentensor/bittensor/blob/staging/bittensor/utils/liquidity.py#L28-L58)
</details>


### Price Range Considerations
- **Narrow Ranges**: Higher fee concentration but more likely to become single-token when price moves
- **Wide Ranges**: Lower fee concentration but more likely to maintain mixed token composition

## Liquidity Positions vs. Staking

While both staking and liquidity provision involve committing tokens to support the Bittensor network, they serve different purposes and operate through distinct mechanisms.

**Staking** is designed to support validators and miners by providing them with consensus power. When you stake TAO to a validator, you're essentially voting for that validator's participation in the subnet's consensus mechanism. The validator's total stake (including your delegation) determines their share of emissions and influence in the network.

Stakers earn emissions off of their stake, which are distributed each tempo.

**Liquidity provision**, on the other hand, is focused on market making and trading facilitation. By providing liquidity to a subnet's trading pool, you're enabling other users to trade between TAO and the subnet's Alpha tokens. This creates a more liquid market and improves price discovery for the subnet's token.

Liquidity providers earn fees when others stake or unstake within the price range defined on the position.


## Liquidity Position Lifecycle

### Creating a Position

When creating a liquidity position, users provide liquidity in the form of a single `liquidity` parameter (in RAO). The system automatically calculates and charges the appropriate amounts of TAO and Alpha tokens from the user's wallet based on the current price.

1. User calls `add_liquidity()` with `liquidity`, `price_low`, and `price_high` parameters
2. System converts price range to tick indices using `price_to_tick()` 
3. System calculates required TAO and Alpha amounts based on current price and range
4. Tokens are transferred from user's wallet to the liquidity pool
5. A new `LiquidityPosition` is created with a unique `position_id`

[See source code](https://github.com/opentensor/bittensor/blob/staging/bittensor/utils/liquidity.py#L61-L72)
[See source code](https://github.com/opentensor/bittensor/blob/staging/bittensor/core/extrinsics/asyncex/liquidity.py#L50-L51)
[`pallets/swap/src/pallet/mod.rs:337`](https://github.com/opentensor/subtensor/blob/devnet-ready/pallets/swap/src/pallet/mod.rs#L337)
The main logic is handled by `do_add_liquidity` ([`pallets/swap/src/pallet/impls.rs:774`](https://github.com/opentensor/subtensor/blob/devnet-ready/pallets/swap/src/pallet/impls.rs#L807)):

### Modifying a Position

Position management through `modify_liquidity` allows you to adjust existing positions. When adding liquidity with a positive `liquidity_delta`, additional TAO and Alpha tokens are transferred from your wallet and the position's liquidity field is updated. When removing liquidity with a negative `liquidity_delta`, a pro-rata amount of TAO and Alpha tokens are returned to your wallet and the position's liquidity field is updated.

[See source code](https://github.com/opentensor/bittensor/blob/staging/bittensor/core/extrinsics/asyncex/liquidity.py#L74-L125)

### Fee Accumulation

As staking and unstaking on the relevant subnet token occur, within your position's price range, *fees* accumulate to your position. The blockchain maintains global fee counters (`FeeGlobalTao`, `FeeGlobalAlpha`) and individual ticks track fees collected at specific price points. 

Fees earned by each position are calculated using `calculate_fees()` [See source code](https://github.com/opentensor/bittensor/blob/staging/bittensor/utils/liquidity.py#L130-L158). Fee distribution is proportional to liquidity providers based on their share of total liquidity in the active price range and the duration their liquidity was active during trading.

### Removing a Position

When a position is destroyed/removed, the position's liquidity is converted back to tokens based on the current subnet price relative to your position's price range. The position is then deleted from the system.

[See source code](https://github.com/opentensor/bittensor/blob/staging/bittensor/core/extrinsics/asyncex/liquidity.py#L127-L185)





## Managing positions

### Adding a liquidity position

Create a liquidity position with `add_liquidity`.
```python
await subtensor.add_liquidity(
    wallet=wallet,
    netuid=netuid,
    liquidity=Balance.from_tao(1000),
    price_low=Balance.from_tao(1.5),
    price_high=Balance.from_tao(2.0),
    wait_for_inclusion=True,
    wait_for_finalization=False,
    period=None
)
```

[See source code](https://github.com/opentensor/bittensor/blob/staging/bittensor/core/subtensor.py#L2997-L3056)

### Modifying a position

Use `modify_liquidity` with the desired amount to add or subtract liquidity to an existing position.

```python
await subtensor.modify_liquidity(
    wallet=wallet,
    netuid=netuid,
    position_id=position_id,
    liquidity_delta=Balance.from_tao(500),
    wait_for_inclusion=True,
    wait_for_finalization=False,
    period=None
)
```

[See source code](https://github.com/opentensor/bittensor/blob/staging/bittensor/core/subtensor.py#L3210-L3269)

### Removing a liquidity position

Removes liquidity and credits balances back to the creator's wallet.

```python
await subtensor.remove_liquidity(
    wallet=wallet,
    netuid=netuid,
    position_id=position_id,
    wait_for_inclusion=True,
    wait_for_finalization=False,
    period=None
)
```

 [See source code](https://github.com/opentensor/bittensor/blob/staging/bittensor/core/subtensor.py#L3418-L3477)

### Listing positions

Get all positions on a specific subnet for a specific wallet. Returns a list of `LiquidityPosition` objects with calculated fees.

```python
positions = await subtensor.get_liquidity_list(
    wallet=wallet,
    netuid=netuid,
    block=None
)
```

[See source code](https://github.com/opentensor/bittensor/blob/staging/bittensor/core/subtensor.py#L1451-L1523)

