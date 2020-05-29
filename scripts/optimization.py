import os
import argparse
import numpy as np
from pydl.hyperopt import optimizer_from_config, hp_space_from_json
from pydl.models import load_json
from algotrade.session import Session


def loss_fn(session_config, *args):
    try:
        s = Session.from_config(**session_config)
        result = s.run()[0]
        res = result.analyzers.ret.get_analysis()['vwr']
        res = np.nan if res < 0 else 1. / res
    except:
        res = np.nan

    return res


def run_optimization(args):
    cfg = load_json(args.config)

    opt = optimizer_from_config(cfg.get('optimizer', dict()))
    search_space = hp_space_from_json(cfg.get('search_space', dict()))

    opt.fmin(
        search_space=search_space,
        obj_func=loss_fn,
        max_threads=args.max_threads
    )


def parse_args():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description='Optimization script'
    )

    parser.add_argument('--config',
                        required=True,
                        type=str,
                        default=os.environ.get('CONFIG', None),
                        help='Optimization session config')

    parser.add_argument('--max_threads',
                        required=False,
                        type=int,
                        default=1)

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    run_optimization(args)
