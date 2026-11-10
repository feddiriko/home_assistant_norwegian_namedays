# Norwegian Namedays

A Home Assistant integration that provides the Norwegian name day for today using a bundled, offline calendar. **It does not make any network requests to retrieve names.** The calendar is loaded locally and the sensor updates daily using Home Assistant's configured time zone.

## Installation

Install **Norwegian Namedays** through HACS by adding this repository as a custom integration repository. Restart Home Assistant, then add **Norwegian Namedays** from **Settings → Devices & services → Add integration**.

The integration creates:

- `sensor.namedays_today` — today's names.
- `sensor.namedays_comment` — the date's `Kommentar`, when available.

The calendar is bundled in `custom_components/norwegian_namedays/namedays.py`, based on the [Norwegian Wikipedia namedays list](https://no.wikipedia.org/wiki/Liste_over_norske_navnedager). Updating the calendar requires updating this local file; Home Assistant will not download updates automatically.
