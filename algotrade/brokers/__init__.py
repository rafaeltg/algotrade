from .backtest import BacktestBroker

BROKERS = {
    BacktestBroker.__name__: BacktestBroker
}
