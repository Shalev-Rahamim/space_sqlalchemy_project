from .repository import BaseRepository
from database.models import Astronaut
from database.connection import session_scope


class AstronautRepository(BaseRepository):
    def __init__(self):
        super().__init__(Astronaut)

    def update(self, astro_id, new_name=None, new_rank=None):
        """Update astronaut details (at least 2 fields supported)"""
        with session_scope() as session:
            astro = session.query(Astronaut).filter(Astronaut.id == astro_id).first()
            if not astro:
                return False

            # Update only provided fields
            if new_name:
                astro.name = new_name
            if new_rank:
                astro.rank = new_rank

            return True
