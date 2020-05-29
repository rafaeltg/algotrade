import argparse
import os
import backtrader as bt
from pydl.models import load_json
from algotrade.session import Session


def run_backtest(args):
    cfg = load_json(args.config)

    s = Session.from_config(**cfg)

    s.addwriter(bt.WriterFile, csv=True, rounding=2)

    s.run()


def parse_args():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description='Backtest script'
    )

    parser.add_argument('--config',
                        required=True,
                        default=os.environ.get('CONFIG', None),
                        help='Backtest session config')

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    run_backtest(args)
