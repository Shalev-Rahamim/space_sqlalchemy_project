from sqlalchemy import func
from database.connection import session_scope
from database.models import Agency, Spacecraft, Astronaut, Mission, BlackBox


class SpaceAnalyticsService:
    """Business logic for space data analysis"""

    @staticmethod
    def get_agency_storage_capacity():
        """1. Total black box storage capacity per agency (JOIN + SUM + GROUP BY)"""
        with session_scope() as session:
            results = (
                session.query(
                    Agency.name,
                    func.sum(BlackBox.storage_capacity_gb).label("total_storage"),
                )
                .select_from(Agency)
                .join(Spacecraft, Agency.id == Spacecraft.agency_id)
                .join(BlackBox, Spacecraft.id == BlackBox.spacecraft_id)
                .group_by(Agency.name)
                .all()
            )

            return [
                {
                    "agency": row.name,
                    "total_storage_gb": round(row.total_storage or 0, 2),
                }
                for row in results
            ]

    @staticmethod
    def get_astronauts_mission_count():
        """2. Ranking astronauts by number of missions (JOIN + COUNT + ORDER BY)"""
        with session_scope() as session:
            results = (
                session.query(
                    Astronaut.name, func.count(Mission.id).label("mission_count")
                )
                .join(Astronaut.missions)
                .group_by(Astronaut.id)
                .order_by(func.count(Mission.id).desc())
                .all()
            )

            return [
                {"astronaut": row.name, "missions": row.mission_count}
                for row in results
            ]

    @staticmethod
    def get_fleet_statistics():
        """3. Number of spacecrafts per agency (OUTER JOIN for zero-fleet agencies)"""
        with session_scope() as session:
            results = (
                session.query(Agency.name, func.count(Spacecraft.id).label("count"))
                .outerjoin(Spacecraft)
                .group_by(Agency.name)
                .all()
            )

            return [
                {"agency": row.name, "spacecraft_count": row.count} for row in results
            ]

    @staticmethod
    def get_mission_complexity_report():
        """4. Average crew experience per mission (JOIN + AVG)"""
        with session_scope() as session:
            results = (
                session.query(
                    Mission.title,
                    func.avg(Astronaut.years_of_experience).label("avg_exp"),
                )
                .join(Mission.astronauts)
                .group_by(Mission.id)
                .all()
            )

            return [
                {"mission": row.title, "avg_experience": round(row.avg_exp, 1)}
                for row in results
            ]

    @staticmethod
    def get_top_destinations():
        """5. Most popular destinations by number of missions (COUNT + GROUP BY)"""
        with session_scope() as session:
            results = (
                session.query(
                    Mission.destination, func.count(Mission.id).label("visit_count")
                )
                .group_by(Mission.destination)
                .order_by(func.count(Mission.id).desc())
                .all()
            )

            return [
                {"destination": row.destination, "visits": row.visit_count}
                for row in results
            ]
