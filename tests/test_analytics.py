
import unittest

from models.driver import Driver
from models.trip import Trip
from models.zone import Zone
from services.analytics_service import AnalyticsService


class TestAnalyticsService(unittest.TestCase):

    def setUp(self):

        self.drivers = [
            Driver(
                "D001",
                "Rahul",
                "Bangalore",
                "Sedan",
                4.5,
                "Active"
            ),
            Driver(
                "D002",
                "Priya",
                "Mumbai",
                "SUV",
                4.8,
                "Active"
            ),
            Driver(
                "D003",
                "Amit",
                "Delhi",
                "Hatchback",
                3.9,
                "Inactive"
            )
        ]

        self.trips = [
            Trip(
                "T001",
                "D001",
                "R001",
                "Bangalore",
                "Koramangala",
                "Indiranagar",
                "2023-10-01 10:00:00",
                "2023-10-01 10:05:00",
                "2023-10-01 10:30:00",
                10,
                300,
                "Completed",
                ""
            ),
            Trip(
                "T002",
                "D001",
                "R002",
                "Bangalore",
                "HSR Layout",
                "Whitefield",
                "2023-10-01 11:00:00",
                "2023-10-01 11:10:00",
                "2023-10-01 11:45:00",
                15,
                450,
                "Completed",
                ""
            ),
            Trip(
                "T003",
                "D002",
                "R003",
                "Mumbai",
                "Bandra",
                "Andheri",
                "2023-10-01 12:00:00",
                None,
                None,
                8,
                200,
                "Cancelled",
                "Driver Cancelled"
            ),
            Trip(
                "T004",
                "D003",
                "R004",
                "Delhi",
                "Saket",
                "Rohini",
                "2023-10-01 13:00:00",
                "2023-10-01 13:10:00",
                "2023-10-01 13:40:00",
                12,
                350,
                "Completed",
                ""
            )
        ]

        self.zones = [
            Zone(
                "Koramangala",
                "Bangalore"
            ),
            Zone(
                "Indiranagar",
                "Bangalore"
            ),
            Zone(
                "HSR Layout",
                "Bangalore"
            ),
            Zone(
                "Whitefield",
                "Bangalore"
            ),
            Zone(
                "Bandra",
                "Mumbai"
            ),
            Zone(
                "Andheri",
                "Mumbai"
            ),
            Zone(
                "Saket",
                "Delhi"
            ),
            Zone(
                "Rohini",
                "Delhi"
            )
        ]

        self.driver_activity = [
            {
                "driver_id": "D001",
                "timestamp": "2023-10-01 09:00:00",
                "status": "online"
            },
            {
                "driver_id": "D001",
                "timestamp": "2023-10-01 10:00:00",
                "status": "busy"
            },
            {
                "driver_id": "D001",
                "timestamp": "2023-10-01 12:00:00",
                "status": "offline"
            },
            {
                "driver_id": "D002",
                "timestamp": "2023-10-01 09:00:00",
                "status": "online"
            },
            {
                "driver_id": "D002",
                "timestamp": "2023-10-01 12:00:00",
                "status": "idle"
            },
            {
                "driver_id": "D003",
                "timestamp": "2023-10-01 09:00:00",
                "status": "offline"
            }
        ]

        self.data = {
            "drivers": self.drivers,
            "trips": self.trips,
            "zones": self.zones,
            "driver_activity": self.driver_activity
        }

        self.analytics = AnalyticsService(
            self.data
        )

    # ---------------------------------------------------------
    # Lookup tests
    # ---------------------------------------------------------

    def test_get_driver(self):
        result = self.analytics.get_driver("D001")

        self.assertIsNotNone(result)
        self.assertEqual(
            result.driver_id,
            "D001"
        )

    def test_get_trip(self):
        result = self.analytics.get_trip("T001")

        self.assertIsNotNone(result)
        self.assertEqual(
            result.trip_id,
            "T001"
        )

    def test_get_zone(self):
        result = self.analytics.get_zone(
            "Bangalore",
            "Koramangala"
        )

        self.assertIsNotNone(result)
        self.assertEqual(
            result.zone_name,
            "Koramangala"
        )

    # ---------------------------------------------------------
    # No matching search result tests
    # ---------------------------------------------------------

    def test_get_driver_no_match(self):
        result = self.analytics.get_driver(
            "D9999"
        )

        self.assertIsNone(result)

    def test_get_trip_no_match(self):
        result = self.analytics.get_trip(
            "T9999"
        )

        self.assertIsNone(result)

    def test_get_zone_no_match(self):
        result = self.analytics.get_zone(
            "Bangalore",
            "NonExistentZone"
        )

        self.assertIsNone(result)

    # ---------------------------------------------------------
    # Dashboard KPI tests
    # ---------------------------------------------------------

    def test_dashboard_kpis(self):
        result = self.analytics.get_dashboard_kpis()

        self.assertEqual(
            result["total_drivers"],
            3
        )

        self.assertEqual(
            result["active_drivers"],
            2
        )

        self.assertEqual(
            result["total_trips"],
            4
        )

        self.assertEqual(
            result["completed_trips"],
            3
        )

        self.assertEqual(
            result["cancelled_trips"],
            1
        )

        self.assertAlmostEqual(
            result["completion_rate"],
            75.0
        )

        self.assertAlmostEqual(
            result["cancellation_rate"],
            25.0
        )

    # ---------------------------------------------------------
    # Trip status tests
    # ---------------------------------------------------------

    def test_trip_status_counts(self):
        result = self.analytics.get_trip_status_counts()

        self.assertEqual(
            result["Completed"],
            3
        )

        self.assertEqual(
            result["Cancelled"],
            1
        )

    # ---------------------------------------------------------
    # Cancellation tests
    # ---------------------------------------------------------

    def test_cancellation_reasons(self):
        result = self.analytics.get_cancellation_reasons()

        self.assertEqual(
            result["Driver Cancelled"],
            1
        )

    # ---------------------------------------------------------
    # Revenue tests
    # ---------------------------------------------------------

    def test_trip_revenue_by_city(self):
        result = self.analytics.get_trip_revenue_by_city()

        self.assertEqual(
            result["Bangalore"],
            750
        )

        self.assertEqual(
            result["Delhi"],
            350
        )

        # Mumbai has no completed trips with revenue,
        # so the implementation omits it from the result.
        self.assertNotIn(
            "Mumbai",
            result
        )

    # ---------------------------------------------------------
    # Driver performance tests
    # ---------------------------------------------------------

    def test_driver_performance(self):
        result = self.analytics.get_driver_performance(
            "D001"
        )

        self.assertEqual(
            result["completed_trips"],
            2
        )

        self.assertEqual(
            result["revenue"],
            750
        )

    def test_driver_rankings_completed_trips(self):
        result = self.analytics.get_driver_rankings(
            "completed_trips",
            top_k=2
        )

        self.assertEqual(
            len(result),
            2
        )

        self.assertEqual(
            result[0]["driver_id"],
            "D001"
        )

    def test_driver_rankings_revenue(self):
        result = self.analytics.get_driver_rankings(
            "revenue",
            top_k=2
        )

        self.assertEqual(
            result[0]["driver_id"],
            "D001"
        )

        self.assertEqual(
            result[0]["revenue"],
            750
        )

    def test_driver_rankings_cancellation_rate(self):
        result = self.analytics.get_driver_rankings(
            "cancellation_rate",
            top_k=3
        )

        self.assertEqual(
            len(result),
            3
        )

    def test_invalid_driver_ranking_metric(self):
        with self.assertRaises(ValueError):
            self.analytics.get_driver_rankings(
                "invalid_metric"
            )

    # ---------------------------------------------------------
    # Driver trip frequency
    # ---------------------------------------------------------

    def test_driver_trip_frequency(self):
        result = self.analytics.get_driver_trip_frequency()

        self.assertEqual(
            result["D001"],
            2
        )

        self.assertEqual(
            result["D002"],
            1
        )

    # ---------------------------------------------------------
    # Zone performance
    # ---------------------------------------------------------

    def test_zone_performance(self):
        result = self.analytics.get_zone_performance(
            "Bangalore",
            "Koramangala"
        )

        self.assertEqual(
            result["requests"],
            1
        )

        self.assertEqual(
            result["completed_trips"],
            1
        )

    def test_zone_demand(self):
        result = self.analytics.get_zone_demand()

        self.assertTrue(
            isinstance(result, list)
        )

        koramangala = next(
            item for item in result
            if item["zone"] == "Koramangala"
        )

        hsr_layout = next(
            item for item in result
            if item["zone"] == "HSR Layout"
        )

        self.assertEqual(
            koramangala["requests"],
            1
        )

        self.assertEqual(
            hsr_layout["requests"],
            1
        )

    def test_top_k_zones(self):
        result = self.analytics.get_top_k_zones(
            top_k=3
        )

        self.assertEqual(
            len(result),
            3
        )

    # ---------------------------------------------------------
    # Consecutive trip analysis
    # ---------------------------------------------------------

    def test_consecutive_trip_analysis(self):
        result = self.analytics.get_consecutive_trip_analysis(
            driver_id="D001",
            max_gap_minutes=45
        )

        self.assertEqual(
            len(result),
            1
        )

        self.assertEqual(
            result[0]["sequence_length"],
            2
        )

        self.assertEqual(
            result[0]["trip_ids"],
            ["T001", "T002"]
        )

    # ---------------------------------------------------------
    # Idle time analysis
    # ---------------------------------------------------------

    def test_idle_time_analysis(self):
        result = self.analytics.get_idle_time_analysis(
            min_idle_minutes=30
        )

        self.assertTrue(
            isinstance(result, list)
        )

    def test_driver_idle_summary(self):
        result = self.analytics.get_driver_idle_summary()

        self.assertTrue(
            isinstance(result, list)
        )

    # ---------------------------------------------------------
    # Peak demand
    # ---------------------------------------------------------

    def test_peak_demand(self):
        result = self.analytics.get_peak_demand(
            top_k=3
        )

        self.assertEqual(
            len(result),
            3
        )

    def test_peak_demand_by_city(self):
        result = self.analytics.get_peak_demand_by_city(
            top_k=2
        )

        self.assertTrue(
            isinstance(result, list)
        )

        self.assertGreater(
            len(result),
            0
        )

        self.assertIn(
            "city",
            result[0]
        )

        self.assertIn(
            "peak_hours",
            result[0]
        )

    # ---------------------------------------------------------
    # Utilization
    # ---------------------------------------------------------

    def test_driver_utilization(self):
        result = self.analytics.get_driver_utilization()

        self.assertTrue(
            isinstance(result, list)
        )

        self.assertEqual(
            len(result),
            3
        )

        d001 = next(
            item for item in result
            if item["driver_id"] == "D001"
        )

        self.assertGreater(
            d001["utilization"],
            0
        )

    def test_top_utilized_drivers(self):
        result = self.analytics.get_top_utilized_drivers(
            top_k=2
        )

        self.assertEqual(
            len(result),
            2
        )

    # ---------------------------------------------------------
    # Cancellation intelligence
    # ---------------------------------------------------------

    def test_cancellation_intelligence(self):
        result = self.analytics.get_cancellation_intelligence()

        self.assertTrue(
            isinstance(result, dict)
        )

        self.assertEqual(
            result["total_trips"],
            4
        )

        self.assertEqual(
            result["cancelled_trips"],
            1
        )

        self.assertAlmostEqual(
            result["overall_rate"],
            25.0
        )

    # ---------------------------------------------------------
    # Rider frequency
    # ---------------------------------------------------------

    def test_rider_trip_frequency(self):
        result = self.analytics.get_rider_trip_frequency()

        self.assertEqual(
            result["R001"],
            1
        )


if __name__ == "__main__":
    unittest.main()
