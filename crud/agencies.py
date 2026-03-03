from .repository import BaseRepository
from database.models import Agency
from database.connection import session_scope


class AgencyRepository(BaseRepository):
    def __init__(self):
        super().__init__(Agency)

    def update(self, agency_id, new_name=None, new_country=None):
        """Update agency details"""
        with session_scope() as session:
            agency = session.query(Agency).filter(Agency.id == agency_id).first()
            if not agency:
                return False

            if new_name:
                agency.name = new_name
            if new_country:
                agency.country = new_country

            return True
