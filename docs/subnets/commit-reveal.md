
import ThemedImage from '@theme/ThemedImage';
import useBaseUrl from '@docusaurus/useBaseUrl';

# Commit Reveal

This page describes the **commit reveal** feature: a configurable waiting period that elapses between a) when consensus weights set by subnet validators are first committed, and b) when they are revealed publicly and included in Yuma Consensus.

This feature was designed to address the issue of *weight copying* by validators. 

## Weight copying

In each Bittensor subnet, each validator scores&mdash;or *'weights'*&mdash;each miner, producing what is referred to as a [weight vector](../glossary.md#weight-vector). The weight vectors for each validator in a subnet are combined into a weight matrix. This matrix determines emissions to miners in the subnet based on the consensus evaluation of their performance, according to [Yuma Consensus](../glossary.md#yuma-consensus).

The weight matrix is public information, and must be, so that emissions in the Bittensor platform can be transparently fair. However, this transparency makes it possible for subnet validators to free-ride on the work of other validators by copying the latest consensus rather than independently evaluating subnet miners. This is unfair and potentially degrades the quality of validation work, undermining Bittensor's ability to incentivize the best miners and produce the best digital commodities overall.

The commit reveal feature is designed to solve the weight copying problem by giving would-be weight copiers access only to stale weights. Copying stale weights should result in validators departing from consensus. However, it is critical to note that this only works if the consensus weight matrix changes sufficiently on the time scale of the commit reveal interval. If the demands on miners are too static, and miner performance is very stable, weight copying will still be successful. The only solution for this is to demand continuous improvement from miners, requiring them to continuously evolve to maintain their scoring. Combined with a properly tuned Commit Reveal interval, this will keep validators honest, as well as producing the best models.

## Commit Reveal and Immunity Period

The [Immunity Period](../glossary.md#immunity-period) is the interval (measured in blocks) during which a miner or validator newly registered on a subnet is 'immune' from deregistration due to performance. The duration of this period value should always be larger than the Commit Reveal interval, otherwise the immunity period will expire before a given miner's scores are available, and they may be deregistered without having their work counted.

When creating a new subnet, ensure that the miner immunity period is larger than the commit reveal interval. When updating the immunity period or commit reveal interval hyperparameters for a subnet, use the following formula:

```
new_immunity_period = (new_commit_reveal_interval - old_commit_reveal_interval) + old_immunity_period
```

See [Subnet Hyperparameters](./subnet-hyperparameters.md).

## Commit reveal in detail

When commit reveal is enabled, it works as follows:  

1. A subnet validator sets the weights normally by using [`set_weights`](pathname:///python-api/html/autoapi/bittensor/core/extrinsics/set_weights/index.html). 

2. Instead of publishing weights openly, an encrypted copy of these weights is committed to the blockchain, using an internal method called [`commit_weights`](pathname:///python-api/html/autoapi/bittensor/core/extrinsics/commit_weights/index.html).

3. A waiting interval, specified as a number of blocks, elapses. Subnet owners configure this interval with the subnet hyperparameter `commit_reveal_weights_interval`.

4. After this interval has elapsed, the unencrypted weights are automatically revealed by the chain, using [Drand time-lock encryption](https://drand.love/docs/timelock-encryption/).

5. The weights are now input to Yuma Consensus.

<br />
:::tip Commit reveal works behind the scenes
After the subnet owner turns ON the commit reveal feature, everything happens behind the scenes. A subnet validator will continue to set weights normally by using [`set_weights`](pathname:///python-api/html/autoapi/bittensor/core/extrinsics/set_weights/index.html).
:::

<center>
<ThemedImage
alt="'1-Commit Reveal'"
sources={{
    light: useBaseUrl('/img/docs/2-commit-reveal.svg'),
    dark: useBaseUrl('/img/docs/dark-2-commit-reveal.svg'),
}}
style={{width: 750}}
/>
</center>


## How to use the commit reveal feature

As a subnet owner, set the below hyperparameters to use the commit reveal feature:

1. `commit_reveal_weights_enabled` (boolean): Set this to `True` to activate the commit reveal feature for the subnet. Default value is `False`.
2. `commit_reveal_weights_interval` (int): Set this to an integer number. This is the number of subnet tempos to elapse before revealing the weights by submitting them again to the blockchain, but now openly for everyone to see. Default value is `1`.

See [Setting subnet hyperparameters](subnet-hyperparameters#setting-the-hyperparameters).

:::danger Ensure that the commit reveal interval is less than your immunity period to avoid unintended miner de-registration!
See [Commit Reveal and Immunity Period](#commit-reveal-and-immunity-period).
:::


Weights will be revealed immediately at the beginning of the tempo after the `commit_reveal_weights_interval`. For example, if `commit_reveal_weights_interval` value is set to `3`, then the reveal will occur at the beginning of the fourth tempo from the current tempo. The current tempo is counted as the first tempo. See the below diagram for this example: 

<center>
<ThemedImage
alt="'1-Commit Reveal'"
sources={{
    light: useBaseUrl('/img/docs/1-commit-reveal.svg'),
    dark: useBaseUrl('/img/docs/dark-1-commit-reveal.svg'),
}}
style={{width: 750}}
/>
</center>

<br />


## Technical papers and blog

- ACM CCS2024 Poster PDF [Solving the Free-rider Problem In Bittensor](pathname:///papers/ACM_CCS2024_Poster.pdf).
- See [Weight Copying in Bittensor, a technical paper (PDF)](pathname:///papers/BT_Weight_Copier-29May2024.pdf).
- Blog post, [Weight Copying in Bittensor](https://blog.bittensor.com/weight-copying-in-bittensor-422585ab8fa5).





Code References and Implementation Details

**Commit Reveal as Anti-Weight-Copying Mechanism:**
- Commit reveal prevents weight copying by introducing a time delay between weight commitment and revelation
  - `subtensor/pallets/subtensor/src/subnets/weights.rs:41` - `do_commit_weights()` implementation
- Validators commit to weights without revealing them immediately, creating a temporal offset
  - `subtensor/pallets/subtensor/src/subnets/weights.rs:74` - Weight commit storage in `WeightCommits<T>`
- The mechanism ensures that copied weights are stale by the time they can be used
  - `subtensor/pallets/subtensor/src/subnets/weights.rs:1075` - `get_reveal_blocks()` timing calculation

**Core Storage and Configuration:**

**Commit Reveal Enablement:**
- Commit reveal is controlled per subnet via `CommitRevealWeightsEnabled` storage
  - `subtensor/pallets/subtensor/src/lib.rs:1430` - `pub type CommitRevealWeightsEnabled<T> = StorageMap<_, Identity, u16, bool, ValueQuery, DefaultCommitRevealWeightsEnabled<T>>;`
- Enablement can be toggled by subnet owners or root
  - `subtensor/pallets/subtensor/src/utils/misc.rs:472-477` - `get_commit_reveal_weights_enabled()` and `set_commit_reveal_weights_enabled()`

**Weight Commit Storage:**
- **WeightCommits**: Stores commit hashes and timing information for each validator
  - `subtensor/pallets/subtensor/src/lib.rs:1662-1669` - `pub type WeightCommits<T: Config> = StorageDoubleMap<_, Twox64Concat, u16, Twox64Concat, T::AccountId, VecDeque<(H256, u64, u64, u64)>, OptionQuery>;`
- **CRV3WeightCommits**: Stores v3 encrypted commits with epoch-based organization
  - `subtensor/pallets/subtensor/src/lib.rs:1671-1680` - `pub type CRV3WeightCommits<T: Config> = StorageDoubleMap<_, Twox64Concat, u16, Twox64Concat, u64, VecDeque<(T::AccountId, BoundedVec<u8, ConstU32<MAX_CRV3_COMMIT_SIZE_BYTES>>, RoundNumber)>, ValueQuery>;`
- **RevealPeriodEpochs**: Configurable reveal period per subnet
  - `subtensor/pallets/subtensor/src/lib.rs:1682-1684` - `pub type RevealPeriodEpochs<T: Config> = StorageMap<_, Twox64Concat, u16, u64, ValueQuery, DefaultRevealPeriodEpochs<T>>;`

**Commit Phase Implementation:**

**Commit Hash Generation:**
- Commit hash is generated from validator data using BlakeTwo256
  - `subtensor/pallets/subtensor/src/tests/weights.rs:1520` - `let commit_hash: H256 = BlakeTwo256::hash_of(&(hotkey, netuid, uids.clone(), weight_values.clone(), salt.clone(), version_key));`
- Hash includes: hotkey, netuid, uids, weight_values, salt, and version_key
  - `subtensor/pallets/subtensor/src/subnets/weights.rs:74` - Commit storage with hash and timing information

**Commit Validation:**
- **Enablement Check**: Ensures commit-reveal is enabled for the subnet
  - `subtensor/pallets/subtensor/src/subnets/weights.rs:52` - `ensure!(Self::get_commit_reveal_weights_enabled(netuid), Error::<T>::CommitRevealDisabled);`
- **Registration Check**: Validates hotkey is registered on the network
  - `subtensor/pallets/subtensor/src/subnets/weights.rs:56-59` - `ensure!(Self::is_hotkey_registered_on_network(netuid, &who), Error::<T>::HotKeyNotRegisteredInSubNet);`
- **Rate Limiting**: Prevents excessive commit frequency
  - `subtensor/pallets/subtensor/src/subnets/weights.rs:61-66` - Rate limit check via `check_rate_limit()`

**Reveal Timing Calculation:**

**Epoch-Based Timing:**
- **Epoch Calculation**: Epochs are calculated based on tempo and netuid offset
  - `subtensor/pallets/subtensor/src/subnets/weights.rs:1040-1047` - `get_epoch_index()` implementation
- **Reveal Period**: Configurable number of epochs between commit and reveal
  - `subtensor/pallets/subtensor/src/subnets/weights.rs:1095-1097` - `get_reveal_period()` and `set_reveal_period()`

**Reveal Block Range:**
- **First Reveal Block**: Calculated from commit epoch + reveal period
  - `subtensor/pallets/subtensor/src/subnets/weights.rs:1075-1085` - `get_reveal_blocks()` implementation
- **Last Reveal Block**: First reveal block + tempo (one epoch duration)
  - `subtensor/pallets/subtensor/src/subnets/weights.rs:1086-1087` - `let last_reveal_block = first_reveal_block.saturating_add(tempo);`

**Reveal Phase Implementation:**

**Reveal Validation:**
- **Enablement Check**: Ensures commit-reveal is still enabled
  - `subtensor/pallets/subtensor/src/subnets/weights.rs:353` - `ensure!(Self::get_commit_reveal_weights_enabled(netuid), Error::<T>::CommitRevealDisabled);`
- **Hash Verification**: Validates revealed data matches committed hash
  - `subtensor/pallets/subtensor/src/subnets/weights.rs:396-396` - Hash matching in reveal validation
- **Timing Validation**: Ensures reveal occurs within valid time window
  - `subtensor/pallets/subtensor/src/subnets/weights.rs:1020-1027` - `is_reveal_block_range()` implementation

**Reveal Timing Checks:**
- **Too Early**: Reveal attempted before valid reveal period
  - `subtensor/pallets/subtensor/src/subnets/weights.rs:1020-1027` - `is_reveal_block_range()` check
- **Expired**: Commit has expired beyond reveal period
  - `subtensor/pallets/subtensor/src/subnets/weights.rs:1029-1035` - `is_commit_expired()` implementation
- **Valid Window**: Reveal must occur exactly at `commit_epoch + reveal_period`

**Commit Expiration and Cleanup:**

**Expiration Logic:**
- **Expiration Check**: Commits expire after reveal period + 1 epoch
  - `subtensor/pallets/subtensor/src/subnets/weights.rs:1029-1035` - `is_commit_expired()` function
- **Automatic Cleanup**: Expired commits are removed during reveal operations
  - `subtensor/pallets/subtensor/src/subnets/weights.rs:512-520` - Expired commit removal in batch reveal

**Queue Management:**
- **FIFO Processing**: Commits are processed in first-in-first-out order
  - `subtensor/pallets/subtensor/src/subnets/weights.rs:74` - `VecDeque<(H256, u64, u64, u64)>` storage
- **Commit Removal**: Revealed commits are removed from the queue
  - `subtensor/pallets/subtensor/src/subnets/weights.rs:410-415` - Commit removal after successful reveal

**Security Properties:**

**Anti-Weight-Copying:**
- **Temporal Offset**: Time delay prevents immediate weight copying
  - `subtensor/pallets/subtensor/src/subnets/weights.rs:1075` - Reveal timing calculation
- **Stale Data**: Copied weights become irrelevant due to network changes
  - `subtensor/pallets/subtensor/src/subnets/weights.rs:1029-1035` - Commit expiration mechanism
- **Hash Verification**: Cryptographic commitment prevents manipulation
  - `subtensor/pallets/subtensor/src/subnets/weights.rs:396` - Hash verification in reveal

**Rate Limiting:**
- **Commit Rate Limit**: Prevents excessive commit frequency
  - `subtensor/pallets/subtensor/src/subnets/weights.rs:61-66` - Rate limit validation
- **Reveal Timing**: Strict timing windows prevent timing attacks
  - `subtensor/pallets/subtensor/src/subnets/weights.rs:1020-1027` - Reveal timing validation

**Testing and Validation:**

**Comprehensive Test Coverage:**
- **Basic Functionality**: Tests verify commit and reveal workflow
  - `subtensor/pallets/subtensor/src/tests/weights.rs:1502-1559` - `test_reveal_weights_when_commit_reveal_disabled()`
- **Timing Validation**: Tests verify reveal timing constraints
  - `subtensor/pallets/subtensor/src/tests/weights.rs:1663-1750` - Timing validation tests
- **Hash Verification**: Tests verify cryptographic commitment integrity
  - `subtensor/pallets/subtensor/src/tests/weights.rs:1750-1831` - `test_commit_reveal_hash()`

**Error Handling:**
- **CommitRevealDisabled**: Attempting operations when disabled
  - `subtensor/pallets/subtensor/src/subnets/weights.rs:52` - Enablement check
- **RevealTooEarly**: Reveal attempted before valid window
  - `subtensor/pallets/subtensor/src/subnets/weights.rs:1020-1027` - Timing validation
- **ExpiredWeightCommit**: Reveal attempted after expiration
  - `subtensor/pallets/subtensor/src/subnets/weights.rs:1029-1035` - Expiration check
- **InvalidRevealCommitHashNotMatch**: Hash verification failure
  - `subtensor/pallets/subtensor/src/subnets/weights.rs:396` - Hash matching

**Network Configuration:**

**Subnet-Level Settings:**
- **Enablement**: Per-subnet commit reveal toggle
  - `subtensor/pallets/subtensor/src/utils/misc.rs:472-477` - Enablement functions
- **Reveal Period**: Configurable epochs between commit and reveal
  - `subtensor/pallets/subtensor/src/subnets/weights.rs:1095-1097` - Reveal period configuration
- **Rate Limits**: Commit frequency restrictions
  - `subtensor/pallets/subtensor/src/subnets/weights.rs:61-66` - Rate limiting

**Default Values:**
- **DefaultCommitRevealWeightsEnabled**: Defaults to false (disabled)
  - `subtensor/pallets/subtensor/src/lib.rs:799` - `pub fn DefaultCommitRevealWeightsEnabled<T: Config>() -> bool { false }`
- **DefaultRevealPeriodEpochs**: Default reveal period configuration
  - `subtensor/pallets/subtensor/src/lib.rs:735` - `pub fn DefaultRevealPeriodEpochs<T: Config>() -> u64 { 1 }`

**Key Mathematical Insights:**
1. **Commit Hash = BlakeTwo256(hotkey, netuid, uids, weights, salt, version_key)**: Cryptographic commitment
2. **Reveal Epoch = Commit Epoch + Reveal Period**: Timing calculation
3. **Reveal Block Range = [first_reveal_block, last_reveal_block]**: Valid reveal window
4. **Expiration = Current Epoch > Commit Epoch + Reveal Period + 1**: Automatic cleanup
5. **Temporal Offset = Reveal Period × Tempo**: Anti-copying delay

**Network Security Implications:**
- **Weight Copying Prevention**: Temporal offset makes copied weights stale
- **Consensus Stability**: Prevents rapid weight manipulation
- **Validator Commitment**: Requires validators to commit to their assessments
- **Network Decentralization**: Reduces influence of weight-copying validators
- **Dynamic Adaptation**: Network changes make stale weights irrelevant

**Complete Commit Reveal Flow:**
1. **Configuration** → Subnet enables commit reveal and sets reveal period
2. **Commit Phase** → Validator commits hash of weights without revealing them
3. **Temporal Offset** → Network progresses for reveal_period epochs
4. **Reveal Window** → Validator reveals weights within valid time window
5. **Hash Verification** → System verifies revealed data matches commit hash
6. **Weight Application** → Verified weights are applied to consensus
7. **Cleanup** → Expired commits are automatically removed

**Commit Reveal vs Traditional Weight Setting:**
- **Traditional**: Immediate weight setting and consensus participation
- **Commit Reveal**: Delayed weight revelation with temporal offset
- **Security**: Commit reveal prevents weight copying and manipulation
- **Complexity**: Additional timing and hash verification requirements
- **Flexibility**: Configurable per subnet based on security needs

