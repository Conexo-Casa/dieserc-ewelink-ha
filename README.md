# DieseRC 4-Channel eWeLink Relay — Home Assistant Integration

Control your DieseRC 4-Channel WiFi Smart Switch (DC 5V–36V passive dry-contact relay) from
Home Assistant using the [SonoffLAN](https://github.com/AlexxIT/SonoffLAN) custom integration
via HACS.

> **No firmware flashing required.** Works with the original eWeLink firmware over your local
> network (LAN) and/or the eWeLink cloud.

---

## Device Details

| Property | Value |
|---|---|
| Brand | DieseRC |
| Channels | 4 independent dry-contact relays |
| Input voltage | DC 5V / 12V / 24V / 36V |
| App | eWeLink |
| Protocol | eWeLink (CoolKit) |
| Likely UIID | **7** (4ch strip) or **84** (4ch) |
| Modes | Inching (momentary) / Self-locking (toggle) |

---

## Prerequisites

- Home Assistant 2023.6 or newer
- [HACS](https://hacs.xyz/) installed
- An active **eWeLink account** with the DieseRC device already paired
- The device and HA on the **same 2.4 GHz Wi-Fi network**

---

## Step 1 — Install SonoffLAN via HACS

1. Open Home Assistant → **HACS** → **Integrations**
2. Click **⋮ → Custom repositories**
3. Add `AlexxIT/SonoffLAN` with category **Integration** (skip if it already appears in search)
4. Search for **Sonoff** and click **Download**
5. **Restart Home Assistant**

Or click the badge below if your HA instance is reachable:

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=AlexxIT&repository=SonoffLAN&category=Integration)

---

## Step 2 — Add the Integration

1. Go to **Settings → Devices & Services → Add Integration**
2. Search for **Sonoff**
3. Enter your **eWeLink email and password**
4. Set **Mode** to `auto` (uses LAN when available, falls back to cloud)
5. Click **Submit**

HA will pull your device list from eWeLink and save it locally. Your 4-channel relay should
appear as four switch entities.

---

## Step 3 — Configure `configuration.yaml`

Add the following to your `configuration.yaml` to label each channel correctly and ensure
proper device class assignment.

```yaml
sonoff:
  devices:
    # Replace YOUR_DEVICE_ID with the 10-character ID shown in the eWeLink app
    # (tap the device → top-right ⋮ → Device Info → Device ID)
    YOUR_DEVICE_ID:
      name: "DieseRC 4CH Relay"
      device_class:
        - switch: 1   # Channel 1 — rename as needed (e.g. "Relay 1")
        - switch: 2   # Channel 2
        - switch: 3   # Channel 3
        - switch: 4   # Channel 4
```

### Rename channels to match your load

```yaml
sonoff:
  devices:
    YOUR_DEVICE_ID:
      name: "DieseRC 4CH Relay"
      device_class:
        - switch: 1   # e.g. Gate
        - switch: 2   # e.g. Garden Lights
        - switch: 3   # e.g. Pump
        - switch: 4   # e.g. Spare
```

After saving, go to **Settings → Devices & Services → Sonoff** and rename each entity
from the UI to whatever label matches your wiring.

---

## Step 4 — If the Device Is Not Detected (UIID Override)

Some DieseRC units register as an unrecognized UIID. If your relay appears as a single switch
or shows incorrect channel count, add the `extra` override to force the correct protocol:

```yaml
sonoff:
  devices:
    YOUR_DEVICE_ID:
      name: "DieseRC 4CH Relay"
      extra: { uiid: 7 }       # Try 7 first (4ch strip). If wrong, try 84.
      device_class:
        - switch: 1
        - switch: 2
        - switch: 3
        - switch: 4
```

**How to find your actual UIID:**

1. In HA go to **Settings → Devices & Services → Sonoff → ⋮ → Download diagnostics**
2. Open the JSON file and look for `"uiid"` inside your device entry
3. Use that value in the `extra` override if needed

---

## Step 5 — Inching (Momentary) Mode

If you need a channel to pulse briefly (e.g. a gate trigger), configure inching mode in the
**eWeLink app** per channel, then automate it in HA:

```yaml
# Example automation: pulse Channel 1 for gate release
automation:
  - alias: "Gate pulse"
    trigger:
      - platform: state
        entity_id: input_button.gate_trigger
    action:
      - service: switch.turn_on
        target:
          entity_id: switch.dieserc_4ch_relay_1
      - delay: "00:00:01"
      - service: switch.turn_off
        target:
          entity_id: switch.dieserc_4ch_relay_1
```

Or use the inching duration set in the eWeLink app — HA just sends `turn_on` and the device
handles the auto-off timing itself.

---

## Entity Names

After setup, your entities will follow this pattern:

| Entity ID | Default Name |
|---|---|
| `switch.dieserc_4ch_relay_1` | DieseRC 4CH Relay 1 |
| `switch.dieserc_4ch_relay_2` | DieseRC 4CH Relay 2 |
| `switch.dieserc_4ch_relay_3` | DieseRC 4CH Relay 3 |
| `switch.dieserc_4ch_relay_4` | DieseRC 4CH Relay 4 |

You can rename these under **Settings → Devices → [your device] → pencil icon**.

---

## Troubleshooting

| Symptom | Fix |
|---|---|
| Device shows as 1 switch instead of 4 | Add `extra: { uiid: 7 }` in `configuration.yaml` |
| Device shows offline | Check it's on 2.4 GHz Wi-Fi (not 5 GHz) |
| LAN control not working | Ensure HA and device are on the same subnet with mDNS/multicast enabled |
| Channels out of order | Re-number `device_class` entries to match your physical wiring |
| State not updating | Enable `mode: cloud` temporarily to verify cloud connectivity |

For detailed debug logs: **Settings → Devices & Services → Sonoff → Configure → Enable debug page**

---

## References

- [SonoffLAN by AlexxIT](https://github.com/AlexxIT/SonoffLAN) — the integration powering this setup
- [SonoffLAN DEVICES list](https://github.com/AlexxIT/SonoffLAN/blob/master/DEVICES.md) — UIID reference
- [eWeLink UIID Protocol](https://github.com/CoolKit-Technologies/eWeLink-API/blob/main/en/UIIDProtocol.md)
- [HACS Installation](https://hacs.xyz/docs/use/download/download/)

---

## License

Apache 2.0 — see [LICENSE](LICENSE)
