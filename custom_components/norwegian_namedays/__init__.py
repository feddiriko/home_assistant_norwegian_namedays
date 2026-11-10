"""Set up the offline Norwegian Namedays integration."""

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er

from .const import DOMAIN

PLATFORMS = ["sensor"]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up sensors and migrate legacy entity IDs where possible."""
    _migrate_entity_registry(hass, entry)
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload the integration platforms."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)


def _migrate_entity_registry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Replace config-entry-random IDs with stable integration entity IDs."""
    registry = er.async_get(hass)
    for key in ("today", "comment"):
        old_unique_id = f"{entry.entry_id}_{key}"
        new_unique_id = f"{DOMAIN}_{key}"
        entity_id = registry.async_get_entity_id("sensor", DOMAIN, old_unique_id)
        if entity_id is None or registry.async_get_entity_id("sensor", DOMAIN, new_unique_id):
            continue
        registry.async_update_entity(
            entity_id,
            new_unique_id=new_unique_id,
            new_entity_id=f"sensor.{new_unique_id}",
        )
