import re
from typing import Union, Optional, Callable

from pandas import DataFrame

from .. import Fundamental, get_default
from .. import historical_pricing
from ..tools._common import fields_arg_parser, universe_arg_parser
from ..content.historical_pricing._hp_data_provider import EventTypes

from .get_data import ADC_PATTERN
from .get_data import _find_and_rename_duplicated_columns
from .get_data import _send_request
from .get_data import _convert_date_columns_to_datetime
from .get_data import _rename_column_n_to_column


EVENTS_INTERVALS = ["tick", "tas", "taq"]

INTERVALS = {
    "tick": {"event_types": None, "adc": "D"},
    "tas": {"event_types": EventTypes.TRADE, "adc": "D"},
    "taq": {"event_types": EventTypes.QUOTE, "adc": "D"},
    "minute": {"pricing": "PT1M", "adc": "D"},
    "1min": {"pricing": "PT1M", "adc": "D"},
    "5min": {"pricing": "PT5M", "adc": "D"},
    "10min": {"pricing": "PT10M", "adc": "D"},
    "30min": {"pricing": "PT30M", "adc": "D"},
    "60min": {"pricing": "PT60M", "adc": "D"},
    "hourly": {"pricing": "PT1H", "adc": "D"},
    "1h": {"pricing": "PT1H", "adc": "D"},
    "daily": {"pricing": "P1D", "adc": "D"},
    "1d": {"pricing": "P1D", "adc": "D"},
    "1D": {"pricing": "P1D", "adc": "D"},
    "7D": {"pricing": "P7D", "adc": "W"},
    "7d": {"pricing": "P7D", "adc": "W"},
    "weekly": {"pricing": "P1W", "adc": "W"},
    "1W": {"pricing": "P1W", "adc": "W"},
    "monthly": {"pricing": "P1M", "adc": "M"},
    "1M": {"pricing": "P1M", "adc": "M"},
    "quarterly": {"pricing": "P3M", "adc": "CQ"},
    "3M": {"pricing": "P3M", "adc": "CQ"},
    "6M": {"pricing": "P6M", "adc": "CS"},
    "yearly": {"pricing": "P1Y", "adc": "CY"},
    "1Y": {"pricing": "P1Y", "adc": "CY"},
}


def get_history(
    universe: Union[str, list],
    fields: Union[str, list, None] = None,
    interval: Optional[str] = None,
    start: Optional[str] = None,
    end: Optional[str] = None,
    adjustments: Optional[str] = None,
    count: Optional[int] = None,
) -> DataFrame:
    """
    With this tool you can request historical data from Pricing and ADC

    Parameters
    ----------
        universe: str | list
            instruments to request.
        fields: str | list, optional
            fields to request.
        interval: str, optional
            The consolidation interval. Supported intervals are:
            tick, tas, taq, minute, 1min, 5min, 10min, 30min, 60min, hourly, 1h, daily,
            1d, 1D, 7D, 7d, weekly, 1W, monthly, 1M, quarterly, 3M, 6M, yearly, 1Y
        start: str, optional
            The start date and timestamp of the query in ISO8601 with UTC only
        end: str,
            The end date and timestamp of the query in ISO8601 with UTC only
        adjustments : str, optional
            The adjustment
        count : int, optional
            The maximum number of data returned. Values range: 1 - 10000

    Returns
    -------
    pandas.DataFrame

     Examples
    --------
    >>> get_history(universe="GOOG.O")
    >>> get_history(universe="GOOG.O", fields="tr.Revenue", interval="1Y")
    >>> get_history(
    ...     universe="GOOG.O",
    ...     fields=["BID", "ASK", "tr.Revenue"],
    ...     interval="1Y",
    ...     start="2015-01-01",
    ...     end="2020-10-01",
    ... )
    """

    if interval not in INTERVALS and interval is not None:
        raise ValueError(
            f"Not supported interval value.\nSupported intervals are:"
            f"{list(INTERVALS.keys())}"
        )

    _pricing_events = historical_pricing.events.Definition
    _pricing_summaries = historical_pricing.summaries.Definition

    _fundamental_data = Fundamental.get_data
    params = {
        "universe": universe,
        "fields": fields,
        "interval": interval,
        "start": start,
        "end": end,
        "adjustments": adjustments,
        "count": count,
    }

    return _get_history(
        p_events=_pricing_events,
        p_summaries=_pricing_summaries,
        adc=_fundamental_data,
        params=params,
    )


def _get_history(
    p_events: Callable,
    p_summaries: Callable,
    adc: Callable,
    params: dict,
) -> DataFrame:
    logger = get_default().logger()
    adc_df, pricing_df = DataFrame(), DataFrame()
    adc_params = _translate_pricing_params_to_adc(params)

    if params["interval"] in EVENTS_INTERVALS:
        p_provider = p_events
        interval = params.pop("interval")
        params["eventTypes"] = INTERVALS[interval]["event_types"]

    else:
        p_provider = p_summaries

        if params["interval"] is not None:
            params["interval"] = INTERVALS[params["interval"]]["pricing"]

    if params["fields"] is not None:
        fields = fields_arg_parser.get_list(params["fields"])

        adc_fields = [i for i in fields if re.match(ADC_PATTERN, i)]
        pricing_fields = [i for i in fields if i not in adc_fields]

        if adc_fields:
            adc_df = _send_request(
                data_provider=adc,
                params={
                    "universe": params["universe"],
                    "fields": adc_fields,
                    "parameters": adc_params,
                    "use_field_names_in_headers": True,
                },
                logger=logger,
            )

        if pricing_fields:
            params["fields"] = pricing_fields
            pricing_df = _send_request(
                data_provider=p_provider,
                params=params,
                logger=logger,
                is_definition=True,
            )

    else:
        pricing_df = _send_request(
            data_provider=p_provider,
            params=params,
            logger=logger,
            is_definition=True,
        )

    if pricing_df.empty:
        result = adc_df
    elif adc_df.empty:
        result = pricing_df
    else:
        universe = universe_arg_parser.get_list(params["universe"])
        is_multiuniverse = True if len(universe) > 1 else False
        result = _merge(pricing_df, adc_df, multiindex=is_multiuniverse)

    return result


def _translate_pricing_params_to_adc(p_params: dict) -> dict:
    adc_params = {}

    if p_params["start"]:
        adc_params["SDate"] = p_params["start"]

    if p_params["end"]:
        adc_params["EDate"] = p_params["end"]

    if p_params["interval"]:
        adc_params["FRQ"] = INTERVALS[p_params["interval"]]["adc"]

    return adc_params


def _merge(
    pricing_df: DataFrame, adc_df: DataFrame, multiindex: bool = False
) -> DataFrame:
    date_column = "Date"

    duplicated_columns = _find_and_rename_duplicated_columns(adc_df)

    if date_column in duplicated_columns:
        date_column = f"{date_column}_0"

    _convert_date_columns_to_datetime(adc_df, pattern="Date")

    if multiindex:
        adc_df = adc_df.pivot(index=date_column, columns="Instrument")
        adc_df = adc_df.swaplevel(axis=1)

        result = pricing_df.join(adc_df, how="outer")
        result.sort_index(axis=1, inplace=True)
    else:
        adc_df.pop("Instrument")
        adc_df.set_index(date_column, inplace=True)

        universe = pricing_df.columns.name

        result = pricing_df.merge(
            adc_df, left_index=True, right_index=True, how="outer"
        )

        result.columns.name = universe

    for i in duplicated_columns:
        _rename_column_n_to_column(i, result, multiindex=multiindex)

    return result
