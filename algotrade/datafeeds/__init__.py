from .yahoo_finance import YahooFinanceData, YahooFinanceCSVData

DATAFEEDS = {
    YahooFinanceData.__name__: YahooFinanceData,
    YahooFinanceCSVData.__name__: YahooFinanceCSVData
}
