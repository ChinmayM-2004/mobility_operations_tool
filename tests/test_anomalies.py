
import unittest
from datetime import datetime, timedelta

from models.driver import Driver
from models.trip import Trip
from services.analytics_service import AnalyticsService
from services.anomaly_service import AnomalyConfig, AnomalyDetector


class TestAnomalyDetector(unittest.TestCase):

    def setUp(self):
        self.drivers = [
            Driver(
                driver_id="D101",
                driver_name="Rahul",
                city="Bangalore",
                vehicle_type="Sedan",
                rating=4.5,
                status="Active"
            ),
            Driver(
                driver_id="D102",
                driver_name="Priya",
                city="Mumbai",
                vehicle_type="SUV",
                rating=3.0,
                status="Active"
            ),
        ]

        self.base_time = datetime(2026, 1, 1, 10, 0, 0)

        self.normal_trip = self.create_trip(
            trip_id="T101",
            driver_id="D101",
            distance_km=10,
            fare=300,
            status="Completed",
            pickup_offset=5,
            drop_offset=35
        )

        self.unknown_driver_trip = self.create_trip(
            trip_id="T102",
            driver_id="D9999",
            distance_km=10,
            fare=300,
            status="Completed",
            pickup_offset=5,
            drop_offset=35
        )

        self.negative_fare_trip = self.create_trip(
            trip_id="T103",
            driver_id="D101",
            distance_km=10,
            fare=-100,
            status="Completed",
            pickup_offset=5,
            drop_offset=35
        )

        self.negative_distance_trip = self.create_trip(
            trip_id="T104",
            driver_id="D101",
            distance_km=-5,
            fare=300,
            status="Completed",
            pickup_offset=5,
            drop_offset=35
        )

        self.zero_distance_trip = self.create_trip(
            trip_id="T105",
            driver_id="D101",
            distance_km=0,
            fare=300,
            status="Completed",
            pickup_offset=5,
            drop_offset=35
        )

        self.long_trip = self.create_trip(
            trip_id="T106",
            driver_id="D101",
            distance_km=20,
            fare=300,
            status="Completed",
            pickup_offset=5,
            drop_offset=250
        )

        self.high_fare_trip = self.create_trip(
            trip_id="T107",
            driver_id="D101",
            distance_km=10,
            fare=1500,
            status="Completed",
            pickup_offset=5,
            drop_offset=35
        )

        self.drop_before_pickup_trip = self.create_trip(
            trip_id="T108",
            driver_id="D101",
            distance_km=10,
            fare=300,
            status="Completed",
            pickup_offset=30,
            drop_offset=10
        )

        self.missing_pickup_trip = self.create_trip(
            trip_id="T109",
            driver_id="D101",
            distance_km=10,
            fare=300,
            status="Completed",
            pickup_time=None,
            drop_offset=35
        )

    def create_trip(
        self,
        trip_id,
        driver_id,
        distance_km,
        fare,
        status,
        pickup_offset=5,
        drop_offset=35,
        pickup_time="default",
        drop_time="default"
    ):
        """
        Helper method for creating Trip objects using the
        actual Trip constructor.
        """

        if pickup_time == "default":
            pickup_time = self.base_time + timedelta(
                minutes=pickup_offset
            )

        if drop_time == "default":
            drop_time = self.base_time + timedelta(
                minutes=drop_offset
            )

        return Trip(
            trip_id=trip_id,
            driver_id=driver_id,
            rider_id=f"R{trip_id[1:]}",
            city="Bangalore",
            pickup_zone="Koramangala",
            drop_zone="Indiranagar",
            request_time=self.base_time,
            pickup_time=pickup_time,
            drop_time=drop_time,
            distance_km=distance_km,
            fare=fare,
            status=status,
            cancellation_reason=""
        )

    def create_analytics(self, trips=None, drivers=None):
        if trips is None:
            trips = [self.normal_trip]

        if drivers is None:
            drivers = self.drivers

        data = {
            "drivers": drivers,
            "trips": trips,
            "zones": [],
            "driver_activity": []
        }

        return AnalyticsService(data)

    # =========================================================
    # THRESHOLD TESTS
    # =========================================================

    def test_default_thresholds(self):
        detector = AnomalyDetector(AnomalyConfig())

        thresholds = detector.get_thresholds()

        self.assertEqual(
            thresholds["max_trip_duration_minutes"],
            180
        )

        self.assertEqual(
            thresholds["unusual_fare"],
            500
        )

        self.assertEqual(
            thresholds["high_cancellation_rate"],
            20
        )

        self.assertEqual(
            thresholds["low_utilization_rate"],
            50
        )

        self.assertEqual(
            thresholds["high_trip_count"],
            30
        )

        self.assertEqual(
            thresholds["low_rating"],
            3.5
        )

    def test_update_thresholds(self):
        detector = AnomalyDetector(AnomalyConfig())

        detector.update_thresholds(
            unusual_fare=500,
            high_trip_count=20
        )

        thresholds = detector.get_thresholds()

        self.assertEqual(
            thresholds["unusual_fare"],
            500
        )

        self.assertEqual(
            thresholds["high_trip_count"],
            20
        )

    # =========================================================
    # TRIP ANOMALY TESTS
    # =========================================================

    def test_unknown_driver_anomaly(self):
        detector = AnomalyDetector(AnomalyConfig())

        anomalies = detector.detect_trip_anomalies(
            [self.unknown_driver_trip],
            self.drivers
        )

        self.assertGreater(len(anomalies), 0)

    def test_negative_fare_anomaly(self):
        detector = AnomalyDetector(AnomalyConfig())

        anomalies = detector.detect_trip_anomalies(
            [self.negative_fare_trip],
            self.drivers
        )

        self.assertGreater(len(anomalies), 0)

    def test_negative_distance_anomaly(self):
        detector = AnomalyDetector(AnomalyConfig())

        anomalies = detector.detect_trip_anomalies(
            [self.negative_distance_trip],
            self.drivers
        )

        self.assertGreater(len(anomalies), 0)

    def test_zero_distance_anomaly(self):
        detector = AnomalyDetector(AnomalyConfig())

        anomalies = detector.detect_trip_anomalies(
            [self.zero_distance_trip],
            self.drivers
        )

        self.assertGreater(len(anomalies), 0)

    def test_missing_pickup_timestamp_anomaly(self):
        detector = AnomalyDetector(AnomalyConfig())

        anomalies = detector.detect_trip_anomalies(
            [self.missing_pickup_trip],
            self.drivers
        )

        self.assertGreater(len(anomalies), 0)

    def test_drop_before_pickup_anomaly(self):
        detector = AnomalyDetector(AnomalyConfig())

        anomalies = detector.detect_trip_anomalies(
            [self.drop_before_pickup_trip],
            self.drivers
        )

        self.assertGreater(len(anomalies), 0)

    def test_long_trip_anomaly(self):
        detector = AnomalyDetector(AnomalyConfig())

        anomalies = detector.detect_trip_anomalies(
            [self.long_trip],
            self.drivers
        )

        self.assertGreater(len(anomalies), 0)

    def test_unusual_fare_anomaly(self):
        detector = AnomalyDetector(AnomalyConfig())

        anomalies = detector.detect_trip_anomalies(
            [self.high_fare_trip],
            self.drivers
        )

        self.assertGreater(len(anomalies), 0)

    def test_normal_trip_has_no_anomaly(self):
        detector = AnomalyDetector(AnomalyConfig())

        anomalies = detector.detect_trip_anomalies(
            [self.normal_trip],
            self.drivers
        )

        self.assertEqual(len(anomalies), 0)

    # =========================================================
    # DRIVER ANOMALY TESTS
    # =========================================================

    def test_low_rating_driver_anomaly(self):
        detector = AnomalyDetector(AnomalyConfig())

        analytics = self.create_analytics()

        anomalies = detector.detect_driver_anomalies(
            self.drivers,
            analytics
        )

        self.assertGreater(len(anomalies), 0)

    def test_high_cancellation_rate_driver_anomaly(self):
        cancelled_trips = []

        for i in range(5):
            cancelled_trips.append(
                Trip(
                    trip_id=f"TC{i}",
                    driver_id="D101",
                    rider_id=f"RC{i}",
                    city="Bangalore",
                    pickup_zone="Koramangala",
                    drop_zone="Indiranagar",
                    request_time=self.base_time + timedelta(minutes=i),
                    pickup_time=None,
                    drop_time=None,
                    distance_km=10,
                    fare=300,
                    status="Cancelled",
                    cancellation_reason="Driver Cancelled"
                )
            )

        analytics = self.create_analytics(
            trips=cancelled_trips
        )

        detector = AnomalyDetector(
            AnomalyConfig(
                high_cancellation_rate=20
            )
        )

        anomalies = detector.detect_driver_anomalies(
            self.drivers,
            analytics
        )

        self.assertGreater(len(anomalies), 0)

    def test_high_trip_count_driver_anomaly(self):
        trips = []

        for i in range(31):
            start_time = (
                self.base_time +
                timedelta(hours=i)
            )

            trips.append(
                Trip(
                    trip_id=f"TH{i}",
                    driver_id="D101",
                    rider_id=f"RH{i}",
                    city="Bangalore",
                    pickup_zone="Koramangala",
                    drop_zone="Indiranagar",
                    request_time=start_time,
                    pickup_time=start_time + timedelta(minutes=5),
                    drop_time=start_time + timedelta(minutes=35),
                    distance_km=10,
                    fare=300,
                    status="Completed",
                    cancellation_reason=""
                )
            )

        analytics = self.create_analytics(
            trips=trips
        )

        detector = AnomalyDetector(
            AnomalyConfig(
                high_trip_count=30
            )
        )

        anomalies = detector.detect_driver_anomalies(
            self.drivers,
            analytics
        )

        self.assertGreater(len(anomalies), 0)

    # =========================================================
    # COMBINED DETECTION TESTS
    # =========================================================

    def test_detect_all_returns_expected_structure(self):
        detector = AnomalyDetector(AnomalyConfig())

        trips = [
            self.normal_trip,
            self.negative_fare_trip,
            self.unknown_driver_trip
        ]

        analytics = self.create_analytics(
            trips=trips
        )

        result = detector.detect_all(
            trips=trips,
            drivers=self.drivers,
            analytics=analytics
        )

        self.assertIn(
            "total_anomalies",
            result
        )

        self.assertIn(
            "severity_counts",
            result
        )

        self.assertIn(
            "issue_counts",
            result
        )

        self.assertIn(
            "thresholds",
            result
        )

        self.assertIn(
            "anomalies",
            result
        )

        self.assertGreater(
            result["total_anomalies"],
            0
        )

        self.assertGreater(
            len(result["anomalies"]),
            0
        )

    def test_detect_all_counts_trip_anomalies(self):
        detector = AnomalyDetector(AnomalyConfig())

        trips = [
            self.normal_trip,
            self.negative_fare_trip,
            self.negative_distance_trip,
            self.high_fare_trip
        ]

        analytics = self.create_analytics(
            trips=trips
        )

        result = detector.detect_all(
            trips=trips,
            drivers=self.drivers,
            analytics=analytics
        )

        self.assertGreaterEqual(
            result["total_anomalies"],
            3
        )

    # =========================================================
    # EMPTY DATA TESTS
    # =========================================================

    def test_empty_trip_data(self):
        detector = AnomalyDetector(AnomalyConfig())

        anomalies = detector.detect_trip_anomalies(
            [],
            self.drivers
        )

        self.assertEqual(
            len(anomalies),
            0
        )

    def test_empty_driver_data(self):
        detector = AnomalyDetector(AnomalyConfig())

        analytics = self.create_analytics(
            trips=[],
            drivers=[]
        )

        anomalies = detector.detect_driver_anomalies(
            [],
            analytics
        )

        self.assertEqual(
            len(anomalies),
            0
        )

    def test_detect_all_empty_data(self):
        detector = AnomalyDetector(AnomalyConfig())

        analytics = self.create_analytics(
            trips=[],
            drivers=[]
        )

        result = detector.detect_all(
            trips=[],
            drivers=[],
            analytics=analytics
        )

        self.assertEqual(
            result["total_anomalies"],
            0
        )

        self.assertEqual(
            len(result["anomalies"]),
            0
        )


if __name__ == "__main__":
    unittest.main()
