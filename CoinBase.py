import datetime, gdax

class CoinbaseExchange(object):
    #Class used to perform different actions on the GDAX API
    def __init__(self, api_key, secret_key, passphrase):
        self.auth = gdax.AuthenticatedClient(api_key, secret_key, passphrase)

    def getTime(self):
        request = self.auth.get_time()
        time = request.get('epoch')
        time_dt = datetime.datetime.fromtimestamp(time).strftime('%Y-%m-%d %H:%M:%S')
        return time_dt

    def getAccounts(self, quote_currency):
        request = self.auth.get_accounts() 
        # #Find index corresponding to pair
        index = next(index for (index, d) in enumerate(request) if ((d.get('currency') == quote_currency)))
        account = request[index].get('id')
        return account

    def getOrderStatus(self, order_id):
        request = self.auth.get_order(order_id)
        if request.get('message') == 'Invalid order id':
            # A 404 was issued - order doesnt exist
            print('Order ID does not exist')
            return False
        else:
            status = request.get('status')
            return status

    def getBalance(self, currency):
        request = self.auth.get_accounts() 
        # #Find index corresponding to pair
        index = next(index for (index, d) in enumerate(request) if ((d.get('currency') == currency)))
        account = request[index].get('balance')
        return account

    def getProductId(self, base_currency, quote_currency):
        request = self.auth.get_products()
        # #Find index corresponding to pair
        try:
            index = next(index for (index, d) in enumerate(request) if ((d.get('base_currency') == base_currency) and (d.get('quote_currency') == quote_currency)))
            product_id = request[index].get('id')
        except StopIteration:
            print("StopIteration Error... Defaulting to BCH-USD")
            product_id = 'BCH-USD'
        except:
            print("Something else went wrong... Defaulting to BCH-USD")
            product_id = 'BCH-USD'
        return product_id

    def getPrice(self, product_id):
        request = self.auth.get_product_ticker(product_id = product_id)
        price = request.get('price')
        return price

    def determinePrice(self, product_id, option):
        request = self.auth.get_product_order_book(product_id, level=1)
        if option == 'buy':
            buy_price = float(request.get('bids')[0][0]) - 0.01
            return buy_price
        if option == 'sell':
            sell_price = float(request.get('asks')[0][0]) + 0.01
            return sell_price

    def buy(self, product_id, quantity, price):
        #Rounded down to 7dp
        quantity = (quantity // 0.0000001) / 10000000

        request = self.auth.buy(type= 'limit',
                        size = quantity,
                        price = price, 
                        side= 'buy',
                        product_id = product_id,
                        time_in_force = 'GTC',
                        post_only = True)
        return request

    def sell(self, product_id, quantity, price, upper):
        #Round price to 2DP
        price = round(float(price), 2)       
        if upper is True:
            request = self.auth.sell(type= 'limit',
                        size = quantity,
                        price = price, 
                        side= 'sell',
                        product_id = product_id,
                        time_in_force = 'GTC',
                        post_only = True)
        else:
            time_to_cancel = 'hour'
            request = self.auth.sell(type= 'limit',
                        size = quantity,
                        price = price, 
                        side= 'sell',
                        product_id = product_id,
                        time_in_force = 'GTT',
                        cancel_after = time_to_cancel,
                        post_only = True)
        return request

    def cancelOrder(self, order_id):
        request = self.auth.cancel_order(order_id)
        if isinstance(request, dict):
            print request.get('message')
            return False
        else:
            return True

    #TODO Fix this Function
    def cancelAllOrders(self, product_id):
        request = self.auth.cancel_all(product_id='BTC-USD')
        return request

    def getOrders(self):
        request = self.auth.get_orders()
        return request

    def getFills(self, product_id):
        request = self.auth.get_fills(product_id = product_id)
        return request