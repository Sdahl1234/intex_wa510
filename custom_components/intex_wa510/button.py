from __future__ import annotations

from dataclasses import dataclass
import logging

from homeassistant.components.button import ButtonEntity
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, DEVICE_NAME, DEVICE_MANUFACTURER, DEVICE_MODEL, DEVICE_SW_VERSION

_LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True)
class ButtonDef:
    key: str
    name: str
    suggested_object_id: str
    icon: str
    action_type: str
    method_name: str | None = None
    maintenance_key: str | None = None
    entity_category: EntityCategory | None = None


BUTTONS = [
    ButtonDef("refresh_measurement", "Actualiser mesure", "piscine_actualiser_mesure", "mdi:refresh", "refresh"),
    ButtonDef("cleaning_done", "Entretien - Nettoyage effectué", "piscine_nettoyage_wa510_effectue", "mdi:spray-bottle", "maintenance", maintenance_key="last_cleaning", entity_category=EntityCategory.CONFIG),
    ButtonDef("ph_calibration_done", "Calibration - pH effectuée", "piscine_calibration_ph_effectuee", "mdi:flask-check", "maintenance", maintenance_key="last_ph_calibration", entity_category=EntityCategory.CONFIG),
    ButtonDef("orp_calibration_done", "Calibration - ORP effectuée", "piscine_calibration_orp_effectuee", "mdi:flask-check-outline", "maintenance", maintenance_key="last_orp_calibration", entity_category=EntityCategory.CONFIG),
    ButtonDef("ph_cal_start", "Calibration - Démarrer pH", "piscine_demarrer_calibration_ph", "mdi:flask-outline", "tuya", "start_ph_calibration", entity_category=EntityCategory.DIAGNOSTIC),
    ButtonDef("ph_cal_4", "Calibration - Valider pH 4.00", "piscine_valider_ph_4", "mdi:numeric-4-circle-outline", "tuya", "validate_ph_4_calibration", entity_category=EntityCategory.DIAGNOSTIC),
    ButtonDef("ph_cal_9", "Calibration - Valider pH 9.00", "piscine_valider_ph_9", "mdi:numeric-9-circle-outline", "tuya", "validate_ph_9_calibration", entity_category=EntityCategory.DIAGNOSTIC),
    ButtonDef("orp_cal_start", "Calibration - Démarrer ORP", "piscine_demarrer_calibration_orp", "mdi:lightning-bolt-outline", "tuya", "start_orp_calibration", entity_category=EntityCategory.DIAGNOSTIC),
    ButtonDef("orp_cal_256", "Calibration - Valider ORP 256 mV", "piscine_valider_orp_256", "mdi:lightning-bolt-circle", "tuya", "validate_orp_256_calibration", entity_category=EntityCategory.DIAGNOSTIC),
]


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([IntexWA510Button(coordinator, entry, desc) for desc in BUTTONS], True)


class IntexWA510Button(CoordinatorEntity, ButtonEntity):
    def __init__(self, coordinator, entry, desc: ButtonDef):
        super().__init__(coordinator)
        self.desc = desc
        self._attr_unique_id = f"{entry.entry_id}_{desc.key}"
        self._attr_name = desc.name
        self._attr_has_entity_name = True
        self._attr_suggested_object_id = desc.suggested_object_id
        self._attr_icon = desc.icon
        self._attr_entity_category = desc.entity_category
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.data["device_id"])},
            "name": DEVICE_NAME,
            "manufacturer": DEVICE_MANUFACTURER,
            "model": DEVICE_MODEL,
            "sw_version": DEVICE_SW_VERSION,
        }

    async def async_press(self) -> None:
        _LOGGER.info("WA510 BUTTON PRESSED: %s", self.desc.name)

        try:
            if self.desc.action_type == "maintenance":
                await self.coordinator.async_mark_maintenance_done(self.desc.maintenance_key)
                return

            if self.desc.action_type == "refresh":
                await self.coordinator.async_refresh_measurement_and_update()
                return

            method = getattr(self.coordinator.client, self.desc.method_name)
            result = await method()
            _LOGGER.info("WA510 BUTTON RESULT: %s / result=%s", self.desc.name, result)
            await self.coordinator.async_request_refresh()

        except Exception as err:
            _LOGGER.exception("WA510 BUTTON ERROR: %s / error=%s", self.desc.name, err)
