<h3>Skimming rewards inflow</h3>
  <b>Model specification & assumptions:</b><br>
Model is calculated by epoch with 256 partial withdrawals per epoch<br>
Validators for partial withdrawals selected by ValidatorIndex, skipping those not eligible<br>
Rotation is accounted in the model - with 16 rotations per block, 512 rotations per epoch. Within model rotations from particular epoch happens simultaneously at the end of that epoch
Order in which rotation are performed are specified within scenarios.<br>
Lido’s rotation is modelled with rotation messages sent as fast as network could handle it<br> 
Validators balances are taken on 18th Jan 2023<br>
Raw data https://drive.google.com/file/d/1WNFML3u66guHEkFkGuk51pW4y3YNowcJ/view <br>
No new Validators or balance growth within the model is assumed, although within skimming loop validators eligible for skimming would be skimmed multiple times according to ValidatorIndex order, representing their presence within skimming limit per epoch<br>
Epochs are aggregated to days with 225 epochs for a day, starting with Day 0, when skimming is enabled<br>
<br>
Rotation scenarios:<br>
Forward index rotation: validators are rotated in order based on validator Index. This scenario represents one of the “worst case” possibilities, delaying skimming rewards for Lido<br>
Backward index rotation: validators are rotated in reversed order based on Validation Index, representing opposite case for previous scenario with minimum delay for Lido due to later rotation of “older” non-Lido validators<br>
Best case scenario: rotation messages are sent only by Lido validators - this scenario provides upper limit on possible skimming inflow with unrealistic assumption on other actors behaviour<br>
  

