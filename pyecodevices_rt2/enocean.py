from . import EcoDevicesRT2, AbstractSwitch

from .const import (
    ENOCEAN_GET_LINK,
    ENOCEAN_SWITCH_GET_ENTRY,
    ENOCEAN_SWITCH_ON_LINK,
    ENOCEAN_SWITCH_OFF_LINK,
    ENOCEAN_SWITCH_TOGGLE_LINK,
    ENOCEAN_SENSOR_GET_ENTRY,
)


class EnOceanSwitch(AbstractSwitch):
    """Class representing the EnOceanSwitch"""

    def __init__(self, ecort2: EcoDevicesRT2, id: int) -> None:
        super(EnOceanSwitch, self).__init__(
            ecort2, id,
            ENOCEAN_GET_LINK, ENOCEAN_SWITCH_GET_ENTRY,
            ENOCEAN_SWITCH_ON_LINK, ENOCEAN_SWITCH_OFF_LINK, ENOCEAN_SWITCH_TOGGLE_LINK)


class EnOceanSensor:
    """Class representing the EnOceanSensor """

    def __init__(self, ecort2: EcoDevicesRT2, id: int) -> None:
        self._ecort2 = ecort2
        self._id = id

    @property
    def value(self) -> float:
        """Return the current EnOceanSwitch status."""
        response = self._ecort2.get(ENOCEAN_GET_LINK)
        return response[ENOCEAN_SENSOR_GET_ENTRY % (self._id)]
