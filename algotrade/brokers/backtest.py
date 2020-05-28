import backtrader as bt


class BacktestBroker(bt.brokers.BackBroker):

    def get_config(self) -> dict:
        ret = {
            'cash': self.get_cash(),
            'startingcash': self.startingcash,
            'commission': self._get_commission_config()
        }

        return ret

    def _get_commission_config(self) -> list:
        ret = []

        for k, v in self.comminfo.items():
            ret.append(dict(
                commission=v.p.commission,
                margin=v.p.margin,
                mult=v.p.mult,
                commtype=v.p.commtype,
                percabs=v.p.percabs,
                stocklike=v.p.stocklike,
                interest=v.p.interest,
                interest_long=v.p.interest_long,
                leverage=v.p.leverage,
                name=k
            ))

        return ret

    @classmethod
    def from_config(cls, **config):
        c = cls()

        c.set_cash(config.get('cash', 10000.0))

        if 'startingcash' in config:
            c.startingcash = config['startingcash']

        commission = config.get('commission', [])
        if commission:
            for comm in commission:
                c.setcommission(**comm)

        return c
