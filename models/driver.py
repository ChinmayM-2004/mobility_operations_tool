class Driver:
    def __init__(
        self,
        driver_id,
        driver_name,
        city,
        vehicle_type,
        rating,
        status
    ):
        self.driver_id = driver_id
        self.driver_name = driver_name
        self.city = city
        self.vehicle_type = vehicle_type
        self.rating = float(rating)
        self.status = status

    def is_active(self):
        """Return True if the driver is currently active."""
        return self.status.lower() == "active"

    def get_profile(self):
        """Return the driver's basic profile as a dictionary."""
        return {
            "driver_id": self.driver_id,
            "driver_name": self.driver_name,
            "city": self.city,
            "vehicle_type": self.vehicle_type,
            "rating": self.rating,
            "status": self.status
        }

    def __repr__(self):
        return (
            f"Driver("
            f"driver_id='{self.driver_id}', "
            f"name='{self.driver_name}', "
            f"city='{self.city}', "
            f"status='{self.status}')"
        )