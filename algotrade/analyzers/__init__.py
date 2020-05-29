import backtrader.analyzers as bta

ANALYZERS = {
    bta.SharpeRatio.__name__: bta.SharpeRatio,
    bta.DrawDown.__name__: bta.DrawDown,
    bta.SQN.__name__: bta.SQN,
    bta.TradeAnalyzer.__name__: bta.TradeAnalyzer,
    bta.VWR.__name__: bta.VWR
}
