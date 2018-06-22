from Trader import *

#Custom settings
LOOP_DURATION = 58.2 # Time period (in seconds)
MAX_LOOP_TIME = 10 * 60 * 60 # Max duration to run (in seconds)
QUOTE_CURRENCY = "BCH" # Cryptocurrency of choice
BASE_CURRENCY = "USD" # Fiat currency of choice
CSV_PRICE = "price.csv" # Price CSV name
CSV_TRANSACTIONS = "transactions.csv" # Transaction CSV name
MODE = 2 # Mode of the Bot
# Authenticate Client Based On Account Credentials
# auth = CoinbaseExchange(key, b64secret, passphrase)

# print auth.getAccounts(QUOTE_CURRENCY)
# print auth.getBalance(QUOTE_CURRENCY)
# print auth.getOrderStatus('asddadsadas')
# print auth.getOrderStatus('79c6dc9d-13b8-4e20-96de-a4afd838baad')
# print auth.getProductId(BASE_CURRENCY, QUOTE_CURRENCY)
# print auth.getPrice('ETH-USD')
# print auth.determinePrice('ETH-USD', 'sell')
# auth.cancelOrder('a63a9772-d783-4a3f-953d-e15924c4435c')
# print auth.sell('BCH-USD', 'yolo', 1900, True)
# print auth.getBalance(QUOTE_CURRENCY)
# print auth.cancelOrders('ETH-USD')
# open_orders = auth.getOrders()
# for item in open_orders:
# 	for stuff in item:
# 		print stuff

	# print auth.cancelOrder(order.get('id'))
# print auth.getProducts()
# print auth.cancelOrder('6cd9475d-d532-4dbd-828a-7ba6704c99c6')

#Start thread
stopFlag = Event()
thread = Trader(stopFlag, LOOP_DURATION, QUOTE_CURRENCY, BASE_CURRENCY, CSV_PRICE, CSV_TRANSACTIONS, MODE)
thread.daemon = True
thread.start()

#Set max time to run
time.sleep(MAX_LOOP_TIME)
stopFlag.set()

