import backtrader.analyzers as bta

ANALYZERS = {
    bta.SharpeRatio.__name__: bta.SharpeRatio,
    bta.DrawDown.__name__: bta.DrawDown
}
