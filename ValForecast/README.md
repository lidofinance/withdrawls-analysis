<h3>Beacon chain & Lido deposits / validators numbers models specification</h3>
<h1>Purpose of modelling </h1>
Tactical: provide forecast on number of validators on beacon chain and which part of them are working with Lido to estimate necessary parameters of network for stETH rebase model in different scenarios within analysis of potential future withdrawals realisation. Among providing expected numbers, also generate extreme scenarios for testing stability of researched realisation.
Strategical: provide toolbox for forecasting amount of deposits and number of validators in different scenarios as part of the modelling system for analysing queue for withdrawals / deposits, possible impact on Lido stakers and market response after enabling withdrawals.
<h1>Models architecture</h1>
Given goals above, the whole pipeline is divided into 3 models, which were developed and could be improved separately, if necessary.
For each beacon chain and lido model number of possible algorithms was considered and tested. Additional information on that could be found in Models selection & calibration
Beacon chain deposits / validators number model:
-Focus was placed on the robustness of the model.
-Resulting model architecture - ARIMA (2, 1, 1)
-Key validation metrics - accuracy of last 2 months of 2022
-Resulting accuracy ~ 0.3%
Lido deposits / validators number model:
-To avoid mixing dependant variables within pipeline model is providing forecast for Lido share within daily deposits to beacon chain
-Resulting model architecture - SARIMAX (1, 0, 1) with exogenous stETH/ETH rate
-Key validation metrics - accuracy of last 1.5 months of 2022 (to focus on more stable period after first weeks of November)
-Resulting accuracy ~ 0.2%
Market model for stETH / ETH
-Supportive model within tactical goals of pipeline for Lido deposits / validators number model
-Most basic approach for 2023 forecast - steady reversion to 1:1 rate on April 1th
-Could be replaced with more advanced approach (e.g., Hull-White with mean reversion to 1) but at this point - no need for that complexity
