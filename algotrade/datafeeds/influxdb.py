import backtrader as bt


class InfluxDB(bt.feeds.InfluxDB):

    def to_config(self) -> dict:
        return self.params.__dict__

    @classmethod
    def from_config(cls, **config):
        return cls(**config)
