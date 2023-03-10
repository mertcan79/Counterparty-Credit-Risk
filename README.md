# Counterparty Credit Risk

**CCR is calculated in two different methods, namely SA-CCRA and CCR RWA, and compared.**

CCR models are relatively new to the Basel framework (Basel II for IMM and Basel III for CVA risk capital charge).
They are generally viewed as complex models that require substantial development effort and the availability of sophisticated IT systems.

The standardized approach for measuring counterparty credit risk exposures” (SA-CCR), the final standard for the calculation of counterparty credit risk of derivatives portfolios is compared to CCR RWA method with same data. Traverse trees are used for better performance.

Risk mitigation parameters are added to both SA-CCR and CCR-RWA classes on top of standard exposure and risk weights.

For CCR RWA they are: PD, LGD, IRR, Credit risk, Liquidity risk and recovery rates.
For SA-CCR they are: PFE, netting sets, risk mitigation.

An example demonstration of the test file, which has real world data, can be seen here:

![alt text](ccr_test.png)
