# Mode 2 : Buy when (EMA - last(EMA) > 0) and sell when (EMA - last(EMA) < 0). Optional buy on low RSI.
def trend_ema(model):
    length = model.ema_dataframe.shape[0]
    if length>12:
        EMA5 = model.ema_dataframe['EMA5'].tail(2).reset_index(drop=True)
        EMA12 = model.ema_dataframe['EMA12'].tail(2).reset_index(drop=True)
        RSI = model.ema_dataframe['RSI'].tail(1).reset_index(drop=True)
        if (EMA5[1] - EMA5[0] < 0):
            signal = {'signal': True, 'value': 'sell'}
        elif (EMA12[1] - EMA12[0] >= 0) or (RSI[0] <= 15):
            signal = {'signal': True, 'value': 'buy'}
        else:
            signal = {'signal': False, 'value': None}
        model.ema_dataframe.loc[model.ema_dataframe.index[length-1], 'signal'] = signal['value']
        model.logPrice(True)
        return signal
    else:
        model.logPrice(True)