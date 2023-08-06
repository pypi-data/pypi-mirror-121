__version__ = "0.1.0"

"""
1. Initiation step.

2. Add initial data

3. add single field 

4. send data to REST API

"""


from sleepwell.event import Event
from sleepwell import state


def init(url=""):
    state.URL = url


def new_event(data={}):
    return Event(data=data)


__all__ = ["new_event"]
