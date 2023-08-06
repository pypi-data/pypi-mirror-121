from types import SimpleNamespace
from typing import List, Optional, Tuple, TYPE_CHECKING, Callable

import pandas as pd
from pandas import DataFrame

from .._content_provider import Response, Data

if TYPE_CHECKING:
    from ._hp_data_provider import DayIntervalType


def get_response(responses: List[Tuple[str, Response]]) -> Response:
    inst_name, response = responses[0]
    df = response.data.df
    if df is not None:
        df.axes[1].name = inst_name
    return response


def join_responses_hp_summaries(get_data_async: Callable) -> Callable:
    async def wrapper(*args, **kwargs) -> Response:
        from ._hp_data_provider import axis_by_day_interval_type

        responses: List[Tuple[str, Response]] = await get_data_async(*args, **kwargs)

        if len(responses) == 1:
            return get_response(responses)

        day_interval_type: "DayIntervalType" = kwargs.get("day_interval_type")
        axis_name = axis_by_day_interval_type.get(day_interval_type)
        return join_responses(responses, new_axis_name=axis_name)

    return wrapper


def join_responses_hp_events(get_data_async: Callable) -> Callable:
    async def wrapper(*args, **kwargs) -> Response:
        responses: List[Tuple[str, Response]] = await get_data_async(*args, **kwargs)

        if len(responses) == 1:
            return get_response(responses)

        return join_responses(responses, new_axis_name="Timestamp")

    return wrapper


def join_responses(
    responses: List[Tuple[str, Response]], new_axis_name: str
) -> Response:
    successful = (response.data.df for _, response in responses if response.is_success)
    first_successful_df = next(successful, None)

    raws = []

    # this is ad-hoc solution which makes response object
    # backward compatible with existing logging logic in
    # rd.get_history
    #
    # you can remove SimpleNamespace() from code
    # after clarifying all requirements for response object with multiple RICs
    raw_response = SimpleNamespace()
    raw_response.request = SimpleNamespace()
    raw_response.request.url = SimpleNamespace()
    raw_response.request.url.path = SimpleNamespace()

    if first_successful_df is None:
        error_message = "ERROR: No successful response.\n"
        for inst_name, response in responses:
            error_message += f"\tERROR: {response.error_message} - {inst_name}\n"
            raws.append(response.data.raw)
        response = Response(raw_response=raw_response)
        response.is_success = False
        response.error_message = error_message
        response.data = Data(raws)
        return response

    universe = []
    columns = (None,)
    dfs = []
    for inst_name, response in responses:
        universe.append(inst_name)

        df = response.data.df
        if response.is_success:
            raws.append(response.data.raw)
        else:
            raws.append(response.data.raw)
            df = DataFrame(columns=columns, index=first_successful_df.index.to_numpy())

        dfs.append(df)

    df = join_dfs(dfs, universe)

    if not df.empty:
        df = df.rename_axis(new_axis_name)

    response = Response(raw_response=raw_response)
    response.is_success = True
    response.data = Data(raws, dataframe=df)

    return response


def join_dfs(dfs: List[DataFrame], universe: List[str]) -> Optional[DataFrame]:
    if len(dfs) != len(universe):
        raise ValueError(
            f"Cannot join dfs, "
            f"because length of dfs list is not equal to length of universe, "
            f"dfs={dfs}, universe={universe}"
        )

    if len(dfs) == 0:
        raise ValueError(f"Cannot join dfs, because dfs list is empty, dfs={dfs}")

    for inst_name, df in zip(universe, dfs):
        df.columns = pd.MultiIndex.from_product([[inst_name], df.columns])

    df = dfs.pop()
    df = df.join(dfs, how="outer")  # noqa
    df = df.convert_dtypes()

    return df
