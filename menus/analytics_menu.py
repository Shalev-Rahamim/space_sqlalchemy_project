from services.queries import SpaceAnalyticsService

analytics = SpaceAnalyticsService()


def view_analytics():
    while True:
        print("\n--- 📊 Space Analytics Reports ---")
        print("1. Agency Fleet Storage Capacity (JOIN + SUM)")
        print("2. Top Experienced Astronauts (JOIN + COUNT)")
        print("3. Agency Fleet Sizes (OUTER JOIN)")
        print("4. Mission Average Experience (JOIN + AVG)")
        print("5. Destination Popularity (COUNT + GROUP BY)")
        print("0. Back")

        choice = input("Select: ")
        if choice == "1":
            # Ensure queries.py has 'get_agency_storage_capacity' implemented
            try:
                results = analytics.get_agency_storage_capacity()
            except AttributeError:
                print(
                    "❌ Error: 'get_agency_storage_capacity' not found in queries.py. Please update the queries file."
                )
                continue

            print("\n🌐 Total Black Box Storage per Agency")
            for row in results:
                print(f"- {row['agency']}: {row['total_storage_gb']} GB")

        elif choice == "2":
            results = analytics.get_astronauts_mission_count()
            print("\n👨‍🚀 Astronaut Ranking by Number of Missions")
            for row in results:
                print(f"- {row['astronaut']}: {row['missions']} missions")

        elif choice == "3":
            results = analytics.get_fleet_statistics()
            print("\n🚀 Fleet Size per Agency")
            for row in results:
                print(f"- {row['agency']}: {row['spacecraft_count']} spacecraft(s)")

        elif choice == "4":
            results = analytics.get_mission_complexity_report()
            print("\n🧠 Average Crew Experience per Mission")
            for row in results:
                print(f"- {row['mission']}: {row['avg_experience']} years avg exp")

        elif choice == "5":
            results = analytics.get_top_destinations()
            print("\n🌍 Most Popular Destinations")
            for row in results:
                print(f"- {row['destination']}: {row['visits']} missions")

        elif choice == "0":
            break
        else:
            print("❌ Invalid choice. Please try again.")
