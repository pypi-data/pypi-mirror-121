from dateutil.parser import ParserError

from ._enums import StatTypes, Frequency
from .._content_provider import (
    DataProvider,
    RequestFactory,
    ResponseFactory,
)
from ...tools import convert_content_data_to_df
from ...tools import universe_arg_parser
from ...tools._datetime import ownership_datetime_adapter


class OwnershipResponseFactory(ResponseFactory):
    def create_success(self, *args, **kwargs):
        data = args[0]
        content_data = data.get("content_data")
        inst = self.response_class(is_success=True, **data)
        dataframe = (
            convert_content_data_to_df(content_data)
            if "headers" in content_data
            else None
        )
        inst.data = self.data_class(content_data, dataframe)
        return inst


class OwnershipRequestFactory(RequestFactory):
    def get_query_parameters(self, *_, **kwargs) -> list:
        query_parameters = []
        universe = kwargs.get("universe")
        if universe is not None:
            universe = universe_arg_parser.get_str(universe, delim=",")
            query_parameters.append(("universe", universe))

        stat_type = kwargs.get("stat_type")
        if stat_type is not None:
            if isinstance(stat_type, StatTypes):
                stat_type = stat_type.value
            query_parameters.append(("statType", stat_type))

        offset = kwargs.get("offset")
        if offset is not None:
            query_parameters.append(("offset", offset))

        limit = kwargs.get("limit")
        if limit is not None:
            query_parameters.append(("limit", limit))

        sort_order = kwargs.get("sort_order")
        if sort_order is not None:
            query_parameters.append(("sortOrder", sort_order))

        frequency = kwargs.get("frequency")
        if frequency is not None:
            if isinstance(frequency, Frequency):
                frequency = frequency.value
            query_parameters.append(("frequency", frequency))

        start = kwargs.get("start")
        if start is not None:
            try:
                start = ownership_datetime_adapter.get_str(start)
            except ParserError as e:
                pass
            query_parameters.append(("start", start))

        end = kwargs.get("end")
        if end is not None:
            try:
                end = ownership_datetime_adapter.get_str(end)
            except ParserError as e:
                pass
            query_parameters.append(("end", end))

        count = kwargs.get("count")
        if count is not None:
            query_parameters.append(("count", count))

        return query_parameters

    def extend_query_parameters(self, query_parameters, extended_params):
        # query_parameters -> [("param1", "val1"), ]
        result = dict(query_parameters)
        # result -> {"param1": "val1"}
        result.update(extended_params)
        # result -> {"param1": "val1", "extended_param": "value"}
        # return [("param1", "val1"), ("extended_param", "value")]
        return list(result.items())


ownership_data_provider = DataProvider(
    request=OwnershipRequestFactory(), response=OwnershipResponseFactory()
)
