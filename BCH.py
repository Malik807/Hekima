from Trader import *

#Custom settings
LOOP_DURATION = 3 * 60 # Time period (in seconds)
MAX_LOOP_TIME = 10 * 24 * 60 * 60 # Max duration to run (in seconds)
QUOTE_CURRENCY = "BCH" # Cryptocurrency of choice
BASE_CURRENCY = "USD" # Fiat currency of choice
CSV_PRICE = "BCH_price.csv" # Price CSV name
CSV_TRANSACTIONS = "BCH_transactions.csv" # Transaction CSV name
MODE = 4 # Mode of the Bot

#Start thread
stopFlag = Event()
thread = Trader(stopFlag, LOOP_DURATION, QUOTE_CURRENCY, BASE_CURRENCY, CSV_PRICE, CSV_TRANSACTIONS, MODE)
thread.daemon = True
thread.start()

#Set max time to run
time.sleep(MAX_LOOP_TIME)
stopFlag.set()