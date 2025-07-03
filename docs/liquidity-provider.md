---
title: Provisioning Liquidity to Subnets
---

# Provisioning Liquidity to Subnets

## Overview

The Liquidity Provider (LP) feature allows users to become providers of trading liquidity for specific subnets, within specified price ranges for the subnet $\alpha$ token. This system is based on Uniswap V3's concentrated liquidity model and enables users to earn fees from trading activity.

The implementation is located in [`bittensor/utils/liquidity.py`](https://github.com/opentensor/bittensor/blob/staging/bittensor/utils/liquidity.py#L1-L8), which provides utilities for managing liquidity positions and price conversions in the Bittensor network.

## Key Concepts

### Liquidity Positions
A liquidity position represents a user's contribution to a trading pool within a specific price range. Each position has:
- **Price Range**: Defined by `price_low` and `price_high` in TAO
- **Liquidity Amount**: The total liquidity provided (in RAO)
- **Position ID**: Unique identifier for the position
- **Fee Tracking**: Separate tracking for TAO and Alpha fees earned

### Price Ranges and Ticks
The system uses a tick-based pricing mechanism based on Uniswap V3:
- **Ticks**: Discrete price points with 0.01% spacing (PRICE_STEP = 1.0001)
- **Price Range**: Each position covers a range of ticks
- **Concentrated Liquidity**: Liquidity is only active within the specified range

## Use Cases

### For TAO holders
- Provide liquidity in expected price ranges
- Earn fees from trading activity
- Participate in market making

### For subnet creators
- Enable user liquidity provision
- Increase trading volume and liquidity
- Improve price discovery

Subnet creators can enable/disable user liquidity provision via the `toggle_user_liquidity` function.

[See source code](https://github.com/opentensor/bittensor/blob/staging/bittensor/core/extrinsics/asyncex/liquidity.py#L187-L232)

### Subnet configuration

A subnet's creator can enable and disable user the Liquidity Provider feature via `toggle_user_liquidity`.

[See source code](https://github.com/opentensor/bittensor/blob/staging/bittensor/core/async_subtensor.py#L4863-L4904)

## Managing positions

### Adding a liquidity position
```python
await subtensor.add_liquidity(
    wallet=wallet,
    netuid=netuid,
    liquidity=Balance.from_tao(1000),
    price_low=Balance.from_tao(1.5),
    price_high=Balance.from_tao(2.0)
)
```

[See source code](https://github.com/opentensor/bittensor/blob/staging/bittensor/core/extrinsics/asyncex/liquidity.py#L13-L72)

### Modifying a position

Use `modify_liquidity` with the desired amount to add or subtract liquidity to an existing position.

```python
await subtensor.modify_liquidity(
    wallet=wallet,
    netuid=netuid,
    position_id=position_id,
    liquidity_delta=Balance.from_tao(500)
)

```

[See source code](https://github.com/opentensor/bittensor/blob/staging/bittensor/core/extrinsics/asyncex/liquidity.py#L74-L125)

### Removing a liquidity position

Removes liquidity and credits balances back to the creator's wallet.

```python
await subtensor.remove_liquidity(
    wallet=wallet,
    netuid=netuid,
    position_id=position_id
)
```

 [See source code](https://github.com/opentensor/bittensor/blob/staging/bittensor/core/extrinsics/asyncex/liquidity.py#L127-L185)

### Listing positions

Get all positions on a specific subnet for a specific wallet. Returns a list of `LiquidityPosition` objects with calculated fees.

```python
positions = await subtensor.get_liquidity_list(
    wallet=wallet,
    netuid=netuid
)
```

[See source code](https://github.com/opentensor/bittensor/blob/staging/bittensor/core/async_subtensor.py#L1862-L2034)

## Fee Structure

### Fee Calculation

Liquidity providers earn fees from trading activity within their price range: 

- **TAO Fees**: Fees earned in TAO tokens
- **Alpha Fees**: Fees earned in Alpha tokens
- **Fee Distribution**: Proportional to liquidity provided and trading volume

The `calculate_fees()` function calculates both TAO and Alpha fees based on global fee data and position liquidity.

[See source code](https://github.com/opentensor/bittensor/blob/staging/bittensor/utils/liquidity.py#L130-L158)


## Risk Considerations

### Impermanent Loss
Liquidity providers face impermanent loss when the price moves outside their specified range:
- **In-Range**: Earns trading fees
- **Out-of-Range**: No fees earned, potential for impermanent loss

### Dynamic TAO/alpha composition

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

### Price Range Risk
- **Narrow Ranges**: Higher fee concentration but higher risk
- **Wide Ranges**: Lower risk but potentially lower fee earnings

## Comparison with Staking

| Aspect | Staking (add_stake) | Liquidity Provider |
|--------|-------------------|-------------------|
| **Purpose** | Support validators/miners | Provide trading liquidity |
| **Token Conversion** | TAO → Alpha | TAO + Alpha pool |
| **Price Range** | Current market price | User-defined range |
| **Rewards** | Subnet participation | Trading fees |
| **Risk** | Validator performance | Impermanent loss |
| **Complexity** | Simple stake/unstake | Position management |


## Liquidity Position Lifecycle

### 1. Position Creation (add_liquidity)

**Token Source**: When creating a liquidity position, users provide liquidity in the form of a single `liquidity` parameter (in RAO). The system automatically calculates and allocates the appropriate amounts of TAO and Alpha tokens based on the current price and the specified price range.

**Process**:
1. User calls `add_liquidity()` with `liquidity`, `price_low`, and `price_high` parameters
2. System converts price range to tick indices using `price_to_tick()` [See source code](https://github.com/opentensor/bittensor/blob/staging/bittensor/utils/liquidity.py#L61-L72)
3. System calculates required TAO and Alpha amounts based on current price and range
4. Tokens are transferred from user's wallet to the liquidity pool
5. A new `LiquidityPosition` is created with a unique `position_id`

[See source code](https://github.com/opentensor/bittensor/blob/staging/bittensor/core/extrinsics/asyncex/liquidity.py#L50-L51)

### 2. Position Management (modify_liquidity)

**Token Flows**:
- **Adding Liquidity**: Positive `liquidity_delta` increases the position size
  - Additional TAO and Alpha tokens are transferred from user's wallet
  - Position's `liquidity` field is updated
- **Removing Liquidity**: Negative `liquidity_delta` decreases the position size
  - Pro-rata amount of TAO and Alpha tokens are returned to user's wallet
  - Position's `liquidity` field is updated

[See source code](https://github.com/opentensor/bittensor/blob/staging/bittensor/core/extrinsics/asyncex/liquidity.py#L74-L125)

### 3. Fee Accumulation

**Fee Collection**: As trading occurs within the position's price range, fees accumulate in both TAO and Alpha tokens:

- **Global Fee Tracking**: System maintains global fee counters (`FeeGlobalTao`, `FeeGlobalAlpha`)
- **Tick-Level Tracking**: Individual ticks track fees collected at specific price points
- **Position Fee Calculation**: Fees earned by each position are calculated using `calculate_fees()` [See source code](https://github.com/opentensor/bittensor/blob/staging/bittensor/utils/liquidity.py#L130-L158)

**Fee Distribution**: Fees are distributed proportionally to liquidity providers based on:
- Their share of total liquidity in the active price range
- The duration their liquidity was active during trading

The fee calculation from global and tick-level data is implemented in [`bittensor/core/async_subtensor.py`](https://github.com/opentensor/bittensor/blob/staging/bittensor/core/async_subtensor.py#L1890-L1930).


### 4. Position Removal (remove_liquidity)

**Token Return**: When removing a position entirely:

1. The liquidity accumulated to the position is credited to the user, the amounts depending on the current subnet token price. See [Dynamic TAO/alpha composition](#dynamic-taoalpha-composition)]
2. Position is deleted from the system

[See source code](https://github.com/opentensor/bittensor/blob/staging/bittensor/core/extrinsics/asyncex/liquidity.py#L127-L185)

## Impermanent Loss Scenarios

**Price Movement Effects**:
- **Price Increases**: Position may end up with more TAO and less Alpha than initially provided
- **Price Decreases**: Position may end up with more Alpha and less TAO than initially provided
- **Out-of-Range**: Position becomes single-token (either all TAO or all Alpha)

**Fee Compensation**: Trading fees earned can offset impermanent loss, potentially making the position profitable even with price movements.

## Tracking your positions

**Storage Structure**: Each position is tracked with:
- `id`: Unique position identifier
- `tick_low`/`tick_high`: Price range boundaries
- `liquidity`: Current liquidity amount
- `fees_tao`/`fees_alpha`: Accumulated fees
- `netuid`: Associated subnet

The `LiquidityPosition` dataclass definition and position creation are implemented in [`bittensor/utils/liquidity.py`](https://github.com/opentensor/bittensor/blob/staging/bittensor/utils/liquidity.py#L18-L26) and [`bittensor/core/async_subtensor.py`](https://github.com/opentensor/bittensor/blob/staging/bittensor/core/async_subtensor.py#L2000-L2030).

