"""Offline Norwegian name-day sensors."""

from __future__ import annotations

from typing import Any

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription
from homeassistant.core import callback
from homeassistant.helpers.event import async_track_time_change
from homeassistant.util import dt as dt_util

from .const import DOMAIN
from .namedays import CALENDAR

NO_NAME_DAY = "No name day"
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
    """Set up the calendar sensors."""
    async_add_entities(
        [NamedaysSensor(description) for description in SENSORS],
        update_before_add=True,
    )


class NamedaysSensor(SensorEntity):
    """Show today's name day or the explanatory comment."""

    entity_description: SensorEntityDescription

    def __init__(self, description: SensorEntityDescription) -> None:
        """Initialize a sensor with a stable identity."""
        self.entity_description = description
        self._attr_unique_id = f"{DOMAIN}_{description.key}"
        self._attr_suggested_object_id = self._attr_unique_id

    async def async_added_to_hass(self) -> None:
        """Refresh when the local day rolls over."""
        await super().async_added_to_hass()
        self.async_on_remove(
            async_track_time_change(
                self.hass,
                self._handle_midnight,
                hour=0,
                minute=0,
                second=0,
            )
        )

    @callback
    def _handle_midnight(self, _now) -> None:
        """Write a fresh state at midnight."""
        self.async_write_ha_state()

    @property
    def native_value(self) -> str | None:
        """Return the current names or comment."""
        item = self._today_item()
        if item is None:
            return NO_NAME_DAY if self.entity_description.key == "today" else None

        if self.entity_description.key == "today":
            names = item.get("names")
            if not isinstance(names, list):
                return NO_NAME_DAY
            value = ", ".join(str(name).strip() for name in names if str(name).strip())
            return value or NO_NAME_DAY

        comment = item.get("comment")
        if not isinstance(comment, str) or not comment.strip():
            return None
        comment = comment.strip()
        return comment if len(comment) <= MAX_STATE_LENGTH else comment[: MAX_STATE_LENGTH - 1] + "…"

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Expose the comment data and the offline source metadata."""
        item = self._today_item()
        if self.entity_description.key == "comment":
            comment = item.get("comment", "") if item else ""
            comment = comment.strip() if isinstance(comment, str) else ""
            return {
                "comment_available": bool(comment),
                **({"full_comment": comment} if len(comment) > MAX_STATE_LENGTH else {}),
            }
        return {
            "data_source": "Bundled offline calendar (Norwegian Wikipedia namedays list)",
        }

    @staticmethod
    def _today_item() -> dict[str, Any] | None:
        """Look up today's entry in the offline calendar."""
        today = dt_util.now().date()
        for item in CALENDAR:
            if item.get("month") == today.month and item.get("day") == today.day:
                return item
        return None
