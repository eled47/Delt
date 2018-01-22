from my_kraken import MyKraken 
from my_binance import MyBinance  

kraken = MyKraken()
binance = MyBinance()



def check_prices(symbol, min_profit_margin):
	eth_price_kraken = kraken.get_market_price(symbol)["ask"]
	eth_price_binance = binance.get_market_price(symbol)["ask"]
	spread = eth_price_kraken - eth_price_binance

	if (min_profit_margin <= spread):
		return "Spread isn't good enough"












