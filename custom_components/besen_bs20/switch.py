"""Switch platform for Besen BS20."""

from __future__ import annotations

from homeassistant.components.switch import SwitchEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import BesenBS20ConfigEntry
from .entity import BesenBS20Entity

PARALLEL_UPDATES = 0


async def async_setup_entry(
    hass: HomeAssistant,
    entry: BesenBS20ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Besen BS20 switches."""

    async_add_entities([BesenBS20ChargeSwitch(entry.runtime_data.coordinator)])


class BesenBS20ChargeSwitch(BesenBS20Entity, SwitchEntity):
    """Charging control switch."""

    _attr_icon = "mdi:ev-plug-type2"

    def __init__(self, coordinator) -> None:
        """Initialize the switch."""

        super().__init__(coordinator, "charging", name="Charge")

    @property
    def is_on(self) -> bool | None:
        """Return whether charging is active."""

        data = self.coordinator.data or self.coordinator.client.state
        return data.charge.charger_status

    async def async_turn_on(self, **kwargs) -> None:
        """Start charging."""

        await self.coordinator.async_start_charging()

    async def async_turn_off(self, **kwargs) -> None:
        """Stop charging."""

        await self.coordinator.async_stop_charging()
