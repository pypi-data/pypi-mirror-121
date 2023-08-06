# coding: utf-8

import traceback
from collections.abc import Callable
import pandas as pd

from ....delivery.stream import StateEvent
from ....core.session import get_valid_session
from ....core.log_reporter import _LogReporter
from ....delivery.stream import RDPStream
from ....delivery.stream import StateManager


class QuantitativeDataStream(StateManager, _LogReporter):
    """
        Open a streaming quantitative analytic service subscription.

    Parameters
    ----------
    universe: dict

    fields: list

    api: str, optional
         Means the default streaming API can be changed

    extended_params: dict
        Default: None

    on_response: callable object (stream, response_message)
        Default: None

    on_update: callable object (stream, update_message)
        Default: None

    on_state: callable object (stream, state_message):
        Called when the stream has new state.
        Default: None

    Methods
    -------
    open()
        Open the QuantitativeDataStream connection
    close()
        Close the QuantitativeDataStream connection, releases resources
    get_snapshot()
        Get DataFrame with stream
    """

    def __init__(
        self,
        universe: dict,
        fields: list = None,
        extended_params: dict = None,
        session: object = None,
        api: str = None,
        on_response: Callable = None,
        on_update: Callable = None,
        on_state: Callable = None,
    ):
        session = get_valid_session(session)

        StateManager.__init__(self, loop=session._loop)
        _LogReporter.__init__(self, logger=session)

        self._session = session
        self._universe = universe
        self._fields = fields
        self._extended_params = extended_params

        self._api = api or "streaming/quantitative-analytics/financial-contracts"

        self._on_response_cb = on_response
        self._on_update_cb = on_update
        self._on_state_cb = on_state

        self._data = None
        self._headers = None

        if extended_params and "view" in extended_params:
            self._column_names = extended_params["view"]
        else:
            self._column_names = fields or None

        self._stream = RDPStream(
            session=self._session,
            service=None,
            view=self._fields,
            parameters=None,
            universe=self._universe,
            extended_params=self.extended_params,
            api=self._api,
            on_ack=self.__on_ack,
            on_response=self.__on_response,
            on_update=self.__on_update,
            on_alarm=self.__on_alarm,
        )
        self._stream.on(StateEvent.CLOSE, lambda *_: self.close())

    def __repr__(self):
        s = super().__repr__()
        s = s.replace(">", f" {{name='{self._universe}', state={self.state}}}>")
        return s

    @property
    def extended_params(self):
        extended_params = (
            dict(self._extended_params) if self._extended_params is not None else {}
        )
        return extended_params

    @property
    def df(self):
        if self._data is None or self._column_names is None:
            return
        return pd.DataFrame.from_records(self._data, columns=self._column_names)

    def get_snapshot(self):
        """
        Returns DataFrame snapshot a streaming quantitative analytic service

        Returns
        -------
        pd.DataFrame

        """
        return self.df

    #   callbacks
    def on_response(self, on_response_cb: Callable):
        """
        This callback is called with the reference to the stream object,
        the instrument name and the instrument response

        Parameters
        ----------
        on_response_cb : Callable
            Called when the stream has response

        Returns
        -------
        current instance

        """
        self._on_response_cb = on_response_cb
        return self

    def on_update(self, on_update_cb: Callable):
        """
        This callback is called with the reference to the stream object,
        the instrument name and the instrument update

        Parameters
        ----------
        on_update_cb : Callable
            Called when the stream has a new update

        Returns
        -------
        current instance

        """
        self._on_update_cb = on_update_cb
        return self

    def on_state(self, on_state_cb: Callable):
        """
        This callback is called with the reference to the stream object,
        when the stream has new state

        Parameters
        ----------
        on_state_cb : Callable
            Called when the stream has a new state

        Returns
        -------
        current instance

        """
        self._on_state_cb = on_state_cb
        return self

    async def _do_open_async(self):
        await self._stream.open_async()

    async def _do_close_async(self):
        await self._stream.close_async()

    def _do_pause(self):
        """
        Currently, stream does not support pause.
        """
        pass

    def _do_resume(self):
        """
        Currently, stream does not support resume.
        """
        pass

    def __on_ack(self, stream: object, ack: dict):
        if "state" in ack:
            self._on_state(stream, ack["state"])

    def __on_response(self, stream: object, response: dict):
        if "data" in response:
            self._data = response["data"]
            self._debug(f"Received on_response - data={self._data}")

        if "headers" in response:
            self._headers = response["headers"]
            self._debug(f"Received on_response - headers={self._headers}")

            self._column_names = [col["name"] for col in self._headers]

        self._on_response(stream, response)

    def __on_update(self, stream, update):
        if "data" in update:
            self._data = update["data"]
            self._debug(f"Received on_update - data={self._data}")

        self._on_update(stream, update)

    def __on_alarm(self, stream, alarm):
        if "state" in alarm:
            self._on_state(stream, alarm["state"])

    def _on_response(self, stream, response_message: dict):
        self.state = stream.state
        self._debug(
            f"QuantitativeDataStream._on_response(response_message={response_message})"
        )
        if self._on_response_cb:
            try:
                self._on_response_cb(self, self._data, self._column_names)
            except Exception as e:
                self._error(
                    f"QuantitativeDataStream on_response callback raised exception: {e!r}"
                )
                self._debug(f"{traceback.format_exc()}")

    def _on_update(self, stream, update_message: dict):
        self.state = stream.state
        self._debug(
            f"QuantitativeDataStream._on_update(update_message={update_message})"
        )
        #   call the on_update callback function
        if self._on_update_cb:
            #   valid on_update callback
            try:
                self._on_update_cb(self, self._data, self._column_names)
            except Exception as e:
                #   on_add callback has an exception
                self._error(
                    f"QuantitativeDataStream on_update callback raised exception: {e!r}"
                )
                self._debug(f"{traceback.format_exc()}")

    def _on_state(self, stream, state_message: dict):
        self.state = stream.state
        self._debug(f"QuantitativeDataStream._on_state(state_message={state_message})")
        if self._on_state_cb:
            try:
                self._on_state_cb(self, state_message)
            except Exception as e:
                self._error(
                    f"QuantitativeDataStream on_state callback raised exception: {e!r}"
                )
                self._debug(f"{traceback.format_exc()}")
