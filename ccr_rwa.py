import random
import math


class CCRRWA:
    def __init__(self, exposures, risk_weights, PD, LGD, interest_rate_risk, credit_risk, liquidity_risk,
                 recovery_rates, threshold):
        """
        Constructor for the CCRRWA class.

        Parameters:
        - exposures: a dictionary of exposures, indexed by counterparty name
        - risk_weights: a dictionary of risk weights, indexed by counterparty name
        - PD: probability of default
        - LGD: loss given default
        - interest_rate_risk
        - credit_risk
        - liquidity_risk
        - recovery_rates
        - threshold: CCR RWA institution is willing to accept as max.
        """
        self.exposures = exposures
        self.risk_weights = risk_weights
        self.PD = PD
        self.LGD = LGD
        self.interest_rate_risk = interest_rate_risk
        self.credit_risk = credit_risk
        self.liquidity_risk = liquidity_risk
        self.recovery_rates = recovery_rates
        self.threshold = threshold

    def calculate_lgd(self):
        """
        Calculates the expected loss given default for each counterparty.

        Returns:
        - lgd: a dictionary of expected loss given default values, indexed by counterparty name
        """
        lgd = {}
        for key, value in self._traverse_tree(self.risk_weights_tree):
            lgd[key] = self.LGD * value
        return lgd

    def calculate_cva(self, probability, lgd):
        """
        Calculates the CVA for each counterparty.

        Parameters:
        - probability: the probability of default for each counterparty
        - lgd: the expected loss given default for each counterparty

        Returns:
        - cva: a dictionary of CVA values, indexed by counterparty name
        """
        netting_factor = 1
        cva = {}
        for key in self.risk_weights:
            # Calculate the Credit Valuation Adjustment for each counterparty
            cva[key] = self.exposures[key] * probability[key] * lgd[key] * self.interest_rate_risk[key] \
                       * self.credit_risk[key] * self.liquidity_risk[key] * (1 - self.recovery_rates[key])
            netting_factor *= (1 - cva[key])
        # Use netting techniques to better capture the complexity of CVA
        for key in self.risk_weights:
            cva[key] = cva[key] / netting_factor
        return cva

    def update_exposures_and_risk_weights(self, new_exposures, new_risk_weights):
        """
        Updates the exposures and risk weights stored in the CCRRWA instance.

        Parameters:
        - new_exposures: a dictionary of new exposures, indexed by counterparty name
        - new_risk_weights: a dictionary of new risk weights, indexed by counterparty name
        """
        self.exposures = new_exposures
        self.risk_weights = new_risk_weights

    def calculate_ccr_rwa(self):
        """
        Calculates the CCR RWA for the exposures and risk weights specified in the constructor.

        Returns:
        - ccr_rwa: the CCR RWA for the exposures
        """
        ccr_rwa = 0
        for key, value in self._traverse_tree(self.exposures_tree):
            ccr_rwa += value * self.risk_weights[key]
        if ccr_rwa > self.threshold:
          print("Attention required, threshold passed. Required to hold additional capital to meet regulatory requirements.")

        return ccr_rwa

    def calculate_probability_of_default(self):
        """
        Calculates the probability of default for each counterparty.

        Returns:
        - probability: a dictionary of probability of default values, indexed by counterparty name
        """
        probability = {}
        for key, value in self._traverse_tree(self.risk_weights_tree):
            probability[key] = 1 - math.exp(-value * self.PD[key])
        return probability

    def calculate_potential_loss(self):
        """
        Calculates the potential loss due to counterparty default for the exposures and risk weights stored in the CCRRWA instance.

        Returns:
        - potential_loss: the potential loss due to counterparty default
        """
        # Calculate the probability of default for each counterparty
        probability = self.calculate_probability_of_default()

        # Calculate the expected loss given default for each counterparty
        lgd = self.calculate_lgd()

        # Calculate the CVA for each counterparty
        cva = self.calculate_cva(probability, lgd)

        # Calculate the potential loss due to counterparty default
        potential_loss = sum(cva.values())
        return potential_loss

    def simulate_counterparty_defaults(self, probability):
        """
        Simulates the impact of counterparty defaults on the bank's balance sheet.

        Parameters:
        - probability: the probability of default for each counterparty

        Returns:
        - loss: the loss incurred due to counterparty defaults
        """
        loss = 0
        for key, value in self._traverse_tree(self.exposures_tree):
            if random.random() < probability[key]:
                loss += value * (1 - self.risk_weights[key])
        return loss

    def _build_balanced_tree(self, items):
        """
        Builds a balanced tree from the specified dictionary of items.

        Parameters:
        - items: a dictionary of items, indexed by key

        Returns:
        - root: the root node of the balanced tree
        """
        if not items:
            return None
        keys = list(items.keys())
        keys.sort()
        mid = len(keys) // 2
        return {
            'key': keys[mid],
            'value': items[keys[mid]],
            'left': self._build_balanced_tree({k: v for k, v in items.items() if k < keys[mid]}),
            'right': self._build_balanced_tree({k: v for k, v in items.items() if k > keys[mid]})
        }

    def _traverse_tree(self, root):
        """
        Traverses the specified balanced tree in-order and yields the values in the tree.

        Parameters:
        - root: the root node of the balanced tree

        Yields:
        - (key, value): the key and value of the current node in the tree
        """
        if not root:
            return
        yield from self._traverse_tree(root['left'])
        yield root['key'], root['value']
        yield from self._traverse_tree(root['right'])

    @property
    def exposures(self):
        """
        Property getter for the exposures stored in the CCRRWA instance.

        Returns:
        - exposures: the exposures stored in the CCRRWA instance
        """
        return self._exposures

    @exposures.setter
    def exposures(self, exposures):
        """
        Property setter for the exposures stored in the CCRRWA instance.

        Parameters:
        - exposures: the exposures to store in the CCRRWA instance
        """
        self._exposures = exposures
        self.exposures_tree = self._build_balanced_tree(self._exposures)

    @property
    def risk_weights(self):
        """
        Property getter for the risk weights stored in the
        Returns:
        - exposures: the exposures stored in the CCRRWA instance
        """
        return self._risk_weights

    @risk_weights.setter
    def risk_weights(self, risk_weights):
        """
        Property setter for the risk weights stored in the CCRRWA instance.

        Parameters:
        - risk_weights: the risk weights to store in the CCRRWA instance
        """
        self._risk_weights = risk_weights
        self.risk_weights_tree = self._build_balanced_tree(self._risk_weights)
