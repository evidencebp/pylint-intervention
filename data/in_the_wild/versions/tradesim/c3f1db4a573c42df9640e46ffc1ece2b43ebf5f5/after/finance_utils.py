"""Finance utilities library."""

# To make print working for Python2/3
from __future__ import print_function

# System
import re
import os
import glob
import csv
import sys
import math
# For socket timeout
import socket
# Use six to import urllib so it is working for Python2/3
from six.moves import urllib

# Custom
import pandas as pd

# User
import yqd


def calc_commission(nb_share):
    """Return the regular stock commission on Questrade: positive=Buy, negative=Sell."""
    # 0.01 $ per share (min 4.95, max 9.95)
    # 0.0035 $ per share ECN fees (sometimes waived, but simpler to always include them)
    nb_share = math.fabs(nb_share)
    return (nb_share > 0) * (nb_share * 0.0035 + min(9.95, max(0.01 * nb_share, 4.95)))


def calc_commission_etf(nb_share):
    """Return the ETF trade commission on Questrade: positive=Buy, negative=Sell."""
    # Sell only: 0.01 $ per share (min 4.95, max 9.95)
    # Buy or sell: 0.0035 $ per share ECN fees (sometimes waived, but simpler to always include them)
    return (nb_share < 0) * min(9.95, max(4.95, -nb_share * 0.01)) + math.fabs(nb_share) * 0.0035


def filename_to_symbol(filename):
    """Return the basename of the filename without the .csv at the end."""
    pat = re.compile(re.escape('.csv'), re.IGNORECASE)
    return pat.sub('', os.path.basename(filename))


def symbol_to_filename(symbol, basedir):
    """Return the complete filename path based on the symbol and basedir."""
    return os.path.join(basedir, symbol.upper()) + '.csv'


def get_all_symbols(basedir):
    return sorted(map(filename_to_symbol, glob.glob(os.path.join(basedir, '*.csv'))))


def get_symbols_from_file(ticker_file):
    """Return the list of ticker symbol listed in the provided text file.

    The parsing is done to ignore blank lines or lines starting with # (comment).
    On a non-comment row, only the first word is taken as a symbol.  This allow crafting the file with
    optional description following the symbol.
    """
    ticker_list = []

    with open(ticker_file, 'r') as f:
        for ticker_row in f.readlines():
            ticker_row = ticker_row.strip()  # remove leading and trailing whitespace
            if not ticker_row or ticker_row[0] == "#":  # skip comment line starting with #
                continue
            ticker = ticker_row.split()[0]  # split on whitespace
            ticker_list.append(ticker)

    return ticker_list


def download_url(url):
    """Download a URL and provide the result as a big string."""

    # Headers to fake a user agent
    headers = {
        'User-Agent':   'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 '
                        '(KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36'
    }

    s = ""
    try:
        req = urllib.request.Request(url, headers=headers)
        f = urllib.request.urlopen(req, timeout=5)
        if sys.version_info.major > 2:
            charset = f.info().get_content_charset()
        else:
            charset = f.headers.getparam('charset')

        if charset is None:  # Default according to HTTP
            charset = 'iso-8859-1'

        r = f.read()
        s = r.decode(charset)

    except (socket.timeout, urllib.error.HTTPError, urllib.error.URLError) as e:
        print("URLError: {}".format(e))
    return s


def download_data(symbol, basedir, start_date, end_date):
    """Wrapper function to yqd library."""
    print("Downloading:{} ...".format(symbol))
    symbol = symbol.upper()
    # Date 1
    d1 = "{0:0>4}".format(start_date.year) + \
         "{0:0>2}".format(start_date.month) + \
         "{0:0>2}".format(start_date.day)

    # Date 2
    d2 = "{0:0>4}".format(end_date.year) + \
         "{0:0>2}".format(end_date.month) + \
         "{0:0>2}".format(end_date.day)

    f = symbol_to_filename(symbol, basedir)

    data = yqd.load_yahoo_quote(symbol, d1, d2)
    # prevent writing invalid data
    if len(data) > 0:
        fh = open(f, 'w')
        fh.write(data)
        fh.close()


def update_all_symbols(basedir, start_date, end_date):
    """Re-download all symbols found in the basedir."""
    for s in get_all_symbols(basedir):
        download_data(s, basedir, start_date, end_date)


def normalize_data_frame(df):
    """Return a new dataframe normalized so that first row is all 1.0."""
    return df / df.iloc[0]


def fill_nan_data(df, inplace=False):
    """Fill the data in the given dataframe so no NaN gaps remain.
    This is done by:
    1. Fill forward nan with last known good value.
    2. Fill backward nan with first known good value.
    Returns: Dataframe with missing values filled or None if inplace=True.
    """

    # Data filling is done in 2 steps
    if inplace:
        # 1. Fill forward nan with last known good value.
        df.fillna(method='ffill', inplace=inplace)
        # 2. Fill backward nan with first known good value.
        df.fillna(method='backfill', inplace=inplace)
    else:
        # 1. Fill forward nan with last known good value.
        df2 = df.fillna(method='ffill', inplace=inplace)
        # 2. Fill backward nan with first known good value.
        df2 = df2.fillna(method='backfill', inplace=inplace)
        return df2


def load_data_frame(csv_file, start_date, end_date, adjust_price=True):
    """Load a CSV stock data file into a pandas dataframe.
    The dataframe is sorted chronologically by date.
    If requested, the prices (open, high, low, close) are adjusted according
    to the adjusted close price.
    """
    try:
        #print("Loading {} ...".format(filename_to_symbol(csv_file)))

        df = pd.read_csv(csv_file, index_col='Date', parse_dates=True)

        # Fix for yahoo bug during weekends.
        # Refer to https://github.com/mathieugouin/tradesim/issues/38
        # Conditions: Only last index is duplicated
        if df.index.duplicated()[-1] and not df.index.duplicated()[0:-1].any():
            df = df.iloc[0:-1] # Keep only 0 to second to last

        if len(df.index[df.index.duplicated()].unique()) > 0:
            raise Exception('Duplicated index in file {}'.format(csv_file))

        df.sort_index(inplace=True)

        # Re-index to only have the relevant date range
        date_range = pd.date_range(start=start_date, end=end_date, name='Date')
        df = df.reindex(date_range)

        # Discarding NaN values that are all NaN for a given row
        df.dropna(how='all', inplace=True)

        # Make sure none isolated remains:
        if df.isna().any().any():
            # To show the NaN
            print(df.loc[df.isna().all(axis=1)])
            raise Exception("ERROR {} contains isolated NaN".format(csv_file))

        if adjust_price:
            # Adjusting Columns based on Adjusted Close
            r = df['Adj Close'] / df['Close']  # ratio
            for col in ['Open', 'High', 'Low', 'Close']:  # n/a for 'Volume'
                df[col] *= r
            df.drop('Adj Close', axis=1, inplace=True)

        # Axis naming
        df.rename_axis('DATA', axis='columns', inplace=True)

        return df

    except Exception as e:
        print(type(e))  # the exception instance
        print(e.args)  # arguments stored in .args
        print(e)  # __str__ allows args to be printed directly
        print('Error parsing ' + csv_file)

        return None


# TBD does not work
def validate_symbol_data(csv_file):
    """Check for basic errors in historical market data."""
    valid = False  # Default
    try:
        with open(csv_file, 'r') as f:
            f.seek(0)
            valid = csv.Sniffer().has_header(f.read(1024))
    except Exception:
        valid = False

    return valid
