import backtrader as bt
from .brokers import BROKERS
from .datafeeds import DATAFEEDS
from .strategies import STRATEGIES
from .sizers import SIZERS
from .analyzers import ANALYZERS
from .utils import from_config


class Session(bt.Cerebro):

    def get_config(self):
        cfg = {
            'data': [
                {
                    'class_name': d.__class__.__name__,
                    'config': d.get_config()
                } for d in self.datas
            ],
            'broker': {
                'class_name': self.broker.__class__.__name__,
                'config': self.broker.get_config()
            },
            'strategy': [
                {
                    'class_name': s.__class__.__name__,
                    'config': s.get_config()
                } for s in self.strats
            ]
        }

        return cfg

    @classmethod
    def from_config(cls, **cfg):
        sess = cls()
        sess._set_data(cfg.get('data', None))
        sess._set_broker(cfg.get('broker', None))
        sess._set_strategy(cfg.get('strategy', None))
        sess._set_strategy(cfg.get('sizers', None))
        sess._set_analyzers(cfg.get('analyzers', None))
        return sess

    def _set_data(self, data):
        if data is None:
            return

        if not isinstance(data, list):
            data = [data]

        for d in data:
            df = from_config(config=d, **DATAFEEDS)
            if df is not None:
                self.adddata(df)

    def _set_broker(self, b: dict):
        if b is None:
            return

        self.broker = from_config(config=b, **BROKERS)

    def _set_strategy(self, strat):
        if strat is None:
            return

        if not isinstance(strat, list):
            strat = [strat]

        for s in strat:
            if 'class_name' in s:
                strat_cls = STRATEGIES.get(s['class_name'], None)
                if strat_cls is not None:
                    params = s.get('params', dict())
                    self.addstrategy(strat_cls, **params)

    def _set_sizers(self, sizers):
        if sizers is None:
            return

        if not isinstance(sizers, list):
            sizers = [sizers]

        for s in sizers:
            if 'class_name' in s:
                sizer_cls = SIZERS.get(s['class_name'], None)
                if sizer_cls is not None:
                    params = s.get('params', dict())

                    if 'start_idx' in s:
                        self.addsizer_byidx(idx=int(s['start_idx']), sizercls=sizer_cls, **params)
                    else:
                        self.addsizer(sizercls=sizer_cls, **params)

    def _set_analyzers(self, analyzers):
        if analyzers is None:
            return

        if not isinstance(analyzers, list):
            analyzers = [analyzers]

        for a in analyzers:
            if 'class_name' in a:
                an_cls = ANALYZERS.get(a['class_name'], None)
                if an_cls is not None:
                    params = a.get('params', dict())
                    self.addanalyzer(an_cls, **params)
