from . import EcoDevicesRT2

from .const import (
    COUNTER_GET_LINK,
    COUNTER_GET_ENTRY,
    COUNTER_SET_LINK,
    RESPONSE_ENTRY,
    RESPONSE_SUCCESS_VALUE
)


class Counter:
    """Class representing the Counter"""

    def __init__(self, ecort2: EcoDevicesRT2, id: int) -> None:
        self._ecort2 = ecort2
        self._id = id

    @property
    def value(self) -> float:
        """Return the current Counter value."""
        response = self._ecort2.get(COUNTER_GET_LINK)
        return response[COUNTER_GET_ENTRY % (self._id)]

    @value.setter
    def value(self, value: int):
        """Modify the current Counter value."""
        response = self._ecort2.get(COUNTER_SET_LINK % (self._id, str(value)))
        return response[RESPONSE_ENTRY] == RESPONSE_SUCCESS_VALUE

    def add(self, value: int):
        """Add a value to the current Counter value."""
        response = self._ecort2.get(COUNTER_SET_LINK % (self._id, "+%d" % value))
        return response[RESPONSE_ENTRY] == RESPONSE_SUCCESS_VALUE

    def substrat(self, value: int):
        """Substract a value to the current Counter value."""
        response = self._ecort2.get(COUNTER_SET_LINK % (self._id, "-%d" % value))
        return response[RESPONSE_ENTRY] == RESPONSE_SUCCESS_VALUE
