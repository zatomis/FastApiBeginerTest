from src.schemas.facilities import FaclitiesAdd
from src.services.base import BaseServiceLayer
from src.tasks.task import test_task


class FacilityServiceLayer(BaseServiceLayer):
    async def create_facility(self, data: FaclitiesAdd):
        facility = await self.db.facilities.add(data)
        await self.db.commit()
        test_task.delay()  # type: ignore
        return facility


    async def get_facilities(self):
        return await self.db.facilities.get_all()