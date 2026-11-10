"""Sensor platform for Norwegian Namedays."""

from typing import Any

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.util import dt as dt_util

from .const import DOMAIN
from .coordinator import NamedaysUpdateCoordinator


SENSORS: tuple[SensorEntityDescription, ...] = (
    SensorEntityDescription(key="today", translation_key="today"),
    SensorEntityDescription(key="comment", translation_key="comment"),
)


async def async_setup_entry(hass, config_entry, async_add_entities) -> None:
    """Set up namedays sensors."""
    coordinator: NamedaysUpdateCoordinator = hass.data[DOMAIN][config_entry.entry_id]
    async_add_entities(
        NamedaysSensor(coordinator, config_entry.entry_id, description)
        for description in SENSORS
    )


class NamedaysSensor(CoordinatorEntity[NamedaysUpdateCoordinator], SensorEntity):
    """Representation of today's names or Wikipedia comment."""

    entity_description: SensorEntityDescription

    def __init__(self, coordinator, entry_id: str, description) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{entry_id}_{description.key}"

    @property
    def native_value(self) -> str | None:
        """Return today's names or comment from the bundled calendar."""
        item = self._today_item()
        if item is None:
            return None
        value = item.get("names" if self.entity_description.key == "today" else "comment")
        if isinstance(value, list):
            return ", ".join(value) or None
        return value or None

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Expose the local calendar on the names sensor."""
        if self.entity_description.key != "today":
            return {}
        return {
            "all_names": [item["names"] for item in self.coordinator.data],
            "data_source": "Bundled offline calendar (Wikipedia Norwegian namedays list)",
        }

    def _today_item(self) -> dict[str, Any] | None:
        """Find today's entry, including leap day, in the local calendar."""
        today = dt_util.now().date()
        return next(
            (
                item
                for item in self.coordinator.data
                if item["month"] == today.month and item["day"] == today.day
            ),
            None,
        )
