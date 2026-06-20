# Besen BS20 Home Assistant Integration

Native Home Assistant integration for Besen BS20-family EV chargers over Bluetooth Low Energy.

This integration talks directly to the charger through Home Assistant's Bluetooth stack. It does not need MQTT, Docker, a sidecar process, or a Home Assistant add-on. It is designed to work through existing ESPHome Bluetooth proxies as long as those proxies support active GATT connections.

## Status

This is an early custom integration. It is written to follow Home Assistant's integration quality rules closely, with config flow setup, diagnostics, translations, reconnect handling, tests, and end-user documentation. It has not yet been submitted to Home Assistant Core.

## Requirements

- Home Assistant with the Bluetooth integration enabled.
- A Besen BS20 or compatible charger advertising as `ACP#...`.
- The charger BLE address and 6-digit PIN.
- For ESPHome Bluetooth proxies:
  - `bluetooth_proxy:` with active connections enabled.
  - A connectable proxy close enough to the charger.
  - Enough free active connection slots.

ESPHome Bluetooth proxies default to active connections enabled in current ESPHome releases. Each continuously connected charger uses one active GATT connection slot on the selected proxy.

## Installation

### HACS custom repository

1. Open HACS.
2. Add this repository as a custom integration repository.
3. Install **Besen BS20**.
4. Restart Home Assistant.
5. Go to **Settings > Devices & services**.
6. Add **Besen BS20** or accept the discovered `ACP#...` device.

### Manual installation

1. Copy `custom_components/besen_bs20` into your Home Assistant `custom_components` directory.
2. Restart Home Assistant.
3. Add **Besen BS20** from **Settings > Devices & services**.

## Setup Parameters

- **BLE address**: The charger Bluetooth address. Discovery fills this automatically when Home Assistant sees an `ACP#...` advertisement.
- **PIN**: The charger's 6-digit Bluetooth PIN. Many units default to `123456`.
- **Sync charger clock**: Keeps the charger's internal clock aligned during heartbeat responses.

The PIN can be updated later through the integration reconfigure flow.

## Entities

The exact entity set depends on charger model, board revision, reported phase count, and supported firmware responses.

Enabled by default:

- Charging switch.
- Charge amps number.
- Current power sensor.
- Total/session energy sensors.
- L1 voltage and current.
- Charger status, plug state, output state, current state, and error state.
- Charger temperature.
- Device name text entity.
- Temperature unit and language selectors.

Diagnostic or less commonly used entities may be disabled by default:

- RSSI.
- L2/L3 voltage and current on three-phase chargers.
- System time.
- LCD brightness.
- Integration/protocol version details.

## Controls And Actions

The integration does not register custom Home Assistant service actions. Use the standard entity actions instead:

- `switch.turn_on` / `switch.turn_off` on the charging switch.
- `number.set_value` on charge amps.
- `select.select_option` on language or temperature unit.
- `text.set_value` on the charger name.

Command failures are raised back to Home Assistant and the device is marked unavailable if the BLE write path fails.

## Updating Data

The charger sends status over BLE notifications after login. Home Assistant keeps one active BLE connection open, listens for notifications, and responds to charger heartbeats. If notifications stop for about 45 seconds, the integration reconnects without repeatedly filling the logs.

This is a local-push integration. There is no cloud dependency.

## Common Automations

Start charging when solar surplus is available:

```yaml
alias: Start EV charging on solar surplus
triggers:
  - trigger: numeric_state
    entity_id: sensor.solar_surplus_power
    above: 2500
    for: "00:05:00"
conditions:
  - condition: state
    entity_id: sensor.besen_bs20_plug_state
    state: Connected Locked
actions:
  - action: number.set_value
    target:
      entity_id: number.besen_bs20_charge_amps
    data:
      value: 8
  - action: switch.turn_on
    target:
      entity_id: switch.besen_bs20_charging
```

Stop charging before peak tariff:

```yaml
alias: Stop EV charging before peak tariff
triggers:
  - trigger: time
    at: "17:00:00"
actions:
  - action: switch.turn_off
    target:
      entity_id: switch.besen_bs20_charging
```

## Supported Devices

Known target:

- Besen BS20.

Likely compatible:

- Besen wallboxes using the same `ACP#` BLE protocol and one of the known UUID pairs.

Unsupported or not implemented:

- Wi-Fi provisioning.
- Password reset.
- Device reset.
- Charging history download.
- Firmware updates through Home Assistant.
- Safety-certified load balancing.

## Troubleshooting

### The charger is not discovered

- Confirm it appears in **Settings > Bluetooth > Advertisement monitor** as `ACP#...`.
- Move an ESPHome Bluetooth proxy closer to the charger.
- Make sure the proxy is added to Home Assistant through the ESPHome integration.
- Run an active scan or temporarily place a local Bluetooth adapter near the charger.

### Setup says no connectable Bluetooth path is available

The charger may be visible only through a passive/non-connectable adapter. Use an ESPHome Bluetooth proxy with active connections enabled, or a local Bluetooth adapter supported by Home Assistant.

### The charger becomes unavailable

- Check **Settings > Bluetooth > Connection monitor**.
- Verify the proxy has free active connection slots.
- Prefer Ethernet ESP32 Bluetooth proxies when possible.
- Avoid placing the proxy next to strong Wi-Fi or USB 3.0 interference sources.

### The PIN is rejected

Use the integration reauthentication prompt or reconfigure flow to enter the correct 6-digit PIN. The integration redacts PINs from diagnostics.

### Diagnostics

From the device page, download diagnostics before opening an issue. Diagnostics include the board revision, charger metadata, latest parsed state, availability, and last error. The PIN is redacted.

## Removal

1. Go to **Settings > Devices & services**.
2. Open **Besen BS20**.
3. Select the integration menu and choose **Delete**.
4. Restart Home Assistant if you also manually copied the integration files and want to remove them from `custom_components`.

## Safety Notes

This integration exposes charger controls but is not a safety controller. Do not rely on it as the only protection for electrical limits, overheating, grid constraints, or vehicle safety. Keep charger hardware, breaker sizing, wiring, and local electrical code protections correct independently of Home Assistant.

## Attribution

The Bluetooth protocol implementation is based on the MIT-licensed work in [slespersen/evseMQTT](https://github.com/slespersen/evseMQTT), with the MQTT/runtime portions replaced by native Home Assistant integration code.
