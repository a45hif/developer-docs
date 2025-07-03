---
title: Provisioning Liquidity to Subnets
---

# Provisioning Liquidity to Subnets

## Overview

The Liquidity Provider (LP) feature allows users to become providers of trading liquidity for specific subnets, within specified price ranges for the subnet $\alpha$ token. This system is based on Uniswap V3's concentrated liquidity model and enables users to earn fees from trading activity.


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


## Tokenomics

### Fees

Liquidity providers earn fees from trading activity within their price range: 

- **TAO Fees**: Fees earned in TAO tokens
- **Alpha Fees**: Fees earned in Alpha tokens
- **Fee Distribution**: Proportional to liquidity provided and trading volume

The `calculate_fees()` function calculates both TAO and Alpha fees based on global fee data and position liquidity.

[See source code](https://github.com/opentensor/bittensor/blob/staging/bittensor/utils/liquidity.py#L130-L158)

### Dynamic token composition

Liquidity providers experience changes in their token composition based on price movements relative to their specified range:


**Price Movement Effects**:

1. **Price Below Range** (`current_price < price_low`):
   - Position becomes **100% Alpha tokens**
   - `amount_alpha = liquidity * (1/sqrt_price_low - 1/sqrt_price_high)`
   - `amount_tao = 0`

2. **Price Above Range** (`current_price > price_high`):
   - Position becomes **100% TAO tokens**
   - `amount_alpha = 0`
   - `amount_tao = liquidity * (sqrt_price_high - sqrt_price_low)`

3. **Price Within Range** (`price_low <= current_price <= price_high`):
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

## Comparison with Staking

| Aspect | Staking (add_stake) | Liquidity Provider |
|--------|-------------------|-------------------|
| **Purpose** | Support validators/miners | Provide trading liquidity |
| **Token Conversion** | TAO → Alpha | TAO + Alpha pool |
| **Price Range** | Current market price | User-defined range |
| **Rewards** | Subnet participation | Trading fees |
| **Risk** | Validator performance | Token composition changes |
| **Complexity** | Simple stake/unstake | Position management |


## Liquidity Position Lifecycle

### 1. Position Creation (add_liquidity)

When creating a liquidity position, users provide liquidity in the form of a single `liquidity` parameter (in RAO). The system automatically calculates and allocates the appropriate amounts of TAO and Alpha tokens based on the current price and the specified price range.

1. User calls `add_liquidity()` with `liquidity`, `price_low`, and `price_high` parameters
2. System converts price range to tick indices using `price_to_tick()` [See source code](https://github.com/opentensor/bittensor/blob/staging/bittensor/utils/liquidity.py#L61-L72)
3. System calculates required TAO and Alpha amounts based on current price and range
4. Tokens are transferred from user's wallet to the liquidity pool
5. A new `LiquidityPosition` is created with a unique `position_id`

[See source code](https://github.com/opentensor/bittensor/blob/staging/bittensor/core/extrinsics/asyncex/liquidity.py#L50-L51)

**Blockchain Implementation Details**:

When the Python SDK calls `add_liquidity_extrinsic` on [line 55 in liquidity.py](https://github.com/opentensor/bittensor/blob/staging/bittensor/core/extrinsics/asyncex/liquidity.py#L55), it triggers the following sequence in the subtensor blockchain:

1. Extrinsic Call (`Swap::add_liquidity`)

The extrinsic call maps to the `add_liquidity` function in the **Swap pallet** ([`pallets/swap/src/pallet/mod.rs:337`](https://github.com/opentensor/subtensor/blob/devnet-ready/pallets/swap/src/pallet/mod.rs#L337)):


#### **2. Core Implementation (`do_add_liquidity`)**

The main logic is handled by `do_add_liquidity` ([`pallets/swap/src/pallet/impls.rs:774`](https://github.com/opentensor/subtensor/blob/devnet-ready/pallets/swap/src/pallet/impls.rs#L774)):

```rust
pub fn do_add_liquidity(
    netuid: NetUid,
    coldkey_account_id: &T::AccountId,
    hotkey_account_id: &T::AccountId,
    tick_low: TickIndex,
    tick_high: TickIndex,
    liquidity: u64,
) -> Result<(PositionId, u64, u64), Error<T>>
```

**Key Steps:**

1. **Validation Checks:**
   - Ensures user liquidity is enabled for the subnet (`EnabledUserLiquidity`)
   - Validates tick range (`tick_high > tick_low`)
   - Checks user has sufficient TAO and Alpha balances
   - Ensures liquidity meets minimum threshold

2. **Position Creation:**
   - Generates new `PositionId` using `PositionId::new()`
   - Creates `Position` struct with tick range and liquidity amount
   - Calculates required TAO and Alpha token amounts based on current price

3. **Tick Management:**
   - Updates tick data at `tick_low` and `tick_high` via `add_liquidity_at_index()`
   - Updates current liquidity if position crosses current price
   - Manages tick bitmap for efficient price range queries

4. **Storage Updates:**
   - Stores position in `Positions` storage map: `(netuid, coldkey, position_id) -> Position`
   - Updates global liquidity tracking
   - Marks subnet as V3 initialized (`SwapV3Initialized`)

#### **3. Token Amount Calculation**

The `Position::to_token_amounts()` method ([`pallets/swap/src/position.rs:63`](https://github.com/opentensor/subtensor/blob/devnet-ready/pallets/swap/src/position.rs#L63)) calculates required tokens based on current price relative to position range:

```rust
// Pseudocode implementation:
if current_price < price_low {
    tao = 0
    alpha = liquidity * (1/sqrt_price_low - 1/sqrt_price_high)
} else if current_price > price_high {
    tao = liquidity * (sqrt_price_high - sqrt_price_low)
    alpha = 0
} else {
    tao = liquidity * (current_price - sqrt_price_low)
    alpha = liquidity * (1/current_price - 1/sqrt_price_high)
}
```

#### **4. Balance Operations**

After successful position creation, the extrinsic performs actual token transfers:

1. **Token Withdrawal (Source of Funds):**
   - **TAO Source**: `T::BalanceOps::decrease_balance(&coldkey, tao_needed)` 
     - Withdraws from your **coldkey's free TAO balance**
     - This is your regular TAO wallet balance, not staked tokens
   - **Alpha Source**: `T::BalanceOps::decrease_stake(&coldkey, &hotkey, netuid, alpha_needed)`
     - Withdraws from your **hotkey's existing stake** on the specified subnet
     - Converts staked Alpha tokens into liquidity position

2. **Reserve Pool Updates:**
   - `T::BalanceOps::increase_provided_tao_reserve(netuid, tao_provided)` - Adds TAO to subnet's liquidity pool
   - `T::BalanceOps::increase_provided_alpha_reserve(netuid, alpha_provided)` - Adds Alpha to subnet's liquidity pool

**Balance Requirements:**
- **Coldkey**: Must have sufficient free TAO balance (not staked)
- **Hotkey**: Must have sufficient staked Alpha tokens on the target subnet
- The exact amounts needed depend on your `liquidity` parameter and current market price

#### **5. Event Emission**

Finally, the system emits a `LiquidityAdded` event ([`pallets/swap/src/pallet/mod.rs:157`](https://github.com/opentensor/subtensor/blob/devnet-ready/pallets/swap/src/pallet/mod.rs#L157)):

```rust
LiquidityAdded {
    coldkey: T::AccountId,
    hotkey: T::AccountId,
    netuid: NetUid,
    position_id: PositionId,
    liquidity: u64,
    tao: u64,
    alpha: u64,
    tick_low: TickIndex,    // Added in PR #1814
    tick_high: TickIndex,   // Added in PR #1814
}
```

#### **Storage Schema**

The Swap pallet maintains several storage items:

- **`Positions`**: `(NetUid, AccountId, PositionId) -> Position` - Individual liquidity positions
- **`Ticks`**: `(NetUid, TickIndex) -> Tick` - Tick-level liquidity and fee data
- **`CurrentLiquidity`**: `NetUid -> u64` - Active liquidity at current price
- **`AlphaSqrtPrice`**: `NetUid -> U64F64` - Current square root price
- **`FeeGlobalTao/Alpha`**: `NetUid -> U64F64` - Global fee accumulation
- **`EnabledUserLiquidity`**: `NetUid -> bool` - User liquidity toggle per subnet

#### **Error Handling**

Common errors returned by the implementation:

- `UserLiquidityDisabled` - Subnet doesn't allow user liquidity
- `InsufficientBalance` - Not enough TAO or Alpha tokens
- `InvalidTickRange` - Invalid price range specification
- `InvalidLiquidityValue` - Liquidity amount too small
- `MaxPositionsExceeded` - Too many positions for this account

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

1. The position's liquidity is converted back to tokens based on the current subnet price relative to your position's price range. See [Token Composition Scenarios](#token-composition-scenarios)
2. Position is deleted from the system

[See source code](https://github.com/opentensor/bittensor/blob/staging/bittensor/core/extrinsics/asyncex/liquidity.py#L127-L185)


### 5. Tracking your positions

**Storage Structure**: Each position is tracked with:
- `id`: Unique position identifier
- `tick_low`/`tick_high`: Price range boundaries
- `liquidity`: Current liquidity amount
- `fees_tao`/`fees_alpha`: Accumulated fees
- `netuid`: Associated subnet

See [`bittensor/utils/liquidity.py`](https://github.com/opentensor/bittensor/blob/staging/bittensor/utils/liquidity.py#L1-L8), which provides utilities for managing liquidity positions and price conversions in the Bittensor network.

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


## Managing positions

### Adding a liquidity position
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


## Comparison with Uniswap V3

### **Similarities with Uniswap V3**

The Bittensor liquidity provider system is heavily inspired by Uniswap V3's concentrated liquidity model, with several key similarities:

#### **1. Concentrated Liquidity Model**
- **Bittensor**: Users specify `price_low` and `price_high` to define liquidity range [See source code](https://github.com/opentensor/bittensor/blob/staging/bittensor/core/extrinsics/asyncex/liquidity.py#L50-L51)
- **Uniswap V3**: Users specify `tickLower` and `tickUpper` to define price range
- **Similarity**: Both allow liquidity providers to concentrate their capital in specific price ranges

#### **2. Tick-Based Pricing System**
- **Bittensor**: Uses `price_to_tick()` and `tick_to_price()` functions with `PRICE_STEP = 1.0001` [See source code](https://github.com/opentensor/bittensor/blob/staging/bittensor/utils/liquidity.py#L61-L80)
- **Uniswap V3**: Uses ticks with 0.01% price spacing (1.0001 multiplier)
- **Similarity**: Identical tick spacing and price conversion mechanics

#### **3. Position Management**
- **Bittensor**: `add_liquidity()`, `modify_liquidity()`, `remove_liquidity()` [See source code](https://github.com/opentensor/bittensor/blob/staging/bittensor/core/extrinsics/asyncex/liquidity.py#L13-L185)
- **Uniswap V3**: `mint()`, `increaseLiquidity()`, `decreaseLiquidity()`, `burn()`
- **Similarity**: Similar lifecycle operations for position management

#### **4. Fee Collection**
- **Bittensor**: Global and tick-level fee tracking with `calculate_fees()` [See source code](https://github.com/opentensor/bittensor/blob/staging/bittensor/utils/liquidity.py#L130-L158)
- **Uniswap V3**: Fee accumulation in positions with `collect()` function
- **Similarity**: Both track fees at multiple levels and allow fee collection

#### **5. Single-Side Liquidity**
- **Bittensor**: Positions can become single-token when price moves outside range [See source code](https://github.com/opentensor/bittensor/blob/staging/bittensor/utils/liquidity.py#L28-L58)
- **Uniswap V3**: Single-side positions when current price is outside the range
- **Similarity**: Both support single-token liquidity positions

### **Key Differences from Uniswap V3**

#### **1. Token Pair Structure**
- **Bittensor**: TAO (network token) vs Alpha (subnet-specific token)
- **Uniswap V3**: Generic token pairs (any ERC-20 tokens)
- **Difference**: Bittensor has a fixed token relationship across all pools

#### **2. Position Representation**
- **Bittensor**: Uses `LiquidityPosition` dataclass with direct fee tracking [See source code](https://github.com/opentensor/bittensor/blob/staging/bittensor/utils/liquidity.py#L18-L26)
- **Uniswap V3**: Uses NFT-based positions via `NonfungiblePositionManager`
- **Difference**: Bittensor positions are not NFTs and have built-in fee tracking

#### **3. Subnet Integration**
- **Bittensor**: Positions are subnet-specific with `netuid` parameter [See source code](https://github.com/opentensor/bittensor/blob/staging/bittensor/core/async_subtensor.py#L2000-L2030)
- **Uniswap V3**: Pool-specific positions
- **Difference**: Bittensor integrates liquidity with subnet governance and operations

#### **4. Fee Structure**
- **Bittensor**: Separate tracking of TAO and Alpha fees with `fees_tao` and `fees_alpha` [See source code](https://github.com/opentensor/bittensor/blob/staging/bittensor/core/async_subtensor.py#L1890-L1930)
- **Uniswap V3**: Single fee rate per pool (0.01%, 0.05%, 0.3%, 1%)
- **Difference**: Bittensor has dual-token fee structure tied to subnet economics

#### **5. Access Control**
- **Bittensor**: Subnet owners can enable/disable user liquidity via `toggle_user_liquidity` [See source code](https://github.com/opentensor/bittensor/blob/staging/bittensor/core/async_subtensor.py#L4863-L4904)
- **Uniswap V3**: Open access to all users
- **Difference**: Bittensor has subnet-level governance over liquidity provision

#### **6. Implementation Architecture**
- **Bittensor**: Built into the core blockchain as a "Swap" module
- **Uniswap V3**: Separate smart contracts on Ethereum
- **Difference**: Bittensor liquidity is native to the blockchain, not a separate protocol

### **Technical Implementation Notes**

#### **Uniswap V3 References**
- **Tick System**: Bittensor uses identical tick spacing (1.0001) as Uniswap V3
- **Price Conversion**: `price_to_tick()` and `tick_to_price()` functions mirror Uniswap V3's implementation
- **Liquidity Math**: The `to_token_amounts()` method uses similar sqrt price calculations [See source code](https://github.com/opentensor/bittensor/blob/staging/bittensor/utils/liquidity.py#L28-L58)

#### **Bittensor-Specific Adaptations**
- **Subnet Economics**: Fee structure designed around subnet participation and Alpha token economics
- **Network Integration**: Liquidity positions tied to subnet operations and governance
- **Simplified Interface**: Direct API methods without NFT complexity

#### **References**
- **Uniswap V3 Documentation**: https://docs.uniswap.org/sdk/v3/guides/liquidity/position-data
- **Concentrated Liquidity**: https://uniswap.org/whitepaper-v3.pdf
- **Tick System**: https://docs.uniswap.org/concepts/protocol/concentrated-liquidity

## Implementation Status

The liquidity provider functionality is **fully implemented** in the subtensor blockchain on the `devnet-ready` branch. Based on [PR #1814](https://github.com/opentensor/subtensor/pull/1814), recent improvements have been made to ensure event consistency with Uniswap V3 standards.

### **Current Implementation State**

| Component | Status | Location |
|-----------|--------|----------|
| **Python SDK** | ✅ Complete | `bittensor/core/extrinsics/asyncex/liquidity.py` |
| **Utility Functions** | ✅ Complete | `bittensor/utils/liquidity.py` |
| **Swap Pallet** | ✅ Complete | `subtensor/pallets/swap/` (devnet-ready branch) |
| **Position Management** | ✅ Complete | Full CRUD operations for liquidity positions |
| **Fee Tracking** | ✅ Complete | Global and position-level fee calculation |
| **Event System** | ✅ Complete | Uniswap V3-compatible events |

### **Deployment Status**

- **Development**: Available on `devnet-ready` branch
- **Production**: Deployment pending mainnet integration
- **Testing**: Full test suite available in `pallets/swap/src/pallet/tests.rs`

### **Usage Requirements**

To use the liquidity provider features:

1. **Subnet Configuration**: Subnet owners must enable user liquidity via `toggle_user_liquidity`
2. **Account Setup**: Users need both TAO (coldkey) and Alpha tokens (hotkey stake)
3. **Network Support**: Currently available on devnet, mainnet deployment in progress
