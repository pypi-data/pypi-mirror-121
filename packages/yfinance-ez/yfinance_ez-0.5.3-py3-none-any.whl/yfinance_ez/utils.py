import requests as requests
import pandas as pd
import re

from yfinance_ez.constants import USER_AGENT_HEADERS

try:
    import ujson as _json
except ImportError:
    import json as _json


def get_json(url, proxy=None):
    html = requests.get(url=url, proxies=proxy, headers=USER_AGENT_HEADERS).text

    if "QuoteSummaryStore" not in html:
        html = requests.get(url=url, proxies=proxy, headers=USER_AGENT_HEADERS).text
        if "QuoteSummaryStore" not in html:
            return {}

    json_str = html.split('root.App.main =')[1].split(
        '(this)')[0].split(';\n}')[0].strip()
    data = _json.loads(json_str)[
        'context']['dispatcher']['stores']['QuoteSummaryStore']

    # return data
    new_data = _json.dumps(data).replace('{}', 'null')
    new_data = re.sub(
        r'\{[\'|\"]raw[\'|\"]:(.*?),(.*?)\}', r'\1', new_data)

    return _json.loads(new_data)


def camel2title(o):
    return [re.sub("([a-z])([A-Z])", "\g<1> \g<2>", i).title() for i in o]


def auto_adjust(data):
    df = data.copy()
    ratio = df["Close"] / df["Adj Close"]
    df["Adj Open"] = df["Open"] / ratio
    df["Adj High"] = df["High"] / ratio
    df["Adj Low"] = df["Low"] / ratio

    df.drop(
        ["Open", "High", "Low", "Close"],
        axis=1, inplace=True)

    df.rename(columns={
        "Adj Open": "Open", "Adj High": "High",
        "Adj Low": "Low", "Adj Close": "Close"
    }, inplace=True)

    df = df[["Open", "High", "Low", "Close", "Volume"]]
    return df[["Open", "High", "Low", "Close", "Volume"]]


def back_adjust(data):
    """ back-adjusted data to mimic true historical prices """

    df = data.copy()
    ratio = df["Adj Close"] / df["Close"]
    df["Adj Open"] = df["Open"] * ratio
    df["Adj High"] = df["High"] * ratio
    df["Adj Low"] = df["Low"] * ratio

    df.drop(
        ["Open", "High", "Low", "Adj Close"],
        axis=1, inplace=True)

    df.rename(columns={
        "Adj Open": "Open", "Adj High": "High",
        "Adj Low": "Low"
    }, inplace=True)

    return df[["Open", "High", "Low", "Close", "Volume"]]


def parse_quotes(data, tz=None):
    timestamps = data["timestamp"]
    ohlc = data["indicators"]["quote"][0]
    volumes = ohlc["volume"]
    opens = ohlc["open"]
    closes = ohlc["close"]
    lows = ohlc["low"]
    highs = ohlc["high"]

    adjclose = closes
    if "adjclose" in data["indicators"]:
        adjclose = data["indicators"]["adjclose"][0]["adjclose"]

    quotes = pd.DataFrame({"Open": opens,
                           "High": highs,
                           "Low": lows,
                           "Close": closes,
                           "Adj Close": adjclose,
                           "Volume": volumes})

    quotes.index = pd.to_datetime(timestamps, unit="s")
    quotes.sort_index(inplace=True)

    if tz is not None:
        quotes.index = quotes.index.tz_localize(tz)

    return quotes


def parse_actions(data, tz=None):
    dividends = pd.DataFrame(columns=["Dividends"])
    splits = pd.DataFrame(columns=["Stock Splits"])

    if "events" in data:
        if "dividends" in data["events"]:
            dividends = pd.DataFrame(
                data=list(data["events"]["dividends"].values()))
            dividends.set_index("date", inplace=True)
            dividends.index = pd.to_datetime(dividends.index, unit="s")
            dividends.sort_index(inplace=True)
            if tz is not None:
                dividends.index = dividends.index.tz_localize(tz)

            dividends.columns = ["Dividends"]

        if "splits" in data["events"]:
            splits = pd.DataFrame(
                data=list(data["events"]["splits"].values()))
            splits.set_index("date", inplace=True)
            splits.index = pd.to_datetime(splits.index, unit="s")
            splits.sort_index(inplace=True)
            if tz is not None:
                splits.index = splits.index.tz_localize(tz)
            splits["Stock Splits"] = splits["numerator"] / \
                                     splits["denominator"]
            splits = splits["Stock Splits"]

    return dividends, splits


def shift_quarter_date(dt: str, shift_forward=True):
    """
    Return next (or prev) quarter date str (eg: <Quarter>Q<YYYY>.
    Args:
        shift_forward: (bool) return next quarter date str if True. Return prev if false.
    """
    quarter = int(dt[0])
    year = int(dt[-4:])

    new_quarter = quarter + 1 if shift_forward else quarter - 1
    if new_quarter == 5:
        new_quarter = 1
        new_year = year + 1
    elif new_quarter == 0:
        new_quarter = 4
        new_year = year - 1
    else:
        new_year = year

    return f"{new_quarter}Q{new_year}"


def correct_quarter_date_column(df: pd.DataFrame, date_col_name: str = 'date') -> pd.DataFrame:
    """
    Found some instances of quarter dates showing up twice. This will autocorrect sequences
    of quarter date strings.
    EG:  (3Q2020, 3Q2020, 1Q2021, 2Q2021) -> (3Q2020, 4Q2020, 1Q2021, 2Q2021)
    Assumes there is only one date that is out of place.
    Args:
        df:
        date_col_name:

    Returns:
        corrected dataframe
    """
    dates = list(df[date_col_name])

    for i in range(len(dates)):
        left_idx = i - 1 if i > 0 else len(dates) - 1
        right_idx = 0 if i == len(dates) - 1 else i + 1

        if dates[i] == dates[left_idx]:
            if shift_quarter_date(dates[i], True) == dates[right_idx]:
                dates[left_idx] = shift_quarter_date(dates[left_idx], False)
            else:
                dates[i] = shift_quarter_date(dates[i], True)
            break

    df[date_col_name] = dates
    return df
