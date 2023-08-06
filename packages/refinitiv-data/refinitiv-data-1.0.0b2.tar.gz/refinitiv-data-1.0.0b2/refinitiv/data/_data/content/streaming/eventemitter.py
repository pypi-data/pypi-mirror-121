from eventemitter import EventEmitter


class OneListenerEventEmitter(EventEmitter):
    def add_listener(self, event, listener):
        try:
            self.remove_all_listeners(event)
        except KeyError:
            # silent
            pass
        return super().add_listener(event, listener)

    on = add_listener
