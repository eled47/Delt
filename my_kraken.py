import threading
import time
from ccxt.kraken import kraken
from ccxt.base.errors import NetworkError
from ccxt.base.errors import ExchangeError
from my_exchange import MyExchange
import config



class MyKraken(MyExchange, kraken):

    def __init__(self):
        super(MyKraken, self).__init__()
        self.apiKey = config.api_key
        self.secret = config.api_secret
        self.markets = self.load_markets()
        self.timeout = 60000  # extend request timeout to 1 min
        self.enableRateLimit = True

    def get_all_orders(self):
        pass

    def get_all_trades(self):
        pass

    def request_error_handler(req_func):
        def new_func(self, *args):
            attempts = 0
            print(req_func.__name__, "| Sending request. Please wait...")
            while attempts < 5:
                try:
                    attempts += 1
                    resp = req_func(self, *args)
                    print("Request successful. Response: ", resp)
                    return resp
                except NetworkError as error:
                    print(error, "Problem encountered with network. " +
                          "Resubmitting request...")
                except ExchangeError as error:
                    print(error, "Problem encountered with exchange. Request" +
                          " unsuccessful.")
                    break
        return new_func

    def order_status_worker(self, order_id):
        print(threading.current_thread().getName(), "| Starting new order" +
              " status thread. Please wait...")
        completed = False
        attempts = 0
        while (completed is False) and (attempts < 10):
            attempts += 1
            status = self.fetch_order_status(order_id)
            if status == "closed":
                completed = True
            else:
                time.sleep(10)
        print("Exiting thread...", threading.current_thread().getName())

    @request_error_handler
    def monitor_order_status(self, order_id):
        new_thread = threading.Thread(
            name=order_id, target=self.order_status_worker, args=(order_id,))
        new_thread.start()
        # TODO(vernon): Return final status of order

    @request_error_handler
    def get_market_price(self, symbol):
        orderbook = self.fetch_order_book(symbol, {'depth': 1})
        bids = orderbook['bids']
        asks = orderbook['asks']
        bid = bids[0][0] if len(bids) > 0 else None
        ask = asks[0][0] if len(asks) > 0 else None
        spread = (ask - bid) if (bid and ask) else None
        return {'symbol': symbol, 'bid': bid, 'ask': ask, 'spread': spread}

    @request_error_handler
    def get_balance(self, currency=None):
        balances = self.fetch_total_balance()
        if currency:
            if currency in balances.keys():
                return balances[currency]
        else:
            return balances

    
    @request_error_handler
    def open_short_position(self, symbol, amount, leverage=2):
        return self.create_market_sell_order(symbol, amount, {
            'leverage': leverage
        })

    @request_error_handler
    def close_short_position(self, symbol, amount, leverage=2):
        return self.create_market_buy_order(symbol, amount, {
            'leverage': leverage
        })

    @request_error_handler
    def close_short_position_with_id(self, order_id, leverage=2):
        order = self.fetch_order(order_id)
        return self.create_market_buy_order(order.symbol, order.amount, {
            'leverage': leverage
        })

    @request_error_handler
    def open_long_position(self, symbol, amount, leverage='none'):
        return self.create_market_buy_order(symbol, amount, {
            'leverage': leverage
        })

    @request_error_handler
    def close_long_position(self, symbol, amount, leverage='none'):
        return self.create_market_sell_order(symbol, amount, {
            'leverage': leverage
        })

    @request_error_handler
    def close_long_position_with_id(self, order_id, leverage=2):
        order = self.fetch_order(order_id)
        return self.create_market_sell_order(order.symbol, order.amount, {
            'leverage': leverage
        })

    @request_error_handler
    def open_limit_sell_order(self, symbol, amount, price):
        return self.create_limit_sell_order(symbol, amount, price)

    @request_error_handler
    def open_limit_buy_order(self, symbol, amount, price):
        return self.create_limit_buy_order(symbol, amount, price)

    @request_error_handler
    def get_margin_level(self):
        trade_balance = self.private_post_tradebalance()['result']
        if 'ml' in trade_balance.keys():
            return trade_balance['ml']

    @request_error_handler
    def get_account_stats(self):
        """
            Returns:
                dict: Mapping of trade balance statistics
                    eb: equivalent balance
                    tb: trade balance
                    m: margin amount of open positions
                    n: unrealized net profit/loss of open positions
                    c: cost basis of open positions
                    v: current floating valuation of open positions
                    e: equity = trade balance + unrealized net profit/loss
                    mf: free margin = equity - initial margin
                    ml: margin level = (equity / initial margin) * 100
        """
        return self.private_post_tradebalance()['result']
