# Mode 1 : Calculate EMA crossover and return signal
def calculateCrossover(model):
    length = model.ema_dataframe.shape[0]
    if length>5:
        EMA5 = model.ema_dataframe['EMA5'].tail(2).reset_index(drop=True)
        EMA20 = model.ema_dataframe['EMA20'].tail(2).reset_index(drop=True)
        if (EMA5[1] <= EMA20[1]) and (EMA5[0] >= EMA20[0]):
            signal = {'signal': True, 'value': 'sell'}
        elif (EMA5[1] >= EMA20[1]) and (EMA5[0] <= EMA20[0]):
            signal = {'signal': True, 'value': 'buy'}
        else:
            signal = {'signal': False, 'value': None}
        model.ema_dataframe.loc[model.ema_dataframe.index[length-1], 'signal'] = signal['value']
        model.logPrice(True)
        return signal
    else:
        model.logPrice(True)