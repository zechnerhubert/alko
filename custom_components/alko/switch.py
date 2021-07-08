"""Support for AL-KO switch platform."""
import logging

from typing import Any

from pyalko.objects.device import AlkoDevice
from pyalko.exceptions import AlkoException

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from . import AlkoDeviceEntity
from .const import (
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities
) -> None:
    """Set up the AL-KO select platform based on a config entry."""
    coordinator: DataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    entities = []

    for device in coordinator.data.devices:
        entities.append(
            AlkoEcoModeSwitch(coordinator, device)
        )

        entities.append(
            AlkoRainSensorSwitch(coordinator, device)
        )

    async_add_entities(entities, True)


class AlkoEcoModeSwitch(AlkoDeviceEntity, SwitchEntity):
    """Defines an AL-KO switch."""

    _attr_icon = "mdi:tree"

    def __init__(
        self,
        coordinator: DataUpdateCoordinator,
        device: AlkoDevice
    ) -> None:
        """Initialize AL-KO switch."""
        super().__init__(
            coordinator,
            device,
            f"{device.thingName}_eco_mode",
            "Eco Mode",
        )

        self._state = self.device.thingState.state.reported.ecoMode

    @property
    def is_on(self) -> bool:
        """Return the state of the switch."""
        return self._state

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn off eco mode switch."""
        try:
            await self._update_device(self.device, ecoMode=False)
        except AlkoException as exception:
            _LOGGER.error(exception)
        self._state = False
        await self.coordinator.async_refresh()

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn on eco mode switch."""
        try:
            await self._update_device(self.device, ecoMode=True)
        except AlkoException as exception:
            _LOGGER.error(exception)
        self._state = True
        await self.coordinator.async_refresh()


class AlkoRainSensorSwitch(AlkoDeviceEntity, SwitchEntity):
    """Defines an AL-KO switch."""

    _attr_icon = "mdi:weather-rainy"

    def __init__(
        self,
        coordinator: DataUpdateCoordinator,
        device: AlkoDevice
    ) -> None:
        """Initialize AL-KO switch."""
        super().__init__(
            coordinator,
            device,
            f"{device.thingName}_rain_sensor",
            "Rain Sensor",
        )

        self._state = self.device.thingState.state.reported.rainSensor

    @property
    def is_on(self) -> bool:
        """Return the state of the switch."""
        return self._state

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn off rain sensor switch."""
        try:
            await self._update_device(self.device, rainSensor=False)
        except AlkoException as exception:
            _LOGGER.error(exception)
        self._state = False
        await self.coordinator.async_refresh()

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn on rain sensor switch."""
        try:
            await self._update_device(self.device, rainSensor=True)
        except AlkoException as exception:
            _LOGGER.error(exception)
        self._state = True
        await self.coordinator.async_refresh()
