from .repository import BaseRepository
from database.models import Spacecraft, BlackBox
from database.connection import session_scope


class SpacecraftRepository(BaseRepository):
    def __init__(self):
        super().__init__(Spacecraft)

    def get_by_agency(self, agency_id):
        """Return all spacecrafts that belong to a given agency"""
        with session_scope() as session:
            spacecrafts = (
                session.query(Spacecraft)
                .filter(Spacecraft.agency_id == agency_id)
                .all()
            )
            return [sc.to_dict() for sc in spacecrafts]

    def update(self, spacecraft_id, new_model_name=None, new_agency_id=None):
        """Update spacecraft details"""
        with session_scope() as session:
            sc = (
                session.query(Spacecraft).filter(Spacecraft.id == spacecraft_id).first()
            )
            if not sc:
                return False

            if new_model_name:
                sc.model_name = new_model_name
            if new_agency_id:
                sc.agency_id = new_agency_id

            return True

    def assign_black_box(self, spacecraft_id, serial_number, storage_gb):
        """Create and link a black box to a spacecraft (1:1 relationship)"""
        with session_scope() as session:
            sc = (
                session.query(Spacecraft).filter(Spacecraft.id == spacecraft_id).first()
            )
            if sc:
                new_box = BlackBox(
                    serial_number=serial_number, storage_capacity_gb=storage_gb
                )
                sc.black_box = new_box
                return True
            return False
