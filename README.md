# Norwegian Namedays

A Home Assistant integration that shows today's Norwegian nameday from a bundled offline calendar. It does not call any external service when reporting the current name day.

## Installation

This repository is intended for Home Assistant's Marketplace. In Home Assistant:

1. Open Settings → Marketplace.
2. Select Add from link.
3. Enter this GitHub repository URL:
   `https://github.com/feddiriko/home_assistant_norwegian_namedays`
4. Install the repository and then add the integration under Settings → Devices & services.

## Entities

After setup, the integration creates these entities:

- `sensor.norwegian_namedays_today` — today's names
- `sensor.norwegian_namedays_comment` — a comment for the date when available

The calendar is bundled in `custom_components/norwegian_namedays/namedays.py` and based on the Norwegian Wikipedia namedays list. The integration updates at midnight using Home Assistant's configured timezone.

## Notes

- This integration is fully local and does not retrieve nameday data from the internet.
- The data source is bundled in the repository and can be updated by editing the local calendar file.
