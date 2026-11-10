"""Local namedays calendar and coordinator."""

from datetime import timedelta
import logging

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import DOMAIN
from .namedays import CALENDAR

_LOGGER = logging.getLogger(__name__)


class NamedaysUpdateCoordinator(DataUpdateCoordinator):
    """Serve the bundled offline namedays calendar."""

    def __init__(self, hass):
        """Initialize the coordinator with local data only."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(days=1),
        )

    async def _async_update_data(self):
        """Return the bundled calendar; no network requests are made."""
        return CALENDAR
