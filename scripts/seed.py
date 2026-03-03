# scripts/seed.py
import sys
import os
import random
from datetime import datetime
from faker import Faker
from database.connection import session_scope, engine, init_db
from database.models import Base, Agency, Spacecraft, BlackBox, Astronaut, Mission

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)


fake = Faker()


def seed_data():
    """Fill the database with real and fake data"""
    print("🗑️  Dropping old tables...")
    Base.metadata.drop_all(engine)
    print("🏗️  Creating new tables...")
    init_db()
    with session_scope() as session:
        print("🚀 Seeding Real Historical Data...")

        # --- Real Agencies ---
        nasa = Agency(name="NASA", country="USA")
        isa = Agency(name="ISA", country="Israel")
        roscosmos = Agency(name="Roscosmos", country="Russia")
        spacex = Agency(name="SpaceX", country="USA")

        session.add_all([nasa, isa, roscosmos, spacex])
        session.flush()

        # --- Real Spacecrafts ---
        apollo_cm = Spacecraft(model_name="Apollo Command Module", agency_id=nasa.id)
        apollo_cm.black_box = BlackBox(
            serial_number="AP-11-BBX", storage_capacity_gb=0.5
        )

        columbia = Spacecraft(model_name="Space Shuttle Columbia", agency_id=nasa.id)
        columbia.black_box = BlackBox(
            serial_number="STS-107-BBX", storage_capacity_gb=64.0
        )

        vostok = Spacecraft(model_name="Vostok 3KA", agency_id=roscosmos.id)
        vostok.black_box = BlackBox(serial_number="VK-1-BBX", storage_capacity_gb=0.1)

        dragon = Spacecraft(model_name="Crew Dragon Endeavour", agency_id=spacex.id)
        dragon.black_box = BlackBox(
            serial_number="CD-2020-BBX", storage_capacity_gb=2048.0
        )

        session.add_all([apollo_cm, columbia, vostok, dragon])

        # --- Real Astronauts ---
        neil = Astronaut(
            name="Neil Armstrong", rank="Commander", years_of_experience=15
        )
        buzz = Astronaut(name="Buzz Aldrin", rank="Pilot", years_of_experience=12)
        ilan = Astronaut(
            name="Ilan Ramon", rank="Payload Specialist", years_of_experience=8
        )
        yuri = Astronaut(name="Yuri Gagarin", rank="Pilot", years_of_experience=5)

        session.add_all([neil, buzz, ilan, yuri])

        # --- Real Missions ---
        apollo11 = Mission(
            title="Apollo 11", destination="Moon", launch_date=datetime(1969, 7, 16)
        )
        sts107 = Mission(
            title="STS-107",
            destination="Low Earth Orbit",
            launch_date=datetime(2003, 1, 16),
        )
        vostok1 = Mission(
            title="Vostok 1",
            destination="Low Earth Orbit",
            launch_date=datetime(1961, 4, 12),
        )

        session.add_all([apollo11, sts107, vostok1])
        session.flush()

        # --- Connect N:M ---
        apollo11.astronauts.extend([neil, buzz])
        sts107.astronauts.append(ilan)
        vostok1.astronauts.append(yuri)

        print("✨ Real data inserted!")

        # --- Fake Data Generation ---
        print("🤖 Generating fake data...")
        agencies_list = [nasa, isa, roscosmos, spacex]

        # Fake Spacecrafts
        for _ in range(10):
            sc = Spacecraft(
                model_name=f"{fake.word().capitalize()} Mark-{random.randint(1, 10)}",
                agency_id=random.choice(agencies_list).id,
            )
            sc.black_box = BlackBox(
                serial_number=f"SN-{fake.uuid4()[:8].upper()}",
                storage_capacity_gb=round(random.uniform(100.0, 5000.0), 2),
            )
            session.add(sc)

        # Fake Astronauts
        fake_astronauts = []
        ranks = ["Commander", "Pilot", "Engineer", "Specialist", "Officer"]
        for _ in range(20):
            astro = Astronaut(
                name=fake.name(),
                rank=random.choice(ranks),
                years_of_experience=random.randint(1, 20),
            )
            fake_astronauts.append(astro)
            session.add(astro)

        # Fake Missions
        destinations = ["Mars", "ISS", "Europa", "Titan", "Lunar Gateway"]
        for _ in range(10):
            mission = Mission(
                title=f"Operation {fake.word().capitalize()}",
                destination=random.choice(destinations),
                launch_date=fake.date_time_between(start_date="-5y", end_date="+2y"),
            )
            crew = random.sample(fake_astronauts, random.randint(2, 4))
            mission.astronauts.extend(crew)
            session.add(mission)

        print("✅ Database seeded successfully!")


if __name__ == "__main__":
    seed_data()
