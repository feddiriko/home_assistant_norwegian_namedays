"""Config flow for the offline Norwegian Namedays integration."""

from homeassistant import config_entries

from .const import DOMAIN


class NamedaysConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Set up a single Norwegian Namedays calendar entry."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Create the config entry, preventing duplicates."""
        await self.async_set_unique_id(DOMAIN)
        self._abort_if_unique_id_configured()
        if user_input is not None:
            return self.async_create_entry(title="Norwegian Namedays", data={})
        return self.async_show_form(step_id="user")
