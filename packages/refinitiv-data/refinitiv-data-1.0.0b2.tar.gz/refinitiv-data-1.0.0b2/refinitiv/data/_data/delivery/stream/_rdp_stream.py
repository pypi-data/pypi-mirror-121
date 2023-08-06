# coding: utf-8

import asyncio
import json

from .stream import Stream, StreamState


class _RDPStream(Stream):
    """
    This class is designed for the generic RDP stream.

    The following are the subscription message from the stream:
    - ack message
    - response message
    - update message
    - alarm message
    """

    def __init__(self, session, api):
        Stream.__init__(self, session, api)

        self._service = None
        self._universe = None
        self._view = None
        self._parameters = None
        self._extended_params = None
        self._subscribe_future = None

    @property
    def service(self):
        return self._service

    @service.setter
    def service(self, val):
        self._service = val

    @property
    def universe(self):
        return self._universe

    @universe.setter
    def universe(self, val):
        self._universe = val

    @property
    def view(self):
        return self._view

    @view.setter
    def view(self, val):
        self._view = val

    @property
    def parameters(self):
        return self._parameters

    @parameters.setter
    def parameters(self, val):
        self._parameters = val

    @property
    def extended_params(self):
        return self._extended_params

    @extended_params.setter
    def extended_params(self, val):
        self._extended_params = val

    @property
    def name(self):
        return self._universe

    @property
    def protocol_name(self):
        return "RDP"

    async def _do_open_async(self, **kwargs):
        self._session._register_stream(self)

        result = await self._session.wait_for_streaming(self.api, self.protocol_name)

        if result:
            self._initialize_subscribe_response_future()

            subscription_message = self._get_subscription_request_message()
            self._session.debug(f"subscription message = {subscription_message}")
            self._send(subscription_message)

            await self._wait_for_subscribe_response()

        else:
            self.state = StreamState.Closed
            self._session.debug(
                f"Start streaming failed. Set stream {self.stream_id} as {self.state}"
            )

        return self.state

    async def _do_close_async(self, **kwargs):
        """
        Close the data stream

        Example of close for generic RDP streaming

        {
            "streamID": "42",
            "method": "Close"
        }
        """
        self._session.debug(f"Close Stream subscription {self.stream_id}")
        self._initialize_unsubscribe_response_future()
        close_message = {"streamID": f"{self.stream_id:d}", "method": "Close"}
        self._session.debug(
            f"Sent close subscription:\n"
            f'{json.dumps(close_message, sort_keys=True, indent=2, separators=(",", ":"))}'
        )
        self._send(close_message)

        if (
            self._subscribe_response_future is not None
            and not self._subscribe_response_future.done()
        ):
            self._subscribe_response_future.cancel()

        try:
            await asyncio.wait_for(
                self._wait_for_unsubscribe_response(),
                timeout=30,
                loop=self._session.loop,
            )
        except asyncio.TimeoutError:
            self._session.warning(
                "WARNING!!! timeout occurred before received un-subscribed response."
            )

        self._session._unregister_stream(self)

    def _do_pause(self):
        # do nothing
        pass

    def _do_resume(self):
        # do nothing
        pass

    def _get_subscription_request_message(self):
        """
        Build the subscription request message

        Example of subscribe messages

            {
                "streamID": "42",
                "method": "Subscribe",
                "service": "analytics/bond/contract",
                "universe": [
                    {
                    "type": "swap",
                    "definition": {
                        "startDate": "2017-07-28T00:00:00Z",
                        "swapType": "Vanilla",
                        "tenor": "3Y"
                    }
                    }
                ],
                "view": [
                    "InstrumentDescription",
                    "ValuationDate",
                    "StartDate",
                    "EndDate",
                    "Calendar",
                    "FixedRate",
                    "PV01AmountInDealCcy",
                    "Duration",
                    "ModifiedDuration",
                    "ForwardCurveName",
                    "DiscountCurveName",
                    "ErrorMessage"
                ]
            }

        or

            {
                "streamID": "43",
                "method": "Subscribe",
                "service": "elektron/market-price",
                "universe": [
                    {
                    "name": "TRI.N"
                    }
                ]
            }

        or

            {
                "streamID": "1",
                "method": "Subscribe",
                "universe": [],
                "parameters": {
                    "universeType": "RIC"
                }
            }
        """
        subscription_message = {
            "streamID": f"{self.stream_id:d}",
            "method": "Subscribe",
            "universe": self._universe,
        }

        if self._service is not None:
            subscription_message["service"] = self._service

        if self._view is not None:
            subscription_message["view"] = self._view

        if self._parameters is not None:
            subscription_message["parameters"] = self._parameters

        if self._extended_params is not None:
            subscription_message = (
                self._update_subscription_message_with_extended_params(
                    self._session, subscription_message, self._extended_params
                )
            )

        return subscription_message

    async def _subscribe_async(self):
        """
        Subscribe RDP stream.
        The subscription steps are waiting for stream to be ready
        and send the message to subscribe item.
        """
        self._session.debug(
            f"_RDPStream.subscribe_async() - waiting for subscribe name = {self.name}"
        )

        result = await self._session.wait_for_streaming_reconnection(
            self.api, self.protocol_name
        )

        if not result:
            self._session.debug(
                "WARNING!!! "
                "the reconnection is failed, so waiting for new reconnection."
            )
            return

        get_subscription_request_message = self._get_subscription_request_message()
        self._session.debug(
            "open message = {}".format(get_subscription_request_message)
        )

        self._send(get_subscription_request_message)

    def _on_status(self, status):
        self._session.debug(
            f"Stream {self.stream_id} [{self.name}] - Receive status message {status}"
        )

    def _on_reconnect(
        self, failover_state, stream_state, data_state, state_code, state_text
    ):
        from .stream_connection import StreamConnection

        if failover_state == StreamConnection.FailoverState.FailoverCompleted:
            if self._subscribe_future is None or self._subscribe_future.done():
                self._session.debug(
                    "      call subscribe_async() function.............."
                )

                self._subscribe_future = asyncio.run_coroutine_threadsafe(
                    self._subscribe_async(), loop=self._loop
                )

        status_message = {
            "ID": self.stream_id,
            "Type": "Status",
            "Key": {"Name": self.name},
            "State": {
                "Stream": stream_state,
                "Data": data_state,
                "Code": state_code,
                "Text": state_text,
            },
        }

        self._on_status(status_message)

    def _on_ack(self, ack):
        with self._stream_lock:
            if self._state is StreamState.Open:
                self._session.debug(
                    f"Stream {self.stream_id} [{self.name}] - Receive ack {ack}"
                )

            state = ack.get("state", None)

            if state is not None:
                stream_state = state.get("stream", None)

                if stream_state == "Open":
                    self.state = StreamState.Open

                elif stream_state == "Closed":
                    self.state = StreamState.Closed

                    if (
                        self._unsubscribe_response_future is not None
                        and not self._unsubscribe_response_future.done()
                    ):
                        self._unsubscribe_response_future.set_result(True)

                else:
                    self._session.debug(
                        f"Stream {self.stream_id} [{self.name}] - "
                        f"Receive unsupported stream state {stream_state}",
                    )

    def _on_response(self, response):
        with self._stream_lock:
            self._session.debug(
                f"Stream {self.stream_id} [{self.name}] - Receive response {response}",
            )

            if self.is_close:
                self.state = StreamState.Open
                self._session.debug(f"Set stream {self.stream_id} as {self.state}")

            if (
                self._subscribe_response_future is not None
                and not self._subscribe_response_future.done()
            ):
                self._subscribe_response_future.set_result(True)

    def _on_update(self, update):
        with self._stream_lock:
            if self._state is StreamState.Open:
                self._session.debug(
                    f"Stream {self.stream_id} [{self.name}] - Receive update {update}",
                )

    def _on_alarm(self, message):
        with self._stream_lock:
            if self._state is StreamState.Open:
                self._session.debug(
                    f"Stream {self.stream_id} [{self.name}] - Receive alarm {message}",
                )
