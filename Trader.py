import time
from threading import Event, Thread
from CoinBase import *
from Functions import *
from config import *

class Trader(Thread):
	#Class used to log price, calculate EMA & Crossover and then trigger a separate thread to
	#buy/sell the chosen cryptocurrency
	def __init__(self, event, wait_time, quote_currency, base_currency, csv_price, csv_transactions, mode):
		Thread.__init__(self)
		self.stopped = event
		self.wait_time = wait_time
		self.quote_currency = quote_currency
		self.base_currency = base_currency
		self.mode = mode
		#Authenticate details
		self.CoinBase = CoinbaseExchange(key, b64secret, passphrase)
		#Create model
		self.model = Model(csv_price, csv_transactions)
		#Choose Product
		self.product_id = self.CoinBase.getProductId(self.quote_currency, self.base_currency)
		#Specify timeout duration
		self.order_timeout = 10 * 60 #10 minutes (in seconds)
		#Display welcome message
		print('Running...')

	def run(self):
		#Run until stopped by stopped by Admin, waiting at set intervals
		while not self.stopped.wait(self.wait_time):
			self.Trade() # Pass mode for bot to utilize (etc 1)

	def order(self, type):
		if (type == 'sell'):
			#Sell product
			#Get all open orders and cancel
			open_orders = self.CoinBase.getOrders()
			if(len(open_orders) > 0):
				for orders in open_orders:
					for order in orders:
						self.CoinBase.cancelOrder(order.get('id'))

			current_balance = float(self.CoinBase.getBalance(self.quote_currency))
			if current_balance > 0:
				#Sell current position
				order = self.model.sell(self.product_id, self.CoinBase, self.quote_currency, self.base_currency)
				order_time = order['created_at']
				order_id = order['id']
				price = order['price']
				print('Time: {}, Order: Sell, Price:{}, Status: {}'.format(order_time, price, order['status']))
				timer_count = 0
				while True:
					#Cancel order if timeout
					if timer_count > self.order_timeout:
						self.CoinBase.cancelOrder(order_id)
						time_now = self.CoinBase.getTime()
						print('Time: {}, Time limit exceeded, order cancelled'.format(time_now))
						break
					order_status = self.CoinBase.getOrderStatus(order_id)

					#Return success message if order successful
					if order_status == 'done':
						time_now = self.CoinBase.getTime()
						print('Time: {}, Sell fulfilled at {}'.format(time_now, order['price']))
						break
					time.sleep(1)
					timer_count = timer_count + 1
			else:
				order_time = self.CoinBase.getTime()
				print('Time: {}, Order: Sell, No currency available.'.format(order_time))
			
		elif (type == 'buy'):
			current_balance = float(self.CoinBase.getBalance(self.base_currency))
			if current_balance > 0:
				#Buy product
				order = self.model.buy(self.product_id, self.CoinBase, self.base_currency)
				order_time = order['created_at']
				order_id = order['id']
				price = order['price']
				print('Time: {}, Order: Buy, Price:{},  Status: {}'.format(order_time, price, order['status']))

				timer_count = 0
				while True:
					#Cancel order if timeout
					order_status = self.CoinBase.getOrderStatus(order_id)
					if timer_count > self.order_timeout:
						self.CoinBase.cancelOrder(order_id)
						time_now = self.CoinBase.getTime()
						print('Time: {}, Time limit exceeded, order cancelled'.format(time_now))
						break
					if order_status == 'done':
						time_now = self.CoinBase.getTime()
						print('Time: {}, Buy fulfilled at {}'.format(time_now, order['price']))
						break
					time.sleep(1)
					timer_count = timer_count + 1
			else:
				order_time = self.CoinBase.getTime()
				print('Time: {}, Order: Buy, No currency available.'.format(order_time))

	def Trade(self):
		# Grab data for bot use
		self.model.calculateEma(self.CoinBase, self.product_id)
		self.model.calculateRSI(12)
		signal = self.model.initStrategy(self.mode)

		if signal is not None:
			if signal['value'] == 'buy':
				order_thread = Thread(target=self.order, args=('buy',))
				order_thread.daemon = True
				order_thread.start()
				# print 'Buy Stuff'
			elif signal['value'] == 'sell':
				order_thread = Thread(target=self.order, args=('sell',))
				order_thread.daemon = True
				order_thread.start()
				# print 'Sell Stuff'