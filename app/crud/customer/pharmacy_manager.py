from math import radians, sin, cos, sqrt, atan2
from ...db.base.database_manager import DatabaseManager
from ...models.customer.pharmacy_model import Pharmacy
from ...schemas.customer.pharmacy_schema import PharmacyCreate, PharmacyUpdate
from ...utils.logger import get_logger

logger = get_logger(__name__)

class PharmacyManager:
    def __init__(self, db_type: str):
        self.db_manager = DatabaseManager(db_type)

    # Haversine formula to calculate distance in km
    def _calculate_distance_km(self, lat1, lon1, lat2, lon2):
        R = 6371
        dlat = radians(lat2 - lat1)
        dlon = radians(lon2 - lon1)
        a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        return R * c

    # --------------------------
    # CRUD
    # --------------------------
    async def create_pharmacy(self, pharmacy: PharmacyCreate):
        try:
            await self.db_manager.connect()
            await self.db_manager.create(Pharmacy, pharmacy.dict())
            logger.info(f"✅ Pharmacy created: {pharmacy.Name}")
            return {"success": True, "message": "Pharmacy created successfully"}
        except Exception as e:
            logger.error(f"❌ Error creating pharmacy: {e}")
            return {"success": False, "message": str(e)}
        finally:
            await self.db_manager.disconnect()

    async def get_pharmacies(self):
        try:
            await self.db_manager.connect()
            return await self.db_manager.read(Pharmacy, {})
        except Exception as e:
            logger.error(f"❌ Error fetching pharmacies: {e}")
            return {"success": False, "message": str(e)}
        finally:
            await self.db_manager.disconnect()

    async def update_pharmacy(self, pharmacy_id: int, pharmacy: PharmacyUpdate):
        try:
            await self.db_manager.connect()
            rowcount = await self.db_manager.update(
                Pharmacy, {"PharmacyId": pharmacy_id}, pharmacy.dict(exclude_unset=True)
            )
            if rowcount:
                logger.info(f"✅ Pharmacy {pharmacy_id} updated")
                return {"success": True, "message": "Pharmacy updated successfully"}
            return {"success": False, "message": "Pharmacy not found"}
        except Exception as e:
            logger.error(f"❌ Error updating pharmacy: {e}")
            return {"success": False, "message": str(e)}
        finally:
            await self.db_manager.disconnect()

    async def delete_pharmacy(self, pharmacy_id: int):
        try:
            await self.db_manager.connect()
            rowcount = await self.db_manager.delete(Pharmacy, {"PharmacyId": pharmacy_id})
            if rowcount:
                logger.info(f"🗑️ Pharmacy {pharmacy_id} deleted")
                return {"success": True, "message": "Pharmacy deleted successfully"}
            return {"success": False, "message": "Pharmacy not found"}
        except Exception as e:
            logger.error(f"❌ Error deleting pharmacy: {e}")
            return {"success": False, "message": str(e)}
        finally:
            await self.db_manager.disconnect()

    # --------------------------
    # Nearby by GPS
    # --------------------------
    async def get_nearby_by_gps(self, latitude: float, longitude: float, radius_km: float = 5):
        try:
            await self.db_manager.connect()
            pharmacies = await self.db_manager.read(Pharmacy, {})
            nearby = []

            for p in pharmacies:
                if not p.GPSLocation:
                    continue
                lat_str, lon_str = p.GPSLocation.split(" ")
                distance = self._calculate_distance_km(latitude, longitude, float(lat_str), float(lon_str))
                if distance <= radius_km:
                    nearby.append({
                        "PharmacyId": p.PharmacyId,
                        "Name": p.Name,
                        "Address": p.Address,
                        "GPSLocation": p.GPSLocation,
                        "Pincode": p.Pincode,
                        "ImgUrl": p.ImgUrl,
                        "Contact": p.Contact,
                        "Email": p.Email,
                        "DistanceKm": round(distance, 2)
                    })

            nearby.sort(key=lambda x: x["DistanceKm"])
            return nearby
        except Exception as e:
            logger.error(f"❌ Error fetching nearby pharmacies by GPS: {e}")
            return {"success": False, "message": str(e)}
        finally:
            await self.db_manager.disconnect()

    # --------------------------
    # Nearby by Pincode
    # --------------------------
    async def get_nearby_by_pincode(self, pincode: str):
        try:
            await self.db_manager.connect()
            pharmacies = await self.db_manager.read(Pharmacy, {"Pincode": pincode})
            result = []
            for p in pharmacies:
                result.append({
                    "PharmacyId": p.PharmacyId,
                    "Name": p.Name,
                    "Address": p.Address,
                    "GPSLocation": p.GPSLocation,
                    "Pincode": p.Pincode,
                    "ImgUrl": p.ImgUrl,
                    "Contact": p.Contact,
                    "Email": p.Email
                })
            return result
        except Exception as e:
            logger.error(f"❌ Error fetching nearby pharmacies by Pincode: {e}")
            return {"success": False, "message": str(e)}
        finally:
            await self.db_manager.disconnect()
