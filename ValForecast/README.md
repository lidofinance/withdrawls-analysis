<h3>Beacon chain network state & Lido position scenarios specification</h3>

Within researching protocol stability with proposed withdrawals realisation we’re aiming to cover a broad field of possible scenarios of network state when withdrawals would become available. Goal of this approach is to identify and assert any risks that could rise not only in situations when network growth continues in normal conditions, but also consider edge cases with major shifts to estimate protocol behaviour even in those unlikely scenarios.
<br>
Scenarios on network state are defined in total ETH deposited and total number of validators for beacon chain as a whole and for Lido specifically:<br><br>
<b>1.Expected scenario:</b><br>
Network state on: 01.04<br>
Scenario assumption is normal network developing.<br>
Forecast is generated based on three models: new deposits on beacon chain, Lido share with stETH:ETH exchange rate support model.<br>
Models specifications could be found here:Beacon chain & Lido validators models<br>
*Total deposited: 16 754 850<br>
Total validators: 523 589<br>
Lido deposited: 4 798 408<br>
Lido validators: 149 950*<br>
*Lido share: 28.6%* <br><br>
<b>2.Extreme  growth negative scenario:</b><br>
Network state on: 01.04<br>
Scenario assumption is extreme growth of beacon chain network with new validators entering exactly at churn limit with Lido daily share in new deposits is extremely low (10% quantile of daily share from may 2022 ~ 2%)<br>
*Total deposited: 21 290 727<br>
Total validators: 665 335<br>
Lido deposited: 4 749 914<br>
Lido validators: 148 435*<br>
*Lido share: 22.3%* <br><br>
<b>3.Extreme  growth positive scenario:</b><br>
Network state on: 01.04<br>
Scenario assumption is extreme growth of beacon chain network with new validators entering exactly at churn limit with Lido daily share in new deposits is quite high (70% quantile of daily share from may 2022 on days with mort than 1500 ETH deposited ~ 40%)<br>
*Total deposited: 21 290 727<br>
Total validators: 665 335<br>
Lido deposited: 6 825 427<br>
Lido validators: 213 295*<br>
*Lido share: 32.1%* <br><br>
<b>4.Extreme  stagnation scenario:</b><br>
Network state on: 01.04<br>
Scenario assumption is extreme stagnation of network growth - with zero new validators from 30.12.2022 to 01.04<br>
*Total deposited: 15 840 327<br>
Total validators: 495 010<br>
Lido deposited: 4 635 456<br>
Lido validators: 144 858*<br>
*Lido share: 29.3%* <br><br>
<b>5.Extreme  post-Shanghai scenario:</b><br>
Network state on: 01.06<br>
Scenario assumption is same with extreme stagnation (4) but after withdrawals available validators are exiting exactly at churn limit for two months and half of them are Lido validators<br>
*Total deposited: 13 032 327<br>
Total validators: 407 260<br>
Lido deposited: 3 231 304<br>
Lido validators: 100 983*<br>
*Lido share: 24.8%* <br><br>



<h3>Beacon chain & Lido deposits / validators numbers models specification</h3>
<h4>Purpose of modelling </h4>
<b>Tactical:</b> provide forecast on number of validators on beacon chain and which part of them are working with Lido to estimate necessary parameters of network for stETH rebase model in different scenarios within analysis of potential future withdrawals realisation. Among providing expected numbers, also generate extreme scenarios for testing stability of researched realisation. <br>
<b>Strategical:</b> provide toolbox for forecasting amount of deposits and number of validators in different scenarios as part of the modelling system for analysing queue for withdrawals / deposits, possible impact on Lido stakers and market response after enabling withdrawals.
<h4>Models architecture</h4>
Given goals above, the whole pipeline is divided into 3 models, which were developed and could be improved separately, if necessary.
For each beacon chain and lido model number of possible algorithms was considered and tested. <br>
<h4>Beacon chain deposits / validators number model:</h4>
-Focus was placed on the robustness of the model.<br>
-Resulting model architecture - ARIMA (2, 1, 1)<br>
-Key validation metrics - accuracy of last 2 months of 2022<br>
-Resulting accuracy ~ 0.3%<br>
<h4>Lido deposits / validators number model:</h4>
-To avoid mixing dependant variables within pipeline model is providing forecast for Lido share within daily deposits to beacon chain<br>
-Resulting model architecture - SARIMAX (1, 0, 1) with exogenous stETH/ETH rate<br>
-Key validation metrics - accuracy of last 1.5 months of 2022 (to focus on more stable period after first weeks of November)<br>
-Resulting accuracy ~ 0.2%<br>
<h4>Market model for stETH / ETH</h4>
-Supportive model within tactical goals of pipeline for Lido deposits / validators number model<br>
-Most basic approach for 2023 forecast - steady reversion to 1:1 rate on April 1th<br>
-Could be replaced with more advanced approach (e.g., Hull-White with mean reversion to 1) but at this point - no need for that complexity


<h3>Models selection & calibration</h3>
For both models 3 classes of algorithms were considered within the model pipeline creation process.
For each architecture hyperparameters optimization (lags and weights for AR-models and splines for GAM) were conducted within cross-validation on moving timeframe of 1m through year 2022 (2 months forecast for beacon chain model and 1.5 months for Lido share)
<img src='https://user-images.githubusercontent.com/118216880/214318898-17ea541f-9850-4dd6-b91a-4cf8bc8a3b0c.png'>


