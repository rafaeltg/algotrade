import backtrader as bt
import datetime as dt
from influxdb import InfluxDBClient as idbclient
from influxdb.exceptions import InfluxDBClientError
from .utils import _parse_dates

TIMEFRAMES = dict(
    (
        (bt.TimeFrame.Seconds, 's'),
        (bt.TimeFrame.Minutes, 'm'),
        (bt.TimeFrame.Days, 'd'),
        (bt.TimeFrame.Weeks, 'w'),
        (bt.TimeFrame.Months, 'm'),
        (bt.TimeFrame.Years, 'y'),
    )
)


class InfluxDB(bt.feeds.DataBase):
    lines = ('adjclose',)

    params = (
        ('host', '127.0.0.1'),
        ('port', 8086),
        ('username', None),
        ('password', None),
        ('database', None),
        ('timeframe', bt.TimeFrame.Days),
        ('startdate', None),
        ('high', 'high_p'),
        ('low', 'low_p'),
        ('open', 'open_p'),
        ('close', 'close_p'),
        ('adjclose', 'adjclose_p'),
        ('volume', 'volume'),
    )

    def start(self):
        super(InfluxDB, self).start()
        try:
            self.ndb = idbclient(
                host=self.p.host,
                port=self.p.port,
                username=self.p.username,
                password=self.p.password,
                database=self.p.database
            )
        except InfluxDBClientError as err:
            print('Failed to establish connection to InfluxDB: %s' % err)
            raise err

        tf = '{multiple}{timeframe}'.format(
            multiple=(self.p.compression if self.p.compression else 1),
            timeframe=TIMEFRAMES.get(self.p.timeframe, 'd'))

        if not self.p.startdate:
            st = '<= now()'
        else:
            st = '>= \'%s\'' % self.p.startdate

        # The query could already consider parameters like fromdate and todate
        # to have the database skip them and not the internal code
        qstr = ('SELECT first("{open_f}") AS "open", '
                'max("{high_f}") AS "high", '
                'min("{low_f}") AS "low", '
                'last("{close_f}") AS "close", '
                'sum("{vol_f}") AS "volume", '
                'last("{adjclose_f}") AS "adjclose" '
                'FROM "{dataname}" '
                'WHERE time {begin} '
                'GROUP BY time({timeframe}) fill(none)').format(
            open_f=self.p.open,
            high_f=self.p.high,
            low_f=self.p.low,
            close_f=self.p.close,
            vol_f=self.p.volume,
            adjclose_f=self.p.adjclose,
            dataname=self.p.dataname,
            timeframe=tf,
            begin=st)

        print(qstr)

        try:
            dbars = list(self.ndb.query(qstr).get_points())
        except InfluxDBClientError as err:
            print('InfluxDB query failed: %s' % err)
            raise err

        self.biter = iter(dbars)

    def _load(self):
        try:
            bar = next(self.biter)
        except StopIteration:
            return False

        self.l.datetime[0] = bt.date2num(dt.datetime.strptime(bar['time'], '%Y-%m-%dT%H:%M:%SZ'))

        self.l.open[0] = bar['open']
        self.l.high[0] = bar['high']
        self.l.low[0] = bar['low']
        self.l.close[0] = bar['close']
        self.l.adjclose[0] = bar['adjclose']
        self.l.volume[0] = bar['volume']

        return True

    @classmethod
    def from_config(cls, **config):
        return cls(**_parse_dates(config))
