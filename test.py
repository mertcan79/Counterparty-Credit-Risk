from main import CCRRWA
import random
import time

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

while True:
    # Generate new exposures and risk weights with slight variations from the previous values
    new_exposures = {k: v + random.uniform(-5, 5) for k, v in exposures.items()}
    new_risk_weights = {k: v + random.uniform(-0.01, 0.01) for k, v in risk_weights.items()}

    # Update the exposures and risk weights in the CCRRWA instance
    ccr_rwa.update_exposures_and_risk_weights(new_exposures, new_risk_weights)

    # Calculate the CCR RWA using the updated exposures and risk weights
    ccr_rwa_value = ccr_rwa.calculate_ccr_rwa()
    print(f'CCR RWA: {ccr_rwa_value:.2f}')

    # Sleep for 3 seconds before updating the exposures and risk weights again
    time.sleep(3)

