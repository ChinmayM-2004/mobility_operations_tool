class Zone:
    def __init__(self, zone_name, city):
        self.zone_name = zone_name
        self.city = city

    def get_profile(self):
        """Return basic zone information."""
        return {
            "zone_name": self.zone_name,
            "city": self.city
        }

    def __repr__(self):
        return (
            f"Zone("
            f"zone_name='{self.zone_name}', "
            f"city='{self.city}')"
        )