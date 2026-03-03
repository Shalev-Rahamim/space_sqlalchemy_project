from .repository import BaseRepository
from database.models import Mission, Astronaut
from database.connection import session_scope


class MissionRepository(BaseRepository):
    def __init__(self):
        super().__init__(Mission)

    def update(self, mission_id, new_title=None, new_dest=None):
        """Update mission details"""
        with session_scope() as session:
            mission = session.query(Mission).filter(Mission.id == mission_id).first()
            if not mission:
                return False

            if new_title:
                mission.title = new_title
            if new_dest:
                mission.destination = new_dest

            return True

    def assign_astronaut(self, mission_id, astronaut_id):
        """Add an astronaut to a mission (N:M relationship)"""
        with session_scope() as session:
            mission = session.query(Mission).filter(Mission.id == mission_id).first()
            astronaut = (
                session.query(Astronaut).filter(Astronaut.id == astronaut_id).first()
            )

            if mission and astronaut:
                mission.astronauts.append(astronaut)
                return True
            return False
