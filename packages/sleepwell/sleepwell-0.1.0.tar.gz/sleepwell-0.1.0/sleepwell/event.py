"""
define the event objects 

format data to be sent 
"""
import json
import requests
from sleepwell import state


class Event:
    """

    Event class for recording events to be sent on Sleep well API

    """

    def __init__(self, data={}):
        self._data = data

    def add_field(self, key, value):
        self._data[key] = value

    def add(self, data):
        try:
            for k, v in data.items():
                self.add_field(k, v)

        except AttributeError:
            raise TypeError("add requires a dict-like argument")

    def is_empty(self):
        return len(self.data) == 0

    def __str__(self):
        return json.dumps(self.data)

    def send(self):
        if state.URL == None:
            return Exception("No url provided")

        requests.post(
            state.URL,
            headers={"Content-type": "application/json"},
            data=json.dumps(self._data),
        )
