import pandas as pd
import matplotlib.pyplot as plt

MAX_PARTIAL_WITHDRAWALS_PER_EPOCH = 2**8
MAX_BLS_TO_EXECUTION_CHANGES = 2**4
BLOCKS_IN_EPOCH = 2**5
WC_CHANGES_IN_EPOCH = MAX_BLS_TO_EXECUTION_CHANGES*BLOCKS_IN_EPOCH

valdatafull = pd.read_csv('Valdata.csv', sep=',')
power_level = 10**9
valdatafull['wc_type'] = [x[1:4] for x in valdatafull['f_withdrawal_credentials']]
valdatafull['wc_type'].unique()
valdatafull = valdatafull.sort_values(by='f_validator_index')
valdatafull = valdatafull.reset_index()

valdatafull = valdatafull[valdatafull['skimmable_balance']>0]
valdatafull = valdatafull.drop(columns='index')
valdatafull = valdatafull.reset_index()

epoch = 1
valdatafull['skimmed_value'] = 0
valdatafull['epoch'] = 0
validafullLido = valdatafull[valdatafull['belong']=='Lido']
while epoch < 5000:
    skim_index = valdatafull[(valdatafull['wc_type'] == 'x01') & (valdatafull['skimmed_value']==0)][:MAX_PARTIAL_WITHDRAWALS_PER_EPOCH].index
    skimmable_balance = valdatafull['skimmable_balance'][skim_index].values
    valdatafull.iloc[skim_index, [7, 8]] = [skimmable_balance, epoch]
    #Backwards scenario
    #wc_change_index = valdatafull[valdatafull['wc_type'] == 'x00'][-WC_CHANGES_IN_EPOCH:].index
    #Forwards scenario
    #wc_change_index = valdatafull[valdatafull['wc_type'] == 'x00'][:WC_CHANGES_IN_EPOCH].index
    #Best case scenario
    wc_change_index = validafullLido[validafullLido['wc_type'] == 'x00'][:WC_CHANGES_IN_EPOCH].index
    validafullOthers = valdatafull[valdatafull['belong'] == 'Other']
    validafullLido = valdatafull[valdatafull['belong'] == 'Lido']
    valdatafull.iloc[wc_change_index, 6] = 'x01'
    epoch = epoch+1
    if (epoch % 100) ==0:
        print(epoch)
    if len(valdatafull[valdatafull['skimmed_value']==0])==0:
        epoch = 9999
    if len(validafullLido[validafullLido['skimmed_value']==0])==0:
        epoch = 9999