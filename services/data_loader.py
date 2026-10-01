import csv

from models.driver import Driver
from models.trip import Trip
from models.zone import Zone


class DataLoader:
    """Loads CSV files and converts records into Python objects."""

    def __init__(self):
        self.drivers = []
        self.trips = []
        self.zones = []
        self.driver_activity = []

    def load_drivers(self, file_path):
        """Load drivers.csv and create Driver objects."""
        self.drivers = []

        with open(file_path, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                driver = Driver(
                    driver_id=row["driver_id"],
                    driver_name=row["driver_name"],
                    city=row["city"],
                    vehicle_type=row["vehicle_type"],
                    rating=row["rating"],
                    status=row["status"]
                )

                self.drivers.append(driver)

        return self.drivers

    def load_trips(self, file_path):
        """Load trips.csv and create Trip objects."""
        self.trips = []

        with open(file_path, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                trip = Trip(
                    trip_id=row["trip_id"],
                    driver_id=row["driver_id"],
                    rider_id=row["rider_id"],
                    city=row["city"],
                    pickup_zone=row["pickup_zone"],
                    drop_zone=row["drop_zone"],
                    request_time=row["request_time"],
                    pickup_time=row["pickup_time"],
                    drop_time=row["drop_time"],
                    distance_km=row["distance_km"],
                    fare=row["fare"],
                    status=row["status"],
                    cancellation_reason=row["cancellation_reason"]
                )

                self.trips.append(trip)

        return self.trips

    def load_driver_activity(self, file_path):
        """Load driver activity records."""
        self.driver_activity = []

        with open(file_path, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                self.driver_activity.append({
                    "driver_id": row["driver_id"],
                    "timestamp": row["timestamp"],
                    "status": row["status"]
                })

        return self.driver_activity

    def create_zones(self):
        """
        Create unique Zone objects from the trip data.

        A zone is identified by its name and city.
        Both pickup and drop zones are included.
        """
        zone_map = {}

        for trip in self.trips:
            pickup_key = (trip.city, trip.pickup_zone)

            if pickup_key not in zone_map:
                zone_map[pickup_key] = Zone(
                    zone_name=trip.pickup_zone,
                    city=trip.city
                )

            if trip.drop_zone:
                drop_key = (trip.city, trip.drop_zone)

                if drop_key not in zone_map:
                    zone_map[drop_key] = Zone(
                        zone_name=trip.drop_zone,
                        city=trip.city
                    )

        self.zones = list(zone_map.values())

        return self.zones

    def load_all(self, drivers_path, trips_path, activity_path):
        """Load all datasets and create the corresponding objects."""
        self.load_drivers(drivers_path)
        self.load_trips(trips_path)
        self.load_driver_activity(activity_path)
        self.create_zones()

        return {
            "drivers": self.drivers,
            "trips": self.trips,
            "zones": self.zones,
            "driver_activity": self.driver_activity
        }