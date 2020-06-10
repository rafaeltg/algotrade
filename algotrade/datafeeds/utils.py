import datetime as dt
from dateutil.parser import parse


def _parse_dates(config: dict):
    cfg = config.copy()

    sessionstart = config.pop('sessionstart', None)
    if sessionstart is not None:
        cfg['sessionstart'] = dt.datetime.strptime(sessionstart, '%H:%M').time()

    sessionend = config.pop('sessionend', None)
    if sessionend is not None:
        cfg['sessionend'] = dt.datetime.strptime(sessionend, '%H:%M').time()

    fromdate = config.pop('fromdate', None)
    if fromdate is not None:
        cfg['fromdate'] = parse(fromdate)

    todate = config.pop('todate', None)
    if todate is not None:
        cfg['todate'] = parse(todate)

    return cfg
