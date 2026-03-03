from crud import AgencyRepository, SpacecraftRepository
from utils import get_valid_int

agency_repo = AgencyRepository()
sc_repo = SpacecraftRepository()


def view_agencies():
    """Displays agencies and allows viewing their spacecrafts"""
    while True:
        agencies = agency_repo.get_all()
        if not agencies:
            print("\n🌌 Empty Space: No agencies found.")
            break

        print("\n--- 🏢 Registered Space Agencies ---")
        for ag in agencies:
            print(f"ID: {ag['id']} | Agency: {ag['name']} ({ag['country']})")

        print("\nOptions:")
        print("1. View spacecrafts for an agency")
        print("0. Back")

        choice = input("Select: ")

        if choice == "1":
            agency_id = get_valid_int("Enter Agency ID: ")
            spacecrafts = sc_repo.get_by_agency(agency_id)
            if not spacecrafts:
                print("🚫 No spacecrafts found for this agency.")
            else:
                print("\n--- 🚀 Spacecrafts for Selected Agency ---")
                for sc in spacecrafts:
                    print(
                        f"ID: {sc['id']} | Model: {sc['model_name']} | Agency ID: {sc['agency_id']}"
                    )

        elif choice == "0":
            break
        else:
            print("❌ Invalid choice. Please try again.")
