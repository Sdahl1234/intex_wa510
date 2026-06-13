<p align="center">
  <img src="https://raw.githubusercontent.com/Yeoh37/intex_wa510/main/logo.png" alt="Intex WA510 Water Analyzer" width="220">
</p>

# Intex WA510 Water Analyzer

Home Assistant custom integration for the **Intex WA510 / AGP SMART SENSOR T3U** via Tuya Cloud.

---

## Features

### Water Monitoring

- pH sensor
- ORP sensor
- Water temperature
- Free chlorine
- Corrected free chlorine
- Battery level
- Error code monitoring

### Controls

- Force measurement refresh
- ORP setpoint control
- pH setpoint control

### Maintenance Tracking

- Last cleaning date
- Days since cleaning
- Cleaning reminder
- Configurable cleaning interval

### Calibration Tracking

- Last pH calibration date
- Last ORP calibration date
- Days since calibration
- Calibration reminders
- Configurable calibration intervals

### Diagnostics

- Last real measurement timestamp
- Maintenance status
- Sensor indicators
- Calibration status

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

You will need Tuya IoT Platform credentials:

- Access ID
- Access Secret
- Device ID

The device must already be linked to your Tuya / Intex account.

For Europe, the default endpoint is:

```text
https://openapi.tuyaeu.com
```

---

## Supported Device

### Intex WA510

Also sold as:

- AGP SMART SENSOR T3U

---

## Entities

### Sensors

- pH
- ORP
- Water temperature
- Free chlorine
- Corrected free chlorine
- Battery level
- Last measurement timestamp

### Binary Sensors

- Calibration required
- Cleaning required
- Maintenance required
- Low battery

### Numbers

- pH setpoint
- ORP setpoint
- Cleaning interval
- pH calibration interval
- ORP calibration interval

### Buttons

- Refresh measurement
- Cleaning completed
- pH calibration completed
- ORP calibration completed

---

## Important Notes

The calibration command buttons exposed by Tuya are experimental.

Do not launch a calibration unless you are actually performing the official calibration procedure described in the Intex documentation.

This project is experimental and is not affiliated with Intex, AGP, Tuya, or Home Assistant.

---

## Changelog

### v0.5.2

- Fixed README logo URL for HACS using a GitHub raw image URL
- Updated manifest version to 0.5.2
- Kept local `logo.png` and `icon.png` at repository root and integration folder
- Kept v0.5.1 cleanup:
  - removed duplicate unavailable sensor entities for pH/ORP setpoints and maintenance thresholds
  - clearer labels for calibration and maintenance items
  - translated Tuya `off` indicator status to `Normal` / `Aucune`
  - cleaner Configuration and Diagnostic sections
