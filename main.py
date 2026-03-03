import sys
from menus import (
    manage_astronauts,
    manage_missions,
    view_agencies,
    view_analytics,
    run_admin_seed,
)
from scripts.seed import seed_data


def run_main_menu():
    while True:
        print("\n" + "=" * 45)
        print("🚀 GALAXY COMMAND - SPACE MANAGEMENT 🚀")
        print("=" * 45)
        print("1. Manage Astronauts (Full CRUD)")
        print("2. Manage Missions & Assignments")
        print("3. View Agencies Directory")
        print("4. Business Analytics & Reports")
        print("9. 🛠️  Admin: Reset Database (Seed)")
        print("0. Exit")
        print("=" * 45)

        choice = input("Select: ")
        if choice == "1":
            manage_astronauts()
        elif choice == "2":
            manage_missions()
        elif choice == "3":
            view_agencies()
        elif choice == "4":
            view_analytics()
        elif choice == "9":
            run_admin_seed()
        elif choice == "0":
            print("Goodbye, Commander! 🌠")
            sys.exit()
        else:
            print("❌ Invalid choice. Please select from the menu.")


if __name__ == "__main__":
    try:
        run_main_menu()
    except KeyboardInterrupt:
        print("\nEmergency abort. Goodbye! 🌠")
        sys.exit()
