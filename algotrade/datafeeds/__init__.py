from .influxdb import InfluxDB
from .yahoo_finance import YahooFinanceData

DATAFEEDS = {
    InfluxDB.__name__: InfluxDB,
    YahooFinanceData.__name__: YahooFinanceData
}
