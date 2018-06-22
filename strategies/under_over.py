# Mode 4 : Buy when price is .3% under EMA. Sell when price is .2 over EMA
def under_over(model):
    length = model.ema_dataframe.shape[0]
    if length>26:
        price = model.ema_dataframe['price'].tail(1).reset_index(drop=True)
        EMA26 = model.ema_dataframe['EMA26'].tail(1).reset_index(drop=True)
        under = float(EMA26[0]) * .99 # 1% below EM26
        over = float(EMA26[0]) * 1.025 # 1.025% above EM26
        price = float(price[0])
        if (price - over > 0 ):
            signal = {'signal': True, 'value': 'sell'}
        elif (price - under < 0):
            signal = {'signal': True, 'value': 'buy'}
        else:
            signal = {'signal': False, 'value': None}
        model.ema_dataframe.loc[model.ema_dataframe.index[length-1], 'signal'] = signal['value']
        model.logPrice(True)
        return signal
    else:
        model.logPrice(True)