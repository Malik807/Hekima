# Mode 5 : 
# Sell if the 20 day moving average is ahead a multiple of the the 5 day moving average
# Buy if the 5 day moving average is lagging behind a multiple of the 20 day moving average
def momentum(model):
    length = model.ema_dataframe.shape[0]
    if length>20:
        EMA5 = model.ema_dataframe['EMA5'].tail(1).reset_index(drop=True)
        EMA20 = model.ema_dataframe['EMA20'].tail(1).reset_index(drop=True)
        weight = .95
        # Sell if the 20 day moving average is ahead a multiple of the the 5 day moving average
        if (float(EMA5[0]) * weight < float(EMA20[0])):
            signal = {'signal': True, 'value': 'sell'}
        # Buy if the 5 day moving average is lagging behind a multiple of the 20 day moving average
        elif (float(EMA5[0]) < float(EMA20[0]) * weight ):
            signal = {'signal': True, 'value': 'buy'}
        else:
            signal = {'signal': False, 'value': None}
        model.ema_dataframe.loc[model.ema_dataframe.index[length-1], 'signal'] = signal['value']
        model.logPrice(True)
        return signal
    else:
        model.logPrice(True)