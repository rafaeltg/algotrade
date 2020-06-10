import sys
import logging
import pandas as pd
import datetime as dt
import argparse
from influxdb import DataFrameClient as dfclient
import yfinance as yf


def format_data(df: pd.DataFrame):
    col_renames = {
        'High': 'high_p',
        'Low': 'low_p',
        'Open': 'open_p',
        'Close': 'close_p',
        'Adj Close': 'adjclose_p',
        'Volume': 'volume'
    }

    df = df.rename(col_renames, axis=1)

    # Sort the dataframe based on ascending dates.
    df.sort_index(ascending=True, inplace=True)

    # Convert dataframe columns to float and ints.
    df[['high_p', 'low_p', 'open_p', 'close_p', 'adjclose_p']] = df[
        ['high_p', 'low_p', 'open_p', 'close_p', 'adjclose_p']].astype(float)
    df[['volume']] = df[['volume']].astype(int)

    return df


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description="Import Yahoo Historical Data to InfluxDB"
    )

    parser.add_argument('--tickers',
                        required=True,
                        action='store',
                        default=None,
                        help='Ticker(s) to request data for.')

    parser.add_argument('--dbhost',
                        required=False,
                        action='store',
                        default='localhost',
                        type=str,
                        help='InfluxDB hostname.')
    parser.add_argument('--dbport',
                        required=False,
                        action='store',
                        default=8086,
                        type=int,
                        help='InfluxDB port number.')
    parser.add_argument('--username',
                        required=False,
                        action='store',
                        default='user',
                        type=str,
                        help='InfluxDB username.')
    parser.add_argument('--password',
                        required=False,
                        action='store',
                        default=None,
                        help='InfluxDB password.')
    parser.add_argument('--database',
                        required=False,
                        action='store',
                        default='instruments',
                        type=str,
                        help='InfluxDB database to use.')

    parser.add_argument('--fromdate',
                        required=True,
                        action='store',
                        default=None,
                        type=str,
                        help='Starting date for historical download with format: YYYY[-MM-DDTHH:MM:SS].')
    parser.add_argument('--todate',
                        required=False,
                        action='store',
                        default=dt.datetime.today().strftime("%Y-%m-%d"),
                        type=str,
                        help='Ending date for historical download with format: YYYY[-MM-DDTHH:MM:SS].')

    parser.add_argument('--debug',
                        required=False,
                        action='store_true',
                        help='Turn on debug logging level.')
    parser.add_argument('--info',
                        required=False,
                        action='store_true',
                        help='Turn on info logging level.')

    args = parser.parse_args()

    log = logging.getLogger()
    log_console = logging.StreamHandler(sys.stdout)
    log.addHandler(log_console)

    if args.debug:
        log.setLevel(logging.DEBUG)

    if args.info:
        log.setLevel(logging.INFO)

    tickers = args.tickers.replace(" ", "").split(',')

    db = dfclient(
        host=args.dbhost,
        port=args.dbport,
        username=args.username,
        password=args.password,
        database=args.database
    )

    for (i, ticker) in enumerate(tickers):
        try:
            log.info("Processing %s (%d out of %d)", ticker, i + 1, len(tickers))

            df = yf.download(ticker,
                             start=args.fromdate,
                             end=args.todate,
                             progress=False)

            df = format_data(df)

            db.write_points(dataframe=df, measurement=ticker)
        except Exception as err:
            log.error('Error returned: %s', err)
