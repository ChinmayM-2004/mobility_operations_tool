from datetime import datetime


class Trip:
    def __init__(
        self,
        trip_id,
        driver_id,
        rider_id,
        city,
        pickup_zone,
        drop_zone,
        request_time,
        pickup_time,
        drop_time,
        distance_km,
        fare,
        status,
        cancellation_reason
    ):
        self.trip_id = trip_id
        self.driver_id = driver_id
        self.rider_id = rider_id
        self.city = city
        self.pickup_zone = pickup_zone
        self.drop_zone = drop_zone

        self.request_time = self._parse_datetime(request_time)
        self.pickup_time = self._parse_datetime(pickup_time)
        self.drop_time = self._parse_datetime(drop_time)

        self.distance_km = float(distance_km)
        self.fare = float(fare)
        self.status = status
        self.cancellation_reason = cancellation_reason

    @staticmethod
    def _parse_datetime(value):
        """Convert a CSV timestamp into a datetime object."""
        if not value:
            return None

        if isinstance(value, datetime):
            return value

        return datetime.strptime(value, "%Y-%m-%d %H:%M:%S")

    def is_completed(self):
        """Return True if the trip is completed."""
        return self.status.lower() == "completed"

    def is_cancelled(self):
        """Return True if the trip is cancelled."""
        return self.status.lower() == "cancelled"

    def calculate_duration(self):
        """Return trip duration in minutes."""
        if not self.pickup_time or not self.drop_time:
            return None

        duration = self.drop_time - self.pickup_time
        return duration.total_seconds() / 60

    def calculate_fare_per_km(self):
        """Return fare per kilometer."""
        if self.distance_km <= 0:
            return None

        return self.fare / self.distance_km

    def __repr__(self):
        return (
            f"Trip("
            f"trip_id='{self.trip_id}', "
            f"driver_id='{self.driver_id}', "
            f"status='{self.status}')"
        )