import matplotlib.pyplot as plt
import pandas as pd

from modelsWrappers import ARIMA_fit_prdeict
from modelsWrappers import OLS_fit_prdeict
from modelsWrappers import GAM_fit_predict

from DataCollection import get_dune_data

query_id = 95814 #@LidoAnalytical / ETH staked with Lido

df = get_dune_data(query_id,'hGaVTaG1o8FEdHOg9U1h2XJvtLI74SuF')
df['date'] = pd.to_datetime(df['time'], format='%Y-%m-%d')

query_id_curve = 100870 #@LidoAnalytical / stETH on Curve
stETHprice = get_dune_data(query_id_curve ,'hGaVTaG1o8FEdHOg9U1h2XJvtLI74SuF')
stETHprice['time'] = pd.to_datetime(stETHprice['time'] , format='%Y-%m-%d')

df = df[df['date'] < '2023-01-01']
df_train = df[df.date < "2022-11-01"]
df_test = df[df.date >= "2022-11-01"]




diff_arima_arch_results = pd.DataFrame()
for p in range(5):
    for d in range(5):
        for q in range(5):
            print(str(p)+" " + str(d) + " " + str(q))
            result = ARIMA_fit_prdeict(df_train, df_test, p,d,q)
            print(result)
            diff_arima_arch_results = diff_arima_arch_results.append({'p':p,
                                                                      'd':d,
                                                                      'q':q,
                                                                      'score':result.values[0]},
                                                                     ignore_index=1)
diff_arima_arch_results['score_sqared'] = (diff_arima_arch_results['score']-1)**2
arima_arch_sorted = diff_arima_arch_results.sort_values(by='score_sqared')
arima_arch_sortedD1 = arima_arch_sorted[arima_arch_sorted.d==1]

fig = plt.figure()
ax = fig.add_subplot(projection='3d')
ax.scatter(arima_arch_sortedD1.p, arima_arch_sortedD1.q, arima_arch_sortedD1.score_sqared)
plt.show()



p = 2
d = 1
q = 1
lag = 0
train_index = df_train.index[-1]
df_cross_arima_result = pd.DataFrame()
pred_dict = {}
while lag < 360:
    df_cross_train = df[:train_index-lag]
    df_cross_test = df[train_index-lag+1:train_index-lag+len(df_test)]
    result2 = ARIMA_fit_prdeict(df_cross_train, df_cross_test, p, d, q)
    result = result2['accuracy_score']
    pred_dict[lag] = result2['y_pred']
    print(lag)
    print(result)
    df_cross_arima_result = df_cross_arima_result.append({'traind_end':df_cross_train['date'].values[-1],
                                                          'test_end': df_cross_test['date'].values[-1],
                                                          'score':result.values[0]},
                                                         ignore_index=1)
    lag +=30

plt.plot(df_cross_arima_result['test_end'], df_cross_arima_result['score'])


#cross valid graph
#plt.plot(df['date'][370:], df['total_deposited'][370:], label = 'fact')
plt.plot(df['date'], df['total_deposited'], label = 'fact')
for l in pred_dict:
    y_pred_df = pred_dict[l]
    plt.plot(y_pred_df['date'], y_pred_df['y_pred'], label = y_pred_df['date'].values[0])

#y_pred_df = result2['y_pred']
#plt.plot(y_pred_df['date'], y_pred_df['y_pred'])
plt.ylabel('Beacon Сhain depostits')
plt.xlabel('Date')
#plt.xticks(rotation=45)
#plt.title("Train/Test split")
#plt.legend()
plt.show()

df_cross_ols_result = pd.DataFrame()
lag = 0
while lag < 360:
    df_cross_train = df[:train_index-lag]
    df_cross_test = df[train_index-lag+1:train_index-lag+len(df_test)]
    result = OLS_fit_prdeict(df_cross_train, df_cross_test)
    resultConst = OLS_fit_prdeict(df_cross_train, df_cross_test, const = True)
    print(lag)
    print(result)
    df_cross_ols_result = df_cross_ols_result.append({'traind_end':df_cross_train['date'].values[-1],
                                                            'test_end': df_cross_test['date'].values[-1],
                                                            'score':result,
                                                            'scoreConst':resultConst},
                                                        ignore_index=1)
    lag +=30

plt.plot(df_cross_arima_result['test_end'], df_cross_arima_result['score'], label = 'ARIMA (2,1,1)')
plt.plot(df_cross_ols_result['test_end'], df_cross_ols_result['score'], label = 'OLS no constant')
plt.plot(df_cross_ols_result['test_end'], df_cross_ols_result['scoreConst'], label = 'OLS with constant')
plt.legend()
plt.show()

df_cross_GAM_result = pd.DataFrame()
lag = 0
while lag < 360:
    df_cross_train = df[:train_index-lag]
    df_cross_test = df[train_index-lag+1:train_index-lag+len(df_test)]
    result = GAM_fit_predict(df_cross_train, df_cross_test)
    print(lag)
    print(result)
    df_cross_GAM_result = df_cross_GAM_result.append({'traind_end':df_cross_train['date'].values[-1],
                                                            'test_end': df_cross_test['date'].values[-1],
                                                            'score':result},
                                                        ignore_index=1)
    lag +=30

plt.plot(df_cross_arima_result['test_end'], df_cross_arima_result['score'], label = 'ARIMA (2,1,1)')
plt.plot(df_cross_ols_result['test_end'], df_cross_ols_result['score'], label = 'OLS no constant')
plt.plot(df_cross_ols_result['test_end'], df_cross_ols_result['scoreConst'], label = 'OLS with constant')
plt.plot(df_cross_GAM_result['test_end'], df_cross_GAM_result['score'], label = 'GAM')
plt.ylabel('Actual / Forecast')
plt.xlabel('Last date on test sample')
plt.legend()
plt.show()

cross_results = df_cross_arima_result.merge(df_cross_ols_result[['test_end','score','scoreConst']], on='test_end')
cross_results = cross_results.merge(df_cross_GAM_result[['test_end','score']],  on='test_end')
cross_results.score_y = cross_results.score_y.astype('float')
cross_results.scoreConst = cross_results.scoreConst.astype('float')
cross_results.score = cross_results.score.astype('float')
cross_results.to_excel('Cross.xlsx')







