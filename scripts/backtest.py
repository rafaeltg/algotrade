import argparse
import os
import backtrader as bt
from pydl.models import load_json
from algotrade.session import Session


def run_backtest():
    args = parse_args()

    if args is None:
        return

    cfg = load_json(args.config)

    s = Session.from_config(**cfg)

    s.addwriter(bt.WriterFile, csv=True, rounding=3)
    s.run()


def parse_args():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description='Sample for strategy selection'
    )

    parser.add_argument('--config',
                        required=False,
                        default=os.environ.get('CONFIG', None),
                        help='session config')

    return parser.parse_args()


if __name__ == "__main__":
    run_backtest()
