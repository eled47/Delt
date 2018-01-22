import abc


class MyExchange(abc.ABC):

    @abc.abstractmethod
    def monitor_order_status(self, order_id):
        pass

    @abc.abstractmethod
    def get_market_price(self, symbol):
        pass

    @abc.abstractmethod
    def get_all_orders(self):
        pass

    @abc.abstractmethod
    def get_all_trades(self):
        pass

    @abc.abstractmethod
    def get_account_stats(self):
        pass

    @abc.abstractmethod
    def get_margin_level(self):
        pass

    @abc.abstractmethod
    def get_balance(self, currency):
        pass

    @abc.abstractmethod
    def request_error_handler(req_func):
        pass

    @abc.abstractmethod
    def open_short_position(self, symbol, amount, leverage):
        pass

    @abc.abstractmethod
    def close_short_position(self, symbol, amount, leverage):
        pass

    @abc.abstractmethod
    def close_short_position_with_id(self, order_id, leverage):
        pass

    @abc.abstractmethod
    def open_long_position(self, symbol, amount, leverage):
        pass

    @abc.abstractmethod
    def close_long_position(self, symbol, amount, leverage):
        pass

    @abc.abstractmethod
    def close_long_position_with_id(self, order_id, leverage):
        pass

    @abc.abstractmethod
    def open_limit_sell_order(self, symbol, amount, price):
        pass

    @abc.abstractmethod
    def open_limit_buy_order(self, symbol, amount, price):
        pass