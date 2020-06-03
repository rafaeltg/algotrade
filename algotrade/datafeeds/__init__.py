from .influxdb import InfluxDB
from .yahoo_finance import YahooFinanceData, YahooFinanceCSVData

DATAFEEDS = {
    InfluxDB.__name__: InfluxDB,
    YahooFinanceData.__name__: YahooFinanceData,
    YahooFinanceCSVData.__name__: YahooFinanceCSVData
}
