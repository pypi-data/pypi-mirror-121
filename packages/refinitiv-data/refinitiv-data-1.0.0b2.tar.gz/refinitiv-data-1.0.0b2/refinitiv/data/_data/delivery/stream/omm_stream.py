# coding: utf8


import logging
import traceback
from threading import Lock
from typing import Callable

from ._omm_stream import _OMMStream
from .state import StreamState


class OMMStream(_OMMStream):
    """
    Open an OMM stream.

    Parameters
    ----------
    name: string
        RIC to retrieve item stream.

    domain: string
        Specify item stream domain (MarketPrice, MarketByPrice, ...)
        Default : "MarketPrice"

    api: string, optional
        specific name of RDP streaming defined in config file. i.e. 'streaming/trading-analytics/redi'
        Default: 'streaming/pricing/main'

    service: string, optional
        Specify the service to subscribe on.
        Default: None

    fields: string or list, optional
        Specify the fields to retrieve.
        Default: None

    extended_params: dict, optional
        Specify optional params
        Default: None

    on_refresh: callable object, optional
        Called when the stream is opened or when the record is refreshed with a new image.
        This callback receives a full image
        Default: None

    on_update: callable object, optional
        Called when an update is received.
        This callback receives an utf-8 string as argument.
        Default: None

    on_error: callable object, optional
        Called when an error occurs.
        This callback receives Exception as argument
        Default: None

    on_complete: callable object, optional
        Called when item stream received all fields.
        This callback has no argument.
        Default: None

    Raises
    ------
    Exception
        If request fails or if Refinitiv Services return an error

    Examples
    --------
    >>> import refinitiv.data as rd
    >>> APP_KEY = "app_key"
    >>> session = rd.session.desktop.Definition(app_key=APP_KEY).get_session()
    >>> session.open()
    >>>
    >>> euro = rd.delivery.omm_stream.Definition("EUR=").get_stream(session)
    >>> euro.open()
    >>>
    >>> def on_update(stream, msg):
    ...     print(msg)
    >>>
    >>> definition = rd.delivery.omm_stream.Definition("THB=")
    >>> thb = definition.get_stream(session)
    >>> thb.on_update(on_update)
    >>> thb.open()
    """

    def __init__(
        self,
        session,
        name,
        api=None,
        domain="MarketPrice",
        service=None,
        fields=None,
        extended_params=None,
        on_refresh=None,
        on_status=None,
        on_update=None,
        on_error=None,
        on_complete=None,
    ):
        _OMMStream.__init__(
            self,
            session=session,
            name=name,
            api=api,
            domain=domain,
            service=service,
            fields=fields,
            extended_params=extended_params,
        )

        self.__item_stream_lock = Lock()
        self._message = None
        self._code = None

        self._on_refresh_callback = on_refresh
        self._on_status_callback = on_status
        self._on_update_callback = on_update
        self._on_error_callback = on_error
        self._on_complete_callback = on_complete

    @property
    def status(self):
        _st = dict(
            [("status", self.state), ("code", self._code), ("message", self._message)]
        )
        return _st

    #######################################
    #  methods to open and close session  #
    #######################################
    def open(self, with_updates: bool = True) -> StreamState:
        """
        Opens the OMMStream to start to stream. Once it's opened, it can be used in order to retrieve data.

        Parameters
        ----------
        with_updates : bool, optional
            actions:
                True - the streaming will work as usual and the data will be received continuously.
                False - only one data snapshot will be received (single Refresh 'NonStreaming') and stream will be closed automatically.

            Defaults to True

        Returns
        -------
        StreamState
            current state of this OMM stream object.

        Examples
        --------
        >>> from refinitiv.data.delivery import omm_stream
        >>> definition = omm_stream.Definition("EUR")
        >>> stream = definition.get_stream()
        >>> stream.open()
        """
        return _OMMStream.open(self, with_updates=with_updates)

    async def open_async(self, with_updates: bool = True) -> StreamState:
        """
        Opens asynchronously the OMMStream to start to stream

        Parameters
        ----------
        with_updates : bool, optional
            actions:
                True - the streaming will work as usual and the data will be received continuously.
                False - only one data snapshot will be received (single Refresh 'NonStreaming') and stream will be closed automatically.

        Returns
        -------
        StreamState
            current state of this OMM stream object.

        Examples
        --------
        >>> from refinitiv.data.delivery import omm_stream
        >>> definition = omm_stream.Definition("EUR")
        >>> stream = definition.get_stream()
        >>> await stream.open_async()
        """
        return await _OMMStream.open_async(self, with_updates=with_updates)

    def close(self) -> StreamState:
        """
        Closes the OMMStream connection, releases resources

        Returns
        -------
        StreamState
            current state of this OMM stream object.

        Examples
        --------
        >>> from refinitiv.data.delivery import omm_stream
        >>> definition = omm_stream.Definition("EUR")
        >>> stream = definition.get_stream()
        >>> stream.open()
        >>> stream.close()
        """
        if self._session:
            self._session.debug(f"Close OMMStream subscription {self.stream_id}")

        state = super(OMMStream, self).close()
        self._code = "Closed"
        self._message = ""
        return state

    ################################################
    #  methods to open asynchronously item stream  #
    ################################################
    async def _do_open_async(self, with_updates=True):
        """
        Open the data stream
        """
        self._session.debug(
            f"Open asynchronously OMMStream {self.stream_id} to {self._name}"
        )
        if self._name is None:
            raise AttributeError("name parameter is mandatory")

        return await super()._do_open_async(with_updates=with_updates)

    #############################
    # OMMStream properties      #
    #############################

    def on_refresh(self, func: Callable):
        """
        This function called when the stream is opened or when the record is refreshed with a new image.
        This callback receives a full image.

        Parameters
        ----------
        func : Callable, optional
             Callable object to process retrieved refresh data

        Returns
        -------
        OMMStream
            current instance it is a OMM stream object.

        Examples
        --------
        Prerequisite: The default session must be opened.
        >>> from datetime import datetime
        >>> from refinitiv.data.delivery import omm_stream
        >>>
        >>> def display_response(response, event_type, event):
                print(f'{response} - {event_type} received at {datetime.now}')
                print(event)
        >>>
        >>> definition = omm_stream.Definition("EUR")
        >>> stream = definition.get_stream()
        >>> stream.on_refresh(lambda stream, event: display_response(stream, 'refresh', event))
        >>>
        >>> stream.open()
        """
        self._on_refresh_callback = func
        return self

    def on_update(self, func: Callable):
        """
        This function called when an update is received.

        Parameters
        ----------
        func : Callable, optional
            Callable object to process retrieved update data

        Returns
        -------
        OMMStream
            current instance it is a OMM stream object.

        Examples
        --------
        Prerequisite: The default session must be opened.
        >>> from datetime import datetime
        >>> from refinitiv.data.delivery import omm_stream
        >>>
        >>> def display_response(response, event_type, event):
                print(f'{response} - {event_type} received at {datetime.now}')
                print(event)
        >>>
        >>> definition = omm_stream.Definition("EUR")
        >>> stream = definition.get_stream()
        >>> stream.on_update(lambda stream, event: display_response(stream, 'update', event))
        >>>
        >>> stream.open()
        """
        self._on_update_callback = func
        return self

    def on_status(self, func: Callable):
        """
        This function these notifications are emitted when the status of one of the requested instruments changes

        Parameters
        ----------
        func : Callable, optional
            Callable object to process retrieved status data

        Returns
        -------
        OMMStream
            current instance it is a OMM stream object.

        Examples
        --------
        Prerequisite: The default session must be opened.
        >>> from datetime import datetime
        >>> from refinitiv.data.delivery import omm_stream
        >>>
        >>> def display_response(response, event_type, event):
                print(f'{response} - {event_type} received at {datetime.now}')
                print(event)
        >>>
        >>> definition = omm_stream.Definition("EUR")
        >>> stream = definition.get_stream()
        >>> stream.on_status(lambda stream, event: display_response(stream, 'status', event))
        >>>
        >>> stream.open()
        """
        self._on_status_callback = func
        return self

    def on_error(self, func: Callable):
        """
        This function called when an error occurs

        Parameters
        ----------
        func : Callable, optional
            Callable object to process when retrieved error data.

        Returns
        -------
        OMMStream
            current instance it is a OMM stream object.

        Examples
        --------
        Prerequisite: The default session must be opened.
        >>> from datetime import datetime
        >>> from refinitiv.data.delivery import omm_stream
        >>>
        >>> def display_response(response, event_type, event):
                print(f'{response} - {event_type} received at {datetime.now}')
                print(event)
        >>>
        >>> definition = omm_stream.Definition("EUR")
        >>> stream = definition.get_stream()
        >>> stream.on_error(lambda stream, event: display_response(stream, 'error', event))
        >>>
        >>> stream.open()
        """
        self._on_error_callback = func
        return self

    def on_complete(self, func: Callable):
        """
        This function called on complete event

        Parameters
        ----------
        func : Callable, optional
            Callable object to process when retrieved on complete data.

        Returns
        -------
        OMMStream
            current instance it is a OMM stream object.

        Examples
        --------
        Prerequisite: The default session must be opened.
        >>> from datetime import datetime
        >>> from refinitiv.data.delivery import omm_stream
        >>>
        >>> def display_response(response, event_type, event):
                print(f'{response} - {event_type} received at {datetime.now}')
                print(event)
        >>>
        >>> definition = omm_stream.Definition("EUR")
        >>> stream = definition.get_stream()
        >>> stream.on_complete(lambda stream, event: display_response(stream, 'complete', event))
        >>>
        >>> stream.open()
        """
        self._on_complete_callback = func
        return self

    ###########################################
    # Process messages from stream connection #
    ###########################################
    def _on_refresh(self, message):
        with self.__item_stream_lock:
            self._status = message.get("State")
            stream_state = self._status.get("Stream")
            self._code = stream_state
            self._message = self._status.get("Text")

            super()._on_refresh(message)
            if not self.is_close and self._on_refresh_callback:
                try:
                    self._session.log(1, "OMMStream : call on_refresh callback")
                    self._on_refresh_callback(self, message)
                except Exception as e:
                    self._session.log(
                        logging.ERROR,
                        f"OMMStream on_refresh callback raised exception: {e!r}",
                    )
                    self._session.log(1, f"{traceback.format_exc()}")

    def _on_status(self, status):
        with self.__item_stream_lock:
            state = status.get("State")
            stream_state = state.get("Stream")
            self._code = stream_state
            self._message = state.get("Text")

            if stream_state in ["Closed", "ClosedRecover", "NonStreaming", "Redirect"]:
                self.state = StreamState.Closed
                self._code = state.get("Code")
                self._session.log(
                    1, "Set stream {} as {}".format(self.stream_id, self._state)
                )
            if self._on_status_callback:
                try:
                    self._session.log(1, "OMMStream : call on_status callback")
                    self._on_status_callback(self, self.status)
                except Exception as e:
                    self._session.log(
                        logging.ERROR,
                        f"OMMStream on_status callback raised exception: {e!r}",
                    )
                    self._session.log(1, f"{traceback.format_exc()}")
            super()._on_status(status)

    def _on_update(self, update):
        with self.__item_stream_lock:
            super()._on_update(update)
            if self.state is not StreamState.Closed and self._on_update_callback:
                try:
                    self._session.log(1, "OMMStream : call on_update callback")
                    self._on_update_callback(self, update)
                except Exception as e:
                    self._session.log(
                        logging.ERROR,
                        f"OMMStream on_update callback raised exception: {e!r}",
                    )
                    self._session.log(1, f"{traceback.format_exc()}")

    def _on_complete(self):
        with self.__item_stream_lock:
            super()._on_complete()
            if self.state is not StreamState.Closed and self._on_complete_callback:
                try:
                    self._session.log(1, "OMMStream : call on_complete callback")
                    self._on_complete_callback(self)
                except Exception as e:
                    self._session.log(
                        logging.ERROR,
                        f"OMMStream on_complete callback raised exception: {e!r}",
                    )
                    self._session.log(1, f"{traceback.format_exc()}")

    def _on_error(self, error):
        with self.__item_stream_lock:
            super()._on_error(error)
            if self.state is not StreamState.Closed:
                self._message = error
                if self._on_error_callback:
                    try:
                        self._session.log(1, "OMMStream: call on_error callback")
                        self._on_error_callback(self, error)
                    except Exception as e:
                        self._session.log(
                            logging.ERROR,
                            f"OMMStream on_error callback raised an exception: {e!r}",
                        )
                        self._session.log(1, f"{traceback.format_exc()}")
