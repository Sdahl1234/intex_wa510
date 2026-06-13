from __future__ import annotations

from dataclasses import dataclass

from homeassistant.components.sensor import SensorEntity, SensorDeviceClass, SensorStateClass
from homeassistant.const import UnitOfTemperature, PERCENTAGE
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, DEVICE_NAME, DEVICE_MANUFACTURER, DEVICE_MODEL, DEVICE_SW_VERSION


@dataclass(frozen=True)
class SensorDef:
    key: str
    name: str
    suggested_object_id: str
    unit: str | None = None
    device_class: SensorDeviceClass | None = None
    state_class: SensorStateClass | None = SensorStateClass.MEASUREMENT
    icon: str | None = None
    entity_category: EntityCategory | None = None


SENSORS = [
    SensorDef("temperature_c", "Température eau", "piscine_temperature", UnitOfTemperature.CELSIUS, SensorDeviceClass.TEMPERATURE, SensorStateClass.MEASUREMENT, "mdi:water-thermometer"),
    SensorDef("ph", "pH", "piscine_ph", None, None, SensorStateClass.MEASUREMENT, "mdi:ph"),
    SensorDef("orp", "ORP", "piscine_orp", "mV", None, SensorStateClass.MEASUREMENT, "mdi:lightning-bolt"),
    SensorDef("free_chlorine", "Chlore libre", "piscine_chlore", "ppm", None, SensorStateClass.MEASUREMENT, "mdi:test-tube"),
    SensorDef("free_chlorine_chemical", "Chlore libre corrigé", "piscine_chlore_corrige", "ppm", None, SensorStateClass.MEASUREMENT, "mdi:test-tube"),
    SensorDef("battery", "Batterie", "piscine_batterie", PERCENTAGE, SensorDeviceClass.BATTERY, SensorStateClass.MEASUREMENT, "mdi:battery"),

    SensorDef("ph_indicator", "Indicateur pH", "piscine_indicateur_ph", None, None, None, "mdi:ph", EntityCategory.DIAGNOSTIC),
    SensorDef("orp_indicator", "Indicateur ORP", "piscine_indicateur_orp", None, None, None, "mdi:lightning-bolt", EntityCategory.DIAGNOSTIC),
    SensorDef("fc_indicator", "Indicateur chlore", "piscine_indicateur_chlore", None, None, None, "mdi:test-tube", EntityCategory.DIAGNOSTIC),
    SensorDef("maintenance_indicator", "Maintenance appareil", "piscine_maintenance", None, None, None, "mdi:wrench-clock", EntityCategory.DIAGNOSTIC),
    SensorDef("error_code", "Code erreur", "piscine_code_erreur", None, None, None, "mdi:alert-circle-outline", EntityCategory.DIAGNOSTIC),
    SensorDef("ph_caliberate", "Calibration - État pH", "piscine_calibration_ph", None, None, None, "mdi:flask", EntityCategory.DIAGNOSTIC),
    SensorDef("orp_caliberate", "Calibration - État ORP", "piscine_calibration_orp", None, None, None, "mdi:flask", EntityCategory.DIAGNOSTIC),
    SensorDef("last_cleaning", "Entretien - Dernier nettoyage", "piscine_dernier_nettoyage_wa510", None, None, None, "mdi:spray-bottle", EntityCategory.DIAGNOSTIC),
    SensorDef("last_ph_calibration", "Calibration - Dernière pH", "piscine_derniere_calibration_ph", None, None, None, "mdi:flask", EntityCategory.DIAGNOSTIC),
    SensorDef("last_orp_calibration", "Calibration - Dernière ORP", "piscine_derniere_calibration_orp", None, None, None, "mdi:flask", EntityCategory.DIAGNOSTIC),
    SensorDef("days_since_cleaning", "Entretien - Jours depuis nettoyage", "piscine_jours_depuis_nettoyage", "j", None, SensorStateClass.MEASUREMENT, "mdi:calendar-clock", EntityCategory.DIAGNOSTIC),
    SensorDef("days_since_ph_calibration", "Calibration - Jours depuis pH", "piscine_jours_depuis_calibration_ph", "j", None, SensorStateClass.MEASUREMENT, "mdi:calendar-clock", EntityCategory.DIAGNOSTIC),
    SensorDef("days_since_orp_calibration", "Calibration - Jours depuis ORP", "piscine_jours_depuis_calibration_orp", "j", None, SensorStateClass.MEASUREMENT, "mdi:calendar-clock", EntityCategory.DIAGNOSTIC),
    SensorDef("last_measurement", "Dernière mesure WA510", "piscine_derniere_mesure_wa510", None, None, None, "mdi:clock-check-outline", EntityCategory.DIAGNOSTIC),
]


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([IntexWA510Sensor(coordinator, entry, desc) for desc in SENSORS], True)


class IntexWA510Sensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, entry, desc: SensorDef):
        super().__init__(coordinator)
        self.desc = desc
        self._attr_unique_id = f"{entry.entry_id}_{desc.key}"
        self._attr_name = desc.name
        self._attr_has_entity_name = True
        self._attr_suggested_object_id = desc.suggested_object_id
        self._attr_native_unit_of_measurement = desc.unit
        self._attr_device_class = desc.device_class
        self._attr_state_class = desc.state_class
        self._attr_icon = desc.icon
        self._attr_entity_category = desc.entity_category
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.data["device_id"])},
            "name": DEVICE_NAME,
            "manufacturer": DEVICE_MANUFACTURER,
            "model": DEVICE_MODEL,
            "sw_version": DEVICE_SW_VERSION,
        }

    @property
    def native_value(self):
        if not self.coordinator.data:
            return None
        return self.coordinator.data.get(self.desc.key)
