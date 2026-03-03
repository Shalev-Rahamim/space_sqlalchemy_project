from database.connection import session_scope


class BaseRepository:
    """Base class for all CRUD operations to avoid code duplication"""

    def __init__(self, model):
        self.model = model

    def create(self, **kwargs):
        """Create and save a new record"""
        with session_scope() as session:
            new_obj = self.model(**kwargs)
            session.add(new_obj)
            session.flush()  # Get the ID before closing session
            return new_obj.to_dict()  # Return as dict for API/Frontend readiness

    def get_all(self):
        """Get all records from the table"""
        with session_scope() as session:
            records = session.query(self.model).all()
            return [record.to_dict() for record in records]

    def get_by_id(self, obj_id):
        """Get a single record by its ID"""
        with session_scope() as session:
            record = session.query(self.model).filter(self.model.id == obj_id).first()
            return record.to_dict() if record else None

    def delete(self, obj_id):
        """Delete a record by ID"""
        with session_scope() as session:
            record = session.query(self.model).filter(self.model.id == obj_id).first()
            if record:
                session.delete(record)
                return True
            return False
