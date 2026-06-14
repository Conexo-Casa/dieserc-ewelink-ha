"""
DieseRC 4CH eWeLink Relay — Home Assistant Integration.

This integration provides configuration scaffolding and setup validation
for the DieseRC 4-Channel WiFi Smart Switch relay module using the eWeLink
protocol via SonoffLAN (AlexxIT/SonoffLAN).

Device: DieseRC 4 Channels WiFi Smart Switch, DC 5V/12V/24V/36V
Protocol: eWeLink (CoolKit) — UIID 7 (4ch strip) or UIID 84
"""

from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

_LOGGER = logging.getLogger(__name__)

DOMAIN = "dieserc_4ch"

# Expected UIID values for this device family
SUPPORTED_UIIDS = [7, 84, 141]


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up the DieseRC 4CH integration."""
    _LOGGER.info(
        "DieseRC 4CH eWeLink Relay integration loaded. "
        "This integration requires SonoffLAN (AlexxIT/SonoffLAN) to be installed and "
        "configured with your eWeLink account. "
        "See https://github.com/Conexo-Casa/dieserc-ewelink-ha for setup instructions."
    )

    # Check if SonoffLAN (sonoff domain) is available
    sonoff_loaded = "sonoff" in hass.config.components
    if not sonoff_loaded:
        _LOGGER.warning(
            "SonoffLAN integration ('sonoff' domain) is not loaded. "
            "DieseRC 4CH relay control requires SonoffLAN. "
            "Install it via HACS: https://github.com/AlexxIT/SonoffLAN"
        )
    else:
        _LOGGER.info(
            "SonoffLAN detected. DieseRC 4CH relay should appear as switch entities. "
            "If channels are missing, add 'extra: { uiid: 7 }' to your sonoff device config."
        )

    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up from a config entry (not used — no config flow)."""
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    return True
