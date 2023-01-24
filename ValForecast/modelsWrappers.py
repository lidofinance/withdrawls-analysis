from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX
import statsmodels.api as sm
from pygam import LinearGAM

def ARIMA_fit_prdeict(df_train, df_test, p,d,q):
    ARIMAmodel = ARIMA(df_train['total_deposited'], order=(p, d, q))
    ARIMAmodel = ARIMAmodel.fit()
    y_pred = ARIMAmodel.predict(start=df_test.index[0], end=df_test.index[-1])
    df_test['total_deposited_pred'] = y_pred
    accuracy_score = df_test['total_deposited'][-1:] / df_test['total_deposited_pred'][-1:]
    return accuracy_score

def OLS_fit_prdeict(df_train, df_test, const=False):
    Y = df_train['total_deposited']
    X = pd.DataFrame({'T': df_train.index})
    if const:
        X = sm.add_constant(X)
    model = sm.OLS(Y, X)
    results = model.fit()
    if const:
        accuracy_score = df_test['total_deposited'][-1:] / results.predict([1,df_test['total_deposited'][-1:].index[0]])[0]
    else:
        accuracy_score = df_test['total_deposited'][-1:] / results.predict([df_test['total_deposited'][-1:].index[0]])[0]
    return accuracy_score

def GAM_fit_predict(df_train, df_test):
    df_GAM_train = pd.DataFrame({"Target": df_train['total_deposited'].diff(),
                                 'Lag1': [0, 0] + list(
                                     df_train['total_deposited'].diff()[1:df_train.shape[0] - 1].values),
                                 'Lag2': [0, 0, 0] + list(
                                     df_train['total_deposited'].diff()[1:df_train.shape[0] - 2].values)})

    gam = LinearGAM(n_splines=50).gridsearch(df_GAM_train[['Lag1', 'Lag2']][3:].to_numpy(),
                                              df_GAM_train['Target'][3:].values)
    lag1 = df_GAM_train['Target'].values[-1]
    lag2 = df_GAM_train['Target'].values[-2]
    value = df_train['total_deposited'].values[-1]
    for i in range(df_test.shape[0]):
        predict = gam.predict(np.array([[lag1, lag2], [1, 1]]))
        value = value + predict[0]
        lag2 = lag1
        lag1 = predict[0]

    accuracy_score = df_test['total_deposited'][-1:] / value
    return accuracy_score