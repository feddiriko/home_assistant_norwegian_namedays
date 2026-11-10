"""Sensor platform for Norwegian Namedays."""

from typing import Any

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.util import dt as dt_util

from .const import DOMAIN
from .coordinator import NamedaysUpdateCoordinator

NO_NAME_DAY = "No name day"
NO_COMMENT = "No comment available"
MAX_STATE_LENGTH = 255

SENSORS: tuple[SensorEntityDescription, ...] = (
    SensorEntityDescription(
        key="today",
        translation_key="today",
        icon="mdi:account-calendar",
    ),
    SensorEntityDescription(
        key="comment",
        translation_key="comment",
        icon="mdi:comment-text-outline",
    ),
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
        # Keep unique IDs stable for entity-registry continuity, but use a
        # readable object ID for new entities instead of exposing the random
        # config-entry ID in the entity ID.
        self._attr_unique_id = f"{entry_id}_{description.key}"
        self._attr_suggested_object_id = f"{DOMAIN}_{description.key}"

    @property
    def native_value(self) -> str:
        """Return today's names or a clear fallback when the value is empty."""
        item = self._today_item()
        if item is None:
            return NO_NAME_DAY if self.entity_description.key == "today" else NO_COMMENT

        if self.entity_description.key == "today":
            names = item.get("names")
            if not isinstance(names, list):
                return NO_NAME_DAY
            value = ", ".join(str(name).strip() for name in names if str(name).strip())
            return value or NO_NAME_DAY

        comment = item.get("comment")
        if not isinstance(comment, str) or not comment.strip():
            return NO_COMMENT
        # HA entity states have a 255-character limit. Keep a readable state and
        # provide the complete text in an attribute when it is longer.
        comment = comment.strip()
        return comment if len(comment) <= MAX_STATE_LENGTH else comment[: MAX_STATE_LENGTH - 1] + "…"

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Expose helpful calendar details and preserve long comment text."""
        item = self._today_item()
        if self.entity_description.key == "comment":
            comment = item.get("comment") if item else None
            comment = comment.strip() if isinstance(comment, str) else ""
            return {
                "comment_available": bool(comment),
                **({"full_comment": comment} if len(comment) > MAX_STATE_LENGTH else {}),
            }

        return {
            "all_names": [entry.get("names", []) for entry in self.coordinator.data],
            "data_source": "Bundled offline calendar (Wikipedia Norwegian namedays list)",
        }

    def _today_item(self) -> dict[str, Any] | None:
        """Find today's entry, including leap day, in the local calendar."""
        today = dt_util.now().date()
        return next(
            (
                item
                for item in self.coordinator.data
                if item.get("month") == today.month and item.get("day") == today.day
            ),
            None,
        )
