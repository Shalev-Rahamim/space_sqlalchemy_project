from crud import MissionRepository
from utils import get_non_empty_input, get_valid_date, get_valid_int, get_optional_input
from utils.logger import log_action

mission_repo = MissionRepository()


def manage_missions():
    while True:
        print("\n--- 🚀 Mission Management ---")
        print("1. View all Missions")
        print("2. Create new Mission")
        print("3. Assign Astronaut to Mission (N:M)")
        print("4. Update Mission")
        print("5. Delete Mission")
        print("0. Back")

        choice = input("Select: ")

        if choice == "1":
            missions = mission_repo.get_all()
            for m in missions:
                launch_date = m.get("launch_date", "N/A")
                print(
                    f"ID: {m['id']} | Title: {m['title']} | Dest: {m['destination']} | Date: {launch_date}"
                )

        elif choice == "2":
            print("\n🆕 New Mission Details:")
            title = get_non_empty_input("Mission Title: ")
            dest = get_non_empty_input("Destination: ")
            launch_date = get_valid_date("Launch Date (YYYY-MM-DD) [Enter for Today]: ")

            mission_repo.create(title=title, destination=dest, launch_date=launch_date)
            log_action(f"CREATED Mission: '{title}' to {dest}, Date: {launch_date}")
            print("✅ Mission created!")

        elif choice == "3":
            m_id = get_valid_int("Mission ID: ")
            a_id = get_valid_int("Astronaut ID: ")

            if mission_repo.assign_astronaut(m_id, a_id):
                log_action(f"ASSIGNED Astronaut ID {a_id} to Mission ID {m_id}")
                print("✅ Astronaut assigned to mission successfully!")
            else:
                print("❌ Failed: Mission or Astronaut ID not found.")

        elif choice == "4":
            m_id = get_valid_int("Enter Mission ID to update: ")
            print("Leave fields blank to keep current values.")

            new_title = get_optional_input("New Title: ")
            new_dest = get_optional_input("New Destination: ")

            if mission_repo.update(m_id, new_title=new_title, new_dest=new_dest):
                log_action(
                    f"UPDATED Mission ID {m_id}. New Title: {new_title}, New Dest: {new_dest}"
                )
                print("✅ Mission updated successfully!")
            else:
                print("❌ Mission ID not found.")

        elif choice == "5":
            m_id = get_valid_int("Enter Mission ID to delete: ")
            if mission_repo.delete(m_id):
                log_action(f"DELETED Mission ID {m_id}")
                print("✅ Mission deleted!")
            else:
                print("❌ Mission ID not found.")

        elif choice == "0":
            break
        else:
            print("❌ Invalid choice.")
