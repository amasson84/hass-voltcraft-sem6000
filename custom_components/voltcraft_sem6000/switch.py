from homeassistant.components.switch import PLATFORM_SCHEMA, SwitchEntity
from homeassistant.const import CONF_MAC, CONF_NAME, CONF_PASSWORD
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.restore_state import RestoreEntity

import voluptuous as vol

from custom_components.voltcraft_sem6000.sem6000 import sem6000

DEFAULT_NAME = "sem6000"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_MAC): cv.string,
        vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
        vol.Optional(CONF_PASSWORD): cv.string,
    }
)
def setup_platform(hass, config, add_entities, discovery_info=None):
    """Perform the setup for Switchbot devices."""
    name = config.get(CONF_NAME)
    mac_addr = config[CONF_MAC]
    password = config.get(CONF_PASSWORD)
    add_entities([SwitchSEM6000(mac_addr, name, password)])


class SwitchSEM6000(SwitchEntity, RestoreEntity):
    """Representation of a Switch for sem 6000."""

    def __init__(self, mac, name, password) -> None:
        """Initialize."""

        self._last_run_success = None
        self._name = name
        self._mac = mac
        self._device = sem6000.SEM6000(deviceAddr=mac, pin=password)



    def turn_on(self, **kwargs) -> None:
        """Turn device on."""
        if self._device.power_on():
            self._last_run_success = True
        else:
            self._last_run_success = False

    def turn_off(self, **kwargs) -> None:
        """Turn device off."""
        if self._device.power_off():
            self._last_run_success = True
        else:
            self._last_run_success = False


    @property
    def is_on(self) -> bool:
        """Return true if device is on."""
        response = sem6000.request_measurement()
        return response.is_power_active

    @property
    def unique_id(self) -> str:
        """Return a unique, Home Assistant friendly identifier for this entity."""
        return self._mac.replace(":", "")

    @property
    def name(self) -> str:
        """Return the name of the switch."""
        return self._name

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the state attributes."""
        return {"last_run_success": self._last_run_success}