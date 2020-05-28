import io
import requests
import backtrader as bt
import datetime as dt


class YahooFinanceData(bt.feeds.YahooFinanceData):

    def start_v7(self):
        self.error = None
        url = self.p.urlhist.format(self.p.dataname)

        sesskwargs = dict()
        if self.p.proxies:
            sesskwargs['proxies'] = self.p.proxies

        crumb = None
        sess = requests.Session()
        for i in range(self.p.retries + 1):  # at least once
            resp = sess.get(url, **sesskwargs)
            if resp.status_code != requests.codes.ok:
                continue

            txt = resp.text
            i = txt.find('CrumbStore')
            if i == -1:
                continue
            i = txt.find('crumb', i)
            if i == -1:
                continue
            istart = txt.find('"', i + len('crumb') + 1)
            if istart == -1:
                continue
            istart += 1
            iend = txt.find('"', istart)
            if iend == -1:
                continue

            crumb = txt[istart:iend]
            crumb = crumb.encode('ascii').decode('unicode-escape')
            break

        if crumb is None:
            self.error = 'Crumb not found'
            self.f = None
            return

        # urldown/ticker?period1=posix1&period2=posix2&interval=1d&events=history&crumb=crumb

        # Try to download
        urld = '{}/{}'.format(self.p.urldown, self.p.dataname)

        urlargs = []
        posix = dt.date(1970, 1, 1)
        if self.p.fromdate is not None:
            period1 = (self.p.fromdate.date() - posix).total_seconds()
            urlargs.append('period1={}'.format(int(period1)))

        if self.p.todate is not None:
            period2 = (self.p.todate.date() - posix).total_seconds()
            urlargs.append('period2={}'.format(int(period2)))

        intervals = {
            bt.TimeFrame.Days: '1d',
            bt.TimeFrame.Weeks: '1wk',
            bt.TimeFrame.Months: '1mo',
        }

        urlargs.append('interval={}'.format(intervals[self.p.timeframe]))
        urlargs.append('events=history')
        urlargs.append('crumb={}'.format(crumb))

        urld = '{}?{}'.format(urld, '&'.join(urlargs))
        f = None
        for i in range(self.p.retries + 1):  # at least once
            resp = sess.get(urld, **sesskwargs)
            if resp.status_code != requests.codes.ok:
                continue

            ctype = resp.headers['Content-Type']
            if 'text/plain' not in ctype:
                self.error = 'Wrong content type: %s' % ctype
                continue  # HTML returned? wrong url?

            # buffer everything from the socket into a local buffer
            try:
                # r.encoding = 'UTF-8'
                f = io.StringIO(resp.text, newline=None)
            except Exception:
                continue  # try again if possible

            break

        self.f = f

    def to_config(self) -> dict:
        config = self.params._getitems()
        config['fromdate'] = self.params.fromdate.strftime('%Y-%m-%d')
        config['enddate'] = self.params.todate.strftime('%Y-%m-%d')
        return config

    @classmethod
    def from_config(cls, **config):
        fromdate = config.pop('fromdate', None)
        if fromdate is not None:
            fromdate = dt.datetime.strptime(fromdate, '%Y-%m-%d')

        todate = config.pop('todate', None)
        if todate is not None:
            todate = dt.datetime.strptime(todate, '%Y-%m-%d')

        return cls(fromdate=fromdate, todate=todate, **config)
