<p align="center">
  <img src="https://raw.githubusercontent.com/Yeoh37/intex_wa510/main/logo.png" alt="Intex WA510 Water Analyzer" width="220">
</p>

# Intex WA510 Water Analyzer

Home Assistant custom integration for the **Intex WA510 / AGP SMART SENSOR T3U** via Tuya Cloud.

---

## Features

### Water monitoring

- pH
- ORP
- Water temperature
- Free chlorine
- Corrected free chlorine
- Battery level
- Error code monitoring

### Controls

- Force measurement refresh
- pH setpoint control
- ORP setpoint control

### Maintenance tracking

- Last cleaning date
- Days since cleaning
- Cleaning reminder
- Configurable cleaning interval
- Cleaning completed button

### Calibration tracking

- Last pH calibration date
- Last ORP calibration date
- Days since pH / ORP calibration
- Calibration reminders
- Configurable calibration intervals
- Calibration completed buttons

### Device presentation

- Device name: **Analyseur Piscine**
- Manufacturer: **Intex / AGP / Tuya**
- Model: **WA510 / AGP SMART SENSOR T3U**
- Logo and icon files included in the repository and integration folder

> Note: Home Assistant may still show `icon not available` for custom integrations unless the integration is included in the official Home Assistant Brands repository. This does not affect the integration.

---

## Installation via HACS

1. Open HACS
2. Add this repository as a custom repository
3. Category: **Integration**
4. Install the integration
5. Restart Home Assistant
6. Add the integration from **Settings → Devices & Services**

Repository:

```text
https://github.com/Yeoh37/intex_wa510
```

---

## Configuration

You need Tuya IoT Platform credentials:

- Access ID / Client ID
- Access Secret / Client Secret
- Device ID

The WA510 device must already be linked to your Tuya / Intex account.

For Europe, the default endpoint is:

```text
https://openapi.tuyaeu.com
```

---

## Changelog

### v0.6.1

Presentation release:
- device is now named **Analyseur Piscine**
- device information uses a consistent manufacturer/model/software version
- logo.png and icon.png are included at repository root and inside the integration folder
- README keeps the HACS-compatible raw GitHub logo URL
- manifest version set to 0.6.1

### v0.6.0

Clean public release:
- clean GitHub / HACS package structure
- manifest version set to 0.6.0
- maintenance and calibration entities kept from v0.5.x
- duplicated unavailable setpoint / threshold sensors removed
