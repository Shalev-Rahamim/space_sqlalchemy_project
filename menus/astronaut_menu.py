from crud import AstronautRepository
from utils import get_valid_int, get_non_empty_input, get_optional_input
from utils.logger import log_action

astro_repo = AstronautRepository()


def manage_astronauts():
    while True:
        print("\n--- 👨‍🚀 Astronaut Management ---")
        print("1. View all Astronauts")
        print("2. Add new Astronaut")
        print("3. Update Astronaut")
        print("4. Delete Astronaut")
        print("0. Back")

        choice = input("Select: ")

        if choice == "1":
            astronauts = astro_repo.get_all()
            if not astronauts:
                print("🚫 No astronauts found.")
            else:
                for a in astronauts:
                    print(
                        f"ID: {a['id']} | Name: {a['name']} | Rank: {a['rank']} | Exp: {a['years_of_experience']}y"
                    )

        elif choice == "2":
            print("\n🆕 New Astronaut Details:")
            name = get_non_empty_input("Name: ")
            rank = get_non_empty_input("Rank: ")
            exp = get_valid_int("Years of Experience: ", min_val=0)
            astro_repo.create(name=name, rank=rank, years_of_experience=exp)
            log_action(f"CREATED Astronaut: {name}, Rank: {rank}")
            print("✅ Added successfully!")

        elif choice == "3":
            try:
                a_id = get_valid_int("Enter Astronaut ID to update: ")
                print("Leave fields blank to keep current values.")
                new_name = get_optional_input("New Name: ")
                new_rank = get_optional_input("New Rank: ")

                if astro_repo.update(a_id, new_name=new_name, new_rank=new_rank):
                    log_action(
                        f"UPDATED Astronaut ID {a_id}. New Name: {new_name}, New Rank: {new_rank}"
                    )
                    print("✅ Astronaut updated successfully!")
                else:
                    print("❌ Astronaut ID not found.")
            except Exception as e:
                print(f"❌ An error occurred: {e}")

        elif choice == "4":
            a_id = get_valid_int("Enter Astronaut ID to delete: ")
            if astro_repo.delete(a_id):
                log_action(f"DELETED Astronaut ID {a_id}")
                print("✅ Astronaut deleted!")

            else:
                print("❌ Astronaut ID not found.")

        elif choice == "0":
            break
        else:
            print("❌ Invalid choice.")
