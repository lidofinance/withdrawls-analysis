<h3>Model description</h3>
This model was created for the simulation of the beacon chain. The model takes Beacon Chain state at the beginning of day and returns how networks will change at the end of day (day here 12 PM UTC to 12 PM UTC) 
<p>
<p>
<h3>Assumptions</h3>

1. If a validator is down, it will be down for a whole day
2. We operate with average effective and real balance so we look to validators in general, not like single units
3. Block proposal probability and sync committee inclusion probability is calculated as lido share among all validators
4. We don’t calculate whistleblower rewards
5. Inactivity leak lasts at least 1 day (225 epochs) 
6. EL rewards are not received in inactivity leak
7. Sync committee rewards for slashed validators are not counted
<p>
<p>
<h3>Model structure</h3>
The model consists of 3 modules, each module responsible for the calculation of specific part of beacon chain:  <p>

1. Attestation and proposal module: calculates which rewards and penalties would be gained by Lido validators due to attestations, participation in sync committee and block proposals (EL reward included in block proposals) 

2. Slashing module: calculate slashing penalties. In slashing penalties we include 3 types - initial slashing penalty, midterm slashing penalty, and penalty for being ‘offline’ (i.e not attesting block during slashing period). We calculate both daily impact (how many ETH would be loosed in 1 day of being slashed) and total impact (how many ETH would be loosed after the slashing period)

3. Inactivity leak module: calculate the impact on Lido validators due to inactivity leak, inactivity leak enables if more than 33% of network effective balance are inactive (i.e. approximately 33% of validator are down). In inactivity leak due to protocol design, we are not receiving attestation rewards, and due to finality loss, we are not receiving EL rewards.

For understanding how exactly rewards and penalties calculated in beacon chain [read this](https://eth2book.info/bellatrix/part2/incentives/rewards/).

<h3>List of inputs</h3>

______________________
<strong>Beacon chain global variables</strong>
<p>

| Variable                                | Value    |
|-----------------------------------------|----------|
| BASE_REWARD_FACTOR                      | 64*10**9 |
| GWEI_DENOMINATOR                        | 10**9    |
| TIMELY_SOURCE_WEIGHT                    | 14       |
| TIMELY_TARGET_WEIGHT                    | 26       |
| TIMELY_HEAD_WEIGHT                      | 14       |
| SYNC_REWARD_WEIGHT                      | 2        |
| PROPOSER_WEIGHT                         | 8        |
| WEIGHT_DENOMINATOR                      | 64       |
| EPOCH_IN_DAY                            | 225      |
| SLOTS_IN_EPOCH                          | 32       |
| SYNC_COMMITTEE_SIZE                     | 512      |
| MIN_SLASHING_PENALTY_QUOTIENT_BELLATRIX | 1/32     |
| MAX_PROPOSER_SLASHINGS_PER_BLOCK        | 16       |
| MAX_ATTESTER_SLASHINGS                  | 2        |
| PROPORTIONAL_SLASHING_MULTIPLIER        | 3        |
| EPOCHS_PER_SLASHINGS_VECTOR           | 8192  |
| INACTIVITY_PENALTY_QUOTIENT_BELLATRIX | 2**24 |
| INACTIVITY_SCORE_BIAS                 | 4     |


______________________
<strong>Network state</strong>
| Network state               |
|-----------------------------|
| lido_vals                   |
| other_vals                  |
| lido_avg_effective_balance  |
| other_avg_effective_balance |
| lido_avg_real_balance       |
| other_avg_real_balance      |
| median_EL_reward            |

______________________
<strong>Сontrolled variables
</strong>
| Network events         |
|------------------------|
| lido_down_vals         |
| other_down_vals        |
| lido_new_slashing      |
| lido_ongoing_slashing  |
| lido_midterm_slashing  |
| other_ongoing_slashing |
| network_state          |
| epoch_in_inactivity    |


<h3>List of outputs</h3>

| Name                            | Type          |
|---------------------------------|---------------|
| attestation_rewards             | Reward        |
| attestation_penalties           | Penalty       |
| proposal_reward                 | Reward        |
| sync_committee_reward           | Penalty       |
| sync_committee_penalty          | Penalty       |
| initial_slashing_penalties      | Penalty       |
| correlation_slashing_penalties  | Penalty       |
| total_att_loss_for_new_slashing | Penalty       |
| inactivity_leak_penalty         | Penalty       |
| epoch_in_inactivity             | Network state |
| el_rewards                      | Reward        |
| cl_rewards                      | Reward        |
| total_rewards                   | Reward        |
| total_penalties                 | Penalty       |
| total_delta                 | Network state |
| network_effective_balance   | Network state |
| lido_avg_real_balance       | Network state |
| other_avg_real_balance      | Network state |
| lido_avg_effective_balance  | Network state |
| other_avg_effective_balance | Network state |