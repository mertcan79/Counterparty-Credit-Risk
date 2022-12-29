from ccr_rwa import CCRRWA
from sa_ccr import SACCR
import random
import time
from datetime import datetime

print("--- CCR RWA CALCULATIONS START ---")

# Create a CCRRWA calculator
exposures = {'Counterparty A': 100, 'Counterparty B': 200, 'Counterparty C': 300, 'Counterparty D': 220}
risk_weights = {'Counterparty A': 0.5, 'Counterparty B': 0.25, 'Counterparty C': 0.75, 'Counterparty D': .55}
probability = {'Counterparty A': 0.1, 'Counterparty B': 0.25, 'Counterparty C': 0.3, 'Counterparty D': .22}

interest_rate_risk = {'Counterparty A': 0.1, 'Counterparty B': 0.08, 'Counterparty C': 0.11, 'Counterparty D': .02}
credit_risk = {'Counterparty A': 0.8, 'Counterparty B': 0.85, 'Counterparty C': 0.93, 'Counterparty D': .92}
liquidity_risk = {'Counterparty A': 0.9, 'Counterparty B': 0.75, 'Counterparty C': 0.63, 'Counterparty D': .79}
recovery_rates = {'Counterparty A': 0.09, 'Counterparty B': 0.05, 'Counterparty C': 0.03, 'Counterparty D': .09}

threshold = 450
LGD = 0.5
# Create an instance of the CCRRWA class
ccr_rwa = CCRRWA(exposures, risk_weights, probability, LGD, interest_rate_risk, credit_risk, liquidity_risk, recovery_rates, threshold)

# Calculate the CCR RWA
ccr_rwa_value = ccr_rwa.calculate_ccr_rwa()
print(f'CCR RWA: {ccr_rwa_value:.2f}')

# Calculate the potential loss due to counterparty default
potential_loss = ccr_rwa.calculate_potential_loss()
print(f'Potential loss due to counterparty default: {potential_loss:.2f}')

# Calculate the expected loss given default for each counterparty
lgd = ccr_rwa.calculate_lgd()
print(f"LGD: {lgd}")

# Calculate the Credit Valuation Adjustment for each counterparty
cva = ccr_rwa.calculate_cva(probability, lgd)
print(f"CVA: {cva}")

# Simulate the impact of counterparty defaults on the bank's balance sheet
loss = ccr_rwa.simulate_counterparty_defaults(probability)
print(f'Loss due to counterparty defaults: {loss:.2f}')
print("--- CCR RWA CALCULATIONS END ---")


print("###########"*10)

print("--- SA-CCRA CALCULATIONS START---")

# Initialize the SACCR instance
saccr = SACCR()

# Initialize the exposures data as a dictionary
exposures_data = {'Counterparty A': 100, 'Counterparty B': 200, 'Counterparty C': 300, 'Counterparty D': 220}

# Initialize the netting sets data as a dictionary
netting_sets_data = {'Counterparty A': 0.55, 'Counterparty B': 0.75, 'Counterparty C': 1.0, 'Counterparty D': 0.65}

# Initialize the risk mitigation data as a dictionary
risk_mitigation_data = {'Counterparty A': 0.1, 'Counterparty B': 0.2, 'Counterparty C': 0.3, 'Counterparty D': 0.15}

# Load the exposures data into the SACCR instance
for counterparty, exposure in exposures_data.items():
  saccr.exposures[counterparty] = exposure

# Load the netting sets data into the SACCR instance
for counterparty, netting_set_data in netting_sets_data.items():
  saccr.netting_sets[counterparty] = netting_set_data

# Load the risk mitigation data into the SACCR instance
for counterparty, risk_mitigation_data in risk_mitigation_data.items():
  saccr.risk_mitigation[counterparty] = risk_mitigation_data


saccr.calculate_pfe()
# Calculate the CCR capital requirement for each counterparty
saccr.calculate_ccr_capital_requirement()
sum_saccra = 0
# Print the CCR capital requirement for each counterparty
for counterparty, ccr_capital_requirement in saccr.ccr_capital_requirement.items():
      print(f'SA-CCR capital requirement for {counterparty}: {ccr_capital_requirement}')
      sum_saccra += ccr_capital_requirement
print(f"SA-CCR is {sum_saccra}")

print("--- SA-CCR CALCULATIONS END---")

print("--- UPDATE CCR with changed exposures and risk weights & netting sets ---")

while True:
    # Generate new exposures and risk weights with slight variations from the previous values
    new_exposures = {k: v + random.uniform(-5, 5) for k, v in exposures.items()}
    new_risk_weights = {k: v + random.uniform(-0.01, 0.01) for k, v in risk_weights.items()}
    new_netting_sets = {k: v + random.uniform(-0.019, 0.019) for k, v in netting_sets_data.items()}

    # Update the exposures and risk weights in the CCRRWA instance
    ccr_rwa.update_exposures_and_risk_weights(new_exposures, new_risk_weights)
    saccr.update_exposures_and_netting_sets(new_exposures, new_netting_sets)

    # Calculate the CCR RWA using the updated exposures and risk weights
    ccr_rwa_value = ccr_rwa.calculate_ccr_rwa()
    saccra_value = saccr.calculate_ccr_capital_requirement()
    print(f'At time {datetime.now()} the CCRs are:')
    print(f'CCR RWA: {ccr_rwa_value:.2f}')
    print(f'SA-CCR: {saccra_value:.2f}')
    # Sleep for 3 seconds before updating the exposures and risk weights again
    time.sleep(3)

