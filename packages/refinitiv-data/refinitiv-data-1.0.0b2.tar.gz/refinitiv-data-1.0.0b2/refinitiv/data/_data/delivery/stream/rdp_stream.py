# coding: utf-8

import traceback
from threading import Lock
from typing import Callable

from ._rdp_stream import _RDPStream
from .state import StreamState


class RDPStream(_RDPStream):
    """
    Open an RDP stream.

    Parameters
    ----------

    service: string, optional
        name of RDP service

    universe: list
        RIC to retrieve item stream.

    view: list
        data fields to retrieve item stream

    parameters: dict
        extra parameters to retrieve item stream.

    api: string
        specific name of RDP streaming defined in config file. i.e.
        'streaming/trading-analytics/redi'

    extended_params: dict, optional
        Specify optional params
        Default: None

    on_ack: callable object, optional
        Called when an ack is received.
        This callback receives an utf-8 string as argument.
        Default: None

    on_response: callable object, optional
        Called when an response is received.
        This callback receives an utf-8 string as argument.
        Default: None

    on_update: callable object, optional
        Called when an update is received.
        This callback receives an utf-8 string as argument.
        Default: None

    on_alarm: callable object, optional
        Called when an alarm is received.
        This callback receives an utf-8 string as argument.
        Default: None

    Raises
    ------
    Exception
        If request fails or if Refinitiv Services return an error

    Examples
    --------
    >>> import refinitiv.data as rd
    >>> APP_KEY = "APP_KEY"
    >>> USERNAME = "USERNAME"
    >>> PASSWORD = "PASSWORD"
    >>> session = rd.session.platform.Definition(
    ...         app_key=APP_KEY,
    ...         grant=rd.session.platform.GrantPassword(
    ...             username=USERNAME,
    ...             password=PASSWORD,
    ...         )
    ... ).get_session()
    >>> session.open()
    >>>
    >>> tds = rd.delivery.rdp_stream.Definition(
    ...     service="",
    ...     universe=[],
    ...     view=[],
    ...     parameters={"universeType": "RIC"},
    ...     api='streaming/trading-analytics/redi'
    ... ).get_stream(session)
    >>> tds.open()
    """

    def __init__(
        self,
        session,
        service: str,
        universe: list,
        view: list,
        parameters: dict,
        api: str,
        extended_params=None,
        on_ack=None,
        on_response=None,
        on_update=None,
        on_alarm=None,
    ):
        _RDPStream.__init__(self, session, api)

        #   lock for callback function
        self.__item_stream_lock = Lock()

        #   set the RDP stream parameters
        #       set in the parent class
        self._service = service
        self._universe = universe
        self._view = view
        self._parameters = parameters

        #   RPD item stream parameters
        self._extended_params = extended_params

        #   callback functions
        self._on_ack_callback = on_ack
        self._on_response_callback = on_response
        self._on_update_callback = on_update
        self._on_alarm_callback = on_alarm

        #   last callback code and message
        self._message = None
        self._code = None

        #   validate parameters
        if self._session is None:
            raise AttributeError("Session must be defined")

    def _on_ack(self, ack):
        with self.__item_stream_lock:

            #   call parent class method
            super()._on_ack(ack)

            #   call callback function
            if self._on_ack_callback:
                self._session.debug("RDPStream : call on_ack callback.")
                try:
                    self._on_ack_callback(self, ack)
                except Exception as e:
                    self._session.error(
                        f"RDPStream on_ack callback raised exception: {e!r}"
                    )
                    self._session.debug(f"{traceback.format_exc()}")

    def _on_response(self, response):
        with self.__item_stream_lock:
            #   call parent class method
            super()._on_response(response)
            #   call callback function
            if self._on_response_callback:
                self._session.debug("RDPStream : call on_response callback.")
                try:
                    self._on_response_callback(self, response)
                except Exception as e:
                    self._session.error(
                        f"RDPStream on_response callback raised exception: {e!r}"
                    )
                    self._session.debug(f"{traceback.format_exc()}")

    def _on_update(self, update):
        with self.__item_stream_lock:
            #   call parent class method
            super()._on_update(update)

            #   call callback function
            if self._on_update_callback:
                self._session.debug("RDPStream : call on_update callback.")
                try:
                    self._on_update_callback(self, update)
                except Exception as e:
                    self._session.error(
                        f"RDPStream on_update callback raised exception: {e!r}"
                    )
                    self._session.debug(f"{traceback.format_exc()}")

    def _on_alarm(self, alarm):
        with self.__item_stream_lock:
            #   call parent class method
            super()._on_alarm(alarm)

            #   call callback function
            if self._on_alarm_callback:
                self._session.debug("RDPStream : call on_alarm callback.")
                try:
                    self._on_alarm_callback(self, alarm)
                except Exception as e:
                    self._session.error(
                        f"RDPStream on_alarm callback raised exception: {e!r}"
                    )
                    self._session.debug(f"{traceback.format_exc()}")

    #######################################
    #  methods to open and close session  #
    #######################################
    def open(self) -> StreamState:
        """
        Opens the RDPStream to start to stream. Once it's opened, it can be used in order to retrieve data.

        Parameters
        ----------

        Returns
        -------
        StreamState
            current state of this RDP stream object.

        Examples
        --------
        >>> from refinitiv.data.delivery import rdp_stream
        >>> definition = rdp_stream.Definition(
                                service=None,
                                universe=[],
                                view=None,
                                parameters={"universeType": "RIC"},
                                api='streaming/trading-analytics/redi')
        >>> stream = definition.get_stream()
        >>> await stream.open_async()
        """
        return _RDPStream.open(self)

    async def open_async(self) -> StreamState:
        """
        Opens asynchronously the RDPStream to start to stream

        Parameters
        ----------

        Returns
        -------
        StreamState
            current state of this RDP stream object.

        Examples
        --------
        >>> from refinitiv.data.delivery import rdp_stream
        >>> definition = rdp_stream.Definition(
                                service=None,
                                universe=[],
                                view=None,
                                parameters={"universeType": "RIC"},
                                api='streaming/trading-analytics/redi')
        >>> stream = definition.get_stream()
        >>> await stream.open_async()
        """
        return await _RDPStream.open_async(self)

    def close(self) -> StreamState:
        """
        Closes the RPDStream connection, releases resources

        Returns
        -------
        StreamState
            current state of this RDP stream object.

        Examples
        --------
        >>> from refinitiv.data.delivery import rdp_stream
        >>> definition = rdp_stream.Definition(
                                service=None,
                                universe=[],
                                view=None,
                                parameters={"universeType": "RIC"},
                                api='streaming/trading-analytics/redi')
        >>> stream = definition.get_stream()
        >>> stream.open()
        >>> stream.close()
        """
        return _RDPStream.close(self)

    async def close_async(self) -> StreamState:
        """
        Closes asynchronously the RPDStream connection, releases resources

        Returns
        -------
        StreamState
            current state of this RDP stream object.

        Examples
        --------
        >>> from refinitiv.data.delivery import rdp_stream
        >>> definition = rdp_stream.Definition(
                                service=None,
                                universe=[],
                                view=None,
                                parameters={"universeType": "RIC"},
                                api='streaming/trading-analytics/redi')
        >>> stream = definition.get_stream()
        >>> stream.open()
        >>> await stream.close_async()
        """
        return await _RDPStream.close_async(self)

    #############################
    # RDPStream properties      #
    #############################

    def on_ack(self, on_ack: Callable):
        """
        This function called when the stream received an ack message.

        Parameters
        ----------
        on_ack : Callable, optional
             Callable object to process retrieved ack data

        Returns
        -------
        RDPStream
            current instance it is a RDP stream object.

        Examples
        --------
        Prerequisite: The default session must be opened.
        >>> from datetime import datetime
        >>> from refinitiv.data.delivery import rdp_stream
        >>>
        >>> def display_response(response, event_type, event):
        ...     print(f'{response} - {event_type} received at {datetime.now}')
        ...     print(event)
        >>>
        >>> definition = rdp_stream.Definition(
        ...                     service=None,
        ...                     universe=[],
        ...                     view=None,
        ...                     parameters={"universeType": "RIC"},
        ...                     api='streaming/trading-analytics/redi')
        >>> stream = definition.get_stream()
        >>> stream.on_ack(lambda stream, event: display_response(stream, 'ack', event))
        >>>
        >>> stream.open()
        """
        self._on_ack_callback = on_ack
        return self

    def on_response(self, on_response):
        """
        This function called when the stream received an response message.

        Parameters
        ----------
        on_response : Callable, optional
             Callable object to process retrieved response data

        Returns
        -------
        RDPStream
            current instance it is a RDP stream object.

        Examples
        --------
        Prerequisite: The default session must be opened.
        >>> from datetime import datetime
        >>> from refinitiv.data.delivery import rdp_stream
        >>>
        >>> def display_response(response, event_type, event):
                print(f'{response} - {event_type} received at {datetime.now}')
                print(event)
        >>>
        >>> definition = rdp_stream.Definition(
                                service=None,
                                universe=[],
                                view=None,
                                parameters={"universeType": "RIC"},
                                api='streaming/trading-analytics/redi')
        >>> stream = definition.get_stream()
        >>> stream.on_response(lambda stream, event: display_response(stream, 'response', event))
        >>>
        >>> stream.open()
        """
        self._on_response_callback = on_response
        return self

    def on_update(self, on_update):
        """
        This function called when the stream received an update message.

        Parameters
        ----------
        on_update : Callable, optional
             Callable object to process retrieved update data

        Returns
        -------
        RDPStream
            current instance it is a RDP stream object.

        Examples
        --------
        Prerequisite: The default session must be opened.
        >>> from datetime import datetime
        >>> from refinitiv.data.delivery import rdp_stream
        >>>
        >>> def display_response(response, event_type, event):
                print(f'{response} - {event_type} received at {datetime.now}')
                print(event)
        >>>
        >>> definition = rdp_stream.Definition(
                                service=None,
                                universe=[],
                                view=None,
                                parameters={"universeType": "RIC"},
                                api='streaming/trading-analytics/redi')
        >>> stream = definition.get_stream()
        >>> stream.on_update(lambda stream, event: display_response(stream, 'update', event))
        >>>
        >>> stream.open()
        """
        self._on_update_callback = on_update
        return self

    def on_alarm(self, on_alarm):
        """
        This function called when the stream received an alarm message.

        Parameters
        ----------
        on_alarm : Callable, optional
             Callable object to process retrieved alarm data

        Returns
        -------
        RDPStream
            current instance it is a RDP stream object.

        Examples
        --------
        Prerequisite: The default session must be opened.
        >>> from datetime import datetime
        >>> from refinitiv.data.delivery import rdp_stream
        >>>
        >>> def display_response(response, event_type, event):
                print(f'{response} - {event_type} received at {datetime.now}')
                print(event)
        >>>
        >>> definition = rdp_stream.Definition(
                                service=None,
                                universe=[],
                                view=None,
                                parameters={"universeType": "RIC"},
                                api='streaming/trading-analytics/redi')
        >>> stream = definition.get_stream()
        >>> stream.on_alarm(lambda stream, event: display_response(stream, 'alarm', event))
        >>>
        >>> stream.open()
        """
        self._on_alarm_callback = on_alarm
        return self
