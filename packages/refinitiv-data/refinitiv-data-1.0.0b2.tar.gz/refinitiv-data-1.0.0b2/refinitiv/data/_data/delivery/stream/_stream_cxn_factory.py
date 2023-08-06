from typing import TYPE_CHECKING

from . import OMMStreamConnection, RDPStreamConnection
from ._protocol_type import ProtocolType
from ._stream_cxn_type import StreamCxnType
from ...core.session._session_type import SessionType

if TYPE_CHECKING:
    from . import StreamConnection
    from ... import Session
    from ...core.session.stream_service_discovery.stream_connection_configuration import (
        StreamConnectionConfiguration,
    )
    from ...core import Session

protocol_type_by_name = {
    "OMM": ProtocolType.OMM,
    "RDP": ProtocolType.RDP,
}

stream_cxn_type_by_api_name = {
    "streaming/pricing/main": StreamCxnType.PRICING,
    "streaming/trading-analytics/redi": StreamCxnType.TRADING,
    "streaming/quantitative-analytics/financial-contracts": StreamCxnType.QUANTITATIVE,
}


def get_protocol_type_by_name(protocol_name: str) -> ProtocolType:
    protocol_type = protocol_type_by_name.get(protocol_name)

    if not protocol_type:
        raise ValueError(f"Can't find protocol type by name: {protocol_name}")

    return protocol_type


def convert_api_to_stream_cxn_type(api: str) -> StreamCxnType:
    stream_cxn_type = stream_cxn_type_by_api_name.get(api)

    if not stream_cxn_type:
        raise ValueError(f"Can't find stream connection type by api: {api}")

    return stream_cxn_type


cnx_class_by_protocol_type = {
    ProtocolType.OMM: OMMStreamConnection,
    ProtocolType.RDP: RDPStreamConnection,
}


def get_stream_cxn(
    stream_cxn_type: StreamCxnType,
    protocol_type: ProtocolType,
    session: "Session",
    session_type: SessionType,
    api: str,
) -> "StreamConnection":
    config: "StreamConnectionConfiguration" = session.run_until_complete(
        session._connection.get_stream_connection_configuration(api)
    )
    session_id = session.session_id
    protocol_name = protocol_type.name
    cxn_name = stream_cxn_type.name
    name = f"WebSocket {session_id} - {protocol_name} Protocol - {cxn_name}"
    cnx_class = cnx_class_by_protocol_type.get(protocol_type)
    stream_cxn = cnx_class(
        name,
        session,
        api,
        config,
        protocol_name,
    )
    stream_cxn.daemon = True
    stream_cxn.start()
    return stream_cxn
