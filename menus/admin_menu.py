from scripts.seed import seed_data


def run_admin_seed():
    """Tries to seed the database after user confirmation"""
    print("\n⚠️  WARNING: This will DELETE ALL DATA and reset the database!")
    confirm = input("Are you sure you want to proceed? (yes/no): ").strip().lower()

    if confirm == "yes":
        try:
            print("⏳ Resetting database... please wait.")
            seed_data()
            print("✅ Database reset complete! New data is ready.")
        except Exception as e:
            print(f"❌ Error during seed: {e}")
    else:
        print("🛡️  Operation cancelled. Data is safe.")
