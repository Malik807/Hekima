# Mode 3 : Buy when RSI < 10 and sell when RSI > 80
def rsi(model):
    length = model.ema_dataframe.shape[0]
    if length>26:
        RSI = model.ema_dataframe['RSI'].tail(1).reset_index(drop=True)
        if (RSI[0] >= 80):
            signal = {'signal': True, 'value': 'sell'}
        elif (RSI[0] <= 15):
            signal = {'signal': True, 'value': 'buy'}
        else:
            signal = {'signal': False, 'value': None}
        model.ema_dataframe.loc[model.ema_dataframe.index[length-1], 'signal'] = signal['value']
        model.logPrice(True)
        return signal
    else:
        model.logPrice(True)