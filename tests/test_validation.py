
import unittest

from models.driver import Driver
from models.trip import Trip
from services.validation_service import DataValidator


class TestDataValidation(unittest.TestCase):

    def make_driver(
        self,
        driver_id="D001",
        driver_name="Rahul",
        city="Bangalore",
        vehicle_type="Sedan",
        rating=4.5,
        status="Active"
    ):
        return Driver(
            driver_id,
            driver_name,
            city,
            vehicle_type,
            rating,
            status
        )

    def make_trip(
        self,
        trip_id="T001",
        driver_id="D001",
        rider_id="R001",
        city="Bangalore",
        pickup_zone="Koramangala",
        drop_zone="Indiranagar",
        request_time="2023-10-01 10:00:00",
        pickup_time="2023-10-01 10:05:00",
        drop_time="2023-10-01 10:30:00",
        distance_km=10,
        fare=300,
        status="Completed",
        cancellation_reason=""
    ):
        return Trip(
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
        )

    # ---------------------------------------------------------
    # Basic validation tests
    # ---------------------------------------------------------

    def test_valid_driver(self):
        validator = DataValidator()

        driver = self.make_driver()

        result = validator.validate_all(
            [driver],
            [],
            []
        )

        self.assertTrue(result["valid"])
        self.assertEqual(result["error_count"], 0)

    def test_invalid_driver_rating(self):
        validator = DataValidator()

        driver = self.make_driver(rating=6)

        result = validator.validate_all(
            [driver],
            [],
            []
        )

        self.assertFalse(result["valid"])
        self.assertTrue(
            any(
                "Invalid rating" in error
                for error in result["errors"]
            )
        )

    def test_invalid_driver_status(self):
        validator = DataValidator()

        driver = self.make_driver(status="Unknown")

        result = validator.validate_all(
            [driver],
            [],
            []
        )

        self.assertFalse(result["valid"])
        self.assertTrue(
            any(
                "Invalid status" in error
                for error in result["errors"]
            )
        )

    def test_unknown_driver_id(self):
        validator = DataValidator()

        driver = self.make_driver()

        trip = self.make_trip(
            driver_id="D9999"
        )

        result = validator.validate_all(
            [driver],
            [trip],
            []
        )

        self.assertFalse(result["valid"])
        self.assertTrue(
            any(
                "Unknown driver_id" in error
                for error in result["errors"]
            )
        )

    def test_negative_fare(self):
        validator = DataValidator()

        driver = self.make_driver()

        trip = self.make_trip(
            fare=-100
        )

        result = validator.validate_all(
            [driver],
            [trip],
            []
        )

        self.assertFalse(result["valid"])
        self.assertTrue(
            any(
                "Negative fare" in error
                for error in result["errors"]
            )
        )

    def test_negative_distance(self):
        validator = DataValidator()

        driver = self.make_driver()

        trip = self.make_trip(
            distance_km=-5
        )

        result = validator.validate_all(
            [driver],
            [trip],
            []
        )

        self.assertFalse(result["valid"])
        self.assertTrue(
            any(
                "Negative distance" in error
                for error in result["errors"]
            )
        )

    def test_missing_pickup_timestamp(self):
        validator = DataValidator()

        driver = self.make_driver()

        trip = self.make_trip(
            pickup_time=None
        )

        result = validator.validate_all(
            [driver],
            [trip],
            []
        )

        self.assertFalse(result["valid"])
        self.assertTrue(
            any(
                "Missing pickup_time" in error
                for error in result["errors"]
            )
        )

    def test_drop_before_pickup(self):
        validator = DataValidator()

        driver = self.make_driver()

        trip = self.make_trip(
            pickup_time="2023-10-01 10:30:00",
            drop_time="2023-10-01 10:10:00"
        )

        result = validator.validate_all(
            [driver],
            [trip],
            []
        )

        self.assertFalse(result["valid"])
        self.assertTrue(
            any(
                "drop_time occurs before pickup_time" in error
                for error in result["errors"]
            )
        )

    def test_missing_cancellation_reason_warning(self):
        validator = DataValidator()

        driver = self.make_driver()

        trip = self.make_trip(
            status="Cancelled",
            pickup_time=None,
            drop_time=None,
            cancellation_reason=""
        )

        result = validator.validate_all(
            [driver],
            [trip],
            []
        )

        self.assertTrue(result["valid"])
        self.assertEqual(result["error_count"], 0)
        self.assertEqual(result["warning_count"], 1)

        self.assertTrue(
            any(
                "Missing cancellation reason" in warning
                for warning in result["warnings"]
            )
        )

    def test_invalid_activity_timestamp(self):
        validator = DataValidator()

        activity = [
            {
                "driver_id": "D001",
                "timestamp": "invalid-date",
                "status": "online"
            }
        ]

        result = validator.validate_all(
            [],
            [],
            activity
        )

        self.assertFalse(result["valid"])
        self.assertTrue(
            any(
                "Invalid timestamp" in error
                for error in result["errors"]
            )
        )

    def test_invalid_activity_status(self):
        validator = DataValidator()

        activity = [
            {
                "driver_id": "D001",
                "timestamp": "2023-10-01 10:00:00",
                "status": "unknown"
            }
        ]

        result = validator.validate_all(
            [],
            [],
            activity
        )

        self.assertFalse(result["valid"])
        self.assertTrue(
            any(
                "Invalid status" in error
                for error in result["errors"]
            )
        )

    def test_empty_datasets(self):
        validator = DataValidator()

        result = validator.validate_all(
            [],
            [],
            []
        )

        self.assertTrue(result["valid"])
        self.assertEqual(result["error_count"], 0)
        self.assertEqual(result["warning_count"], 0)

    # ---------------------------------------------------------
    # Missing required column tests
    # ---------------------------------------------------------

    def test_missing_driver_columns(self):
        validator = DataValidator()

        columns = {
            "driver_id",
            "driver_name"
        }

        validator.validate_required_columns(
            columns,
            validator.REQUIRED_DRIVER_COLUMNS,
            "Drivers"
        )

        self.assertTrue(
            any(
                "Missing required column 'city'" in error
                for error in validator.errors
            )
        )

        self.assertTrue(
            any(
                "Missing required column 'rating'" in error
                for error in validator.errors
            )
        )

    def test_missing_trip_columns(self):
        validator = DataValidator()

        columns = {
            "trip_id",
            "driver_id",
            "rider_id"
        }

        validator.validate_required_columns(
            columns,
            validator.REQUIRED_TRIP_COLUMNS,
            "Trips"
        )

        self.assertTrue(
            any(
                "Missing required column 'fare'" in error
                for error in validator.errors
            )
        )

        self.assertTrue(
            any(
                "Missing required column 'request_time'" in error
                for error in validator.errors
            )
        )

    def test_missing_activity_columns(self):
        validator = DataValidator()

        columns = {
            "driver_id"
        }

        validator.validate_required_columns(
            columns,
            validator.REQUIRED_ACTIVITY_COLUMNS,
            "Driver Activity"
        )

        self.assertTrue(
            any(
                "Missing required column 'timestamp'" in error
                for error in validator.errors
            )
        )

        self.assertTrue(
            any(
                "Missing required column 'status'" in error
                for error in validator.errors
            )
        )

    # ---------------------------------------------------------
    # Duplicate record tests
    # ---------------------------------------------------------

    def test_duplicate_driver_id(self):
        validator = DataValidator()

        driver1 = self.make_driver(
            driver_id="D001"
        )

        driver2 = self.make_driver(
            driver_id="D001",
            driver_name="Amit"
        )

        result = validator.validate_all(
            [driver1, driver2],
            [],
            []
        )

        self.assertFalse(result["valid"])

        self.assertTrue(
            any(
                "Duplicate driver_id" in error
                for error in result["errors"]
            )
        )

    def test_duplicate_trip_id(self):
        validator = DataValidator()

        driver = self.make_driver()

        trip1 = self.make_trip(
            trip_id="T001"
        )

        trip2 = self.make_trip(
            trip_id="T001",
            rider_id="R002"
        )

        result = validator.validate_all(
            [driver],
            [trip1, trip2],
            []
        )

        self.assertFalse(result["valid"])

        self.assertTrue(
            any(
                "Duplicate trip_id" in error
                for error in result["errors"]
            )
        )

    def test_duplicate_activity_record(self):
        validator = DataValidator()

        activity_record = {
            "driver_id": "D001",
            "timestamp": "2023-10-01 10:00:00",
            "status": "online"
        }

        activity = [
            activity_record,
            activity_record.copy()
        ]

        result = validator.validate_all(
            [],
            [],
            activity
        )

        self.assertFalse(result["valid"])

        self.assertTrue(
            any(
                "Duplicate record" in error
                for error in result["errors"]
            )
        )


if __name__ == "__main__":
    unittest.main()
