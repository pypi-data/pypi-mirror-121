import threading
from typing import TYPE_CHECKING

from ...errors import StreamConnectionError

if TYPE_CHECKING:
    from ... import StreamConnection


class StreamCxnManager(object):
    def __init__(self) -> None:
        self._stream_cxn_by_id: dict = {}
        self._register_lock: threading.Lock = threading.Lock()
        self._id_counter: int = 0

    def get_new_id(self) -> int:
        self._id_counter += 1
        return self._id_counter

    def register(self, stream_cxn: "StreamConnection") -> None:

        with self._register_lock:
            if not stream_cxn:
                raise StreamConnectionError(
                    1, "Try to register unavailable streaming session"
                )

            id_ = stream_cxn.streaming_session_id

            if id_ in self._stream_cxn_by_id:
                raise StreamConnectionError(
                    1,
                    f"Try to register again existing streaming session id {id_}",
                )

            id_ = self.get_new_id()
            stream_cxn.debug(f"Register streaming session {id_}")
            self._stream_cxn_by_id[id_] = stream_cxn
            stream_cxn._streaming_session_id = id_

    def unregister(self, stream_cxn: "StreamConnection") -> None:

        with self._register_lock:
            if not stream_cxn:
                raise StreamConnectionError(
                    1, "Try to unregister unavailable streaming session"
                )

            id_ = stream_cxn.streaming_session_id

            if id_ is None:
                raise StreamConnectionError(
                    1, "Try to unregister unavailable streaming session"
                )

            if id_ not in self._stream_cxn_by_id:
                raise StreamConnectionError(
                    1,
                    f"Try to unregister unknown streaming session id {id_}",
                )

            stream_cxn.debug(f"Unregister streaming session {id_}")
            self._stream_cxn_by_id.pop(id_)


stream_cxn_manager = StreamCxnManager()
