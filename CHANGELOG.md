# Changelog

All notable changes to this project will be documented in this file.

This project follows semantic versioning where practical. Tags use a `v` prefix, for example `v0.1.0`.

## [0.1.0] - 2026-06-20

### Added

- Initial native Home Assistant custom integration for Besen BS20 chargers.
- BLE protocol client based on the MIT-licensed `slespersen/evseMQTT` project.
- Home Assistant config flow with Bluetooth discovery, manual setup, reauthentication, and reconfiguration.
- Sensor, switch, number, select, and text platforms.
- Diagnostics and repair issue helpers.
- HACS metadata and local Home Assistant brand assets.
- CI for linting and tests.

### Known Limitations

- Hardware validation with a real Besen BS20 over ESPHome Bluetooth proxy is still required.
- Test coverage is currently protocol-focused; broader fake-BLE and Home Assistant config-flow coverage is planned.
- Firmware updates, charging history, Wi-Fi setup, device reset, and password reset are not implemented.

