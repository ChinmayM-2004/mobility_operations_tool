from dataclasses import dataclass


# ---------------------------------------------------------
# ANOMALY CONFIGURATION
# ---------------------------------------------------------

@dataclass
class AnomalyConfig:
    """Configurable thresholds used by the anomaly detector."""

    max_trip_duration_minutes: float = 180.0
    unusual_fare: float = 500.0

    high_cancellation_rate: float = 20.0
    low_utilization_rate: float = 50.0

    high_trip_count: int = 30
    low_rating: float = 3.5

    min_distance_km: float = 0.0


# ---------------------------------------------------------
# ANOMALY RESULT
# ---------------------------------------------------------

@dataclass
class AnomalyResult:
    """Represents one detected anomaly."""

    anomaly_type: str
    entity_id: str
    issue: str
    severity: str
    details: str
    metadata: dict


# ---------------------------------------------------------
# ANOMALY DETECTOR
# ---------------------------------------------------------

class AnomalyDetector:
    """
    Detects data-quality and operational anomalies
    across trips and drivers.
    """

    def __init__(self, config=None):

        self.config = config or AnomalyConfig()

    # -----------------------------------------------------
    # CONFIGURATION
    # -----------------------------------------------------

    def get_thresholds(self):
        """Return the current anomaly thresholds."""

        return {
            "max_trip_duration_minutes":
                self.config.max_trip_duration_minutes,

            "unusual_fare":
                self.config.unusual_fare,

            "high_cancellation_rate":
                self.config.high_cancellation_rate,

            "low_utilization_rate":
                self.config.low_utilization_rate,

            "high_trip_count":
                self.config.high_trip_count,

            "low_rating":
                self.config.low_rating,

            "min_distance_km":
                self.config.min_distance_km
        }

    def update_thresholds(self, **kwargs):
        """
        Update configurable anomaly thresholds.

        Only known configuration fields are updated.
        """

        valid_fields = {
            "max_trip_duration_minutes",
            "unusual_fare",
            "high_cancellation_rate",
            "low_utilization_rate",
            "high_trip_count",
            "low_rating",
            "min_distance_km"
        }

        for key, value in kwargs.items():

            if key in valid_fields:
                setattr(
                    self.config,
                    key,
                    value
                )

    # -----------------------------------------------------
    # TRIP ANOMALIES
    # -----------------------------------------------------

    def detect_trip_anomalies(
        self,
        trips,
        drivers
    ):
        """
        Detect anomalies in trip records.

        Checks:
        - Unknown driver
        - Negative fare
        - Negative distance
        - Zero distance
        - Invalid timestamps
        - Drop time before pickup time
        - Extremely long duration
        - Unusual fare
        """

        anomalies = []

        driver_ids = {
            driver.driver_id
            for driver in drivers
        }

        for trip in trips:

            # -------------------------------------------------
            # Unknown driver
            # -------------------------------------------------

            if trip.driver_id not in driver_ids:

                anomalies.append(
                    AnomalyResult(
                        anomaly_type="Trip",
                        entity_id=trip.trip_id,
                        issue="Unknown driver",
                        severity="High",
                        details=(
                            f"Driver {trip.driver_id} "
                            "does not exist in the driver dataset."
                        ),
                        metadata={
                            "driver_id": trip.driver_id
                        }
                    )
                )

            # -------------------------------------------------
            # Negative fare
            # -------------------------------------------------

            if trip.fare < 0:

                anomalies.append(
                    AnomalyResult(
                        anomaly_type="Trip",
                        entity_id=trip.trip_id,
                        issue="Negative fare",
                        severity="High",
                        details=(
                            f"Fare recorded as "
                            f"{trip.fare}."
                        ),
                        metadata={
                            "fare": trip.fare
                        }
                    )
                )

            # -------------------------------------------------
            # Negative distance
            # -------------------------------------------------

            if trip.distance_km < 0:

                anomalies.append(
                    AnomalyResult(
                        anomaly_type="Trip",
                        entity_id=trip.trip_id,
                        issue="Negative distance",
                        severity="High",
                        details=(
                            f"Distance recorded as "
                            f"{trip.distance_km} km."
                        ),
                        metadata={
                            "distance_km": trip.distance_km
                        }
                    )
                )

            # -------------------------------------------------
            # Zero distance
            # -------------------------------------------------

            elif trip.distance_km == 0:

                anomalies.append(
                    AnomalyResult(
                        anomaly_type="Trip",
                        entity_id=trip.trip_id,
                        issue="Zero distance",
                        severity="Medium",
                        details=(
                            "Distance recorded as 0.0 km."
                        ),
                        metadata={
                            "distance_km": trip.distance_km
                        }
                    )
                )

            # -------------------------------------------------
            # Missing request timestamp
            # -------------------------------------------------

            if trip.request_time is None:

                anomalies.append(
                    AnomalyResult(
                        anomaly_type="Trip",
                        entity_id=trip.trip_id,
                        issue="Invalid timestamp",
                        severity="High",
                        details=(
                            "Trip has no request timestamp."
                        ),
                        metadata={}
                    )
                )

            # -------------------------------------------------
            # Completed trip timestamp validation
            # -------------------------------------------------

            if trip.is_completed():

                if trip.pickup_time is None:

                    anomalies.append(
                        AnomalyResult(
                            anomaly_type="Trip",
                            entity_id=trip.trip_id,
                            issue="Invalid timestamp",
                            severity="High",
                            details=(
                                "Completed trip has no "
                                "pickup timestamp."
                            ),
                            metadata={}
                        )
                    )

                if trip.drop_time is None:

                    anomalies.append(
                        AnomalyResult(
                            anomaly_type="Trip",
                            entity_id=trip.trip_id,
                            issue="Invalid timestamp",
                            severity="High",
                            details=(
                                "Completed trip has no "
                                "drop timestamp."
                            ),
                            metadata={}
                        )
                    )

                # ---------------------------------------------
                # Drop before pickup
                # ---------------------------------------------

                if (
                    trip.pickup_time
                    and trip.drop_time
                    and trip.drop_time < trip.pickup_time
                ):

                    anomalies.append(
                        AnomalyResult(
                            anomaly_type="Trip",
                            entity_id=trip.trip_id,
                            issue="Drop time < pickup time",
                            severity="High",
                            details=(
                                "Drop timestamp occurs "
                                "before pickup timestamp."
                            ),
                            metadata={}
                        )
                    )

                # ---------------------------------------------
                # Extremely long trip
                # ---------------------------------------------

                duration = trip.calculate_duration()

                if (
                    duration is not None
                    and duration
                    > self.config.max_trip_duration_minutes
                ):

                    anomalies.append(
                        AnomalyResult(
                            anomaly_type="Trip",
                            entity_id=trip.trip_id,
                            issue="Extremely long trip duration",
                            severity="Medium",
                            details=(
                                f"Trip duration is "
                                f"{duration:.2f} minutes."
                            ),
                            metadata={
                                "duration_minutes": duration
                            }
                        )
                    )

            # -------------------------------------------------
            # Unusual fare
            # -------------------------------------------------

            if trip.fare > self.config.unusual_fare:

                anomalies.append(
                    AnomalyResult(
                        anomaly_type="Trip",
                        entity_id=trip.trip_id,
                        issue="Unusual fare",
                        severity="Medium",
                        details=(
                            f"Fare recorded as "
                            f"{trip.fare}."
                        ),
                        metadata={
                            "fare": trip.fare
                        }
                    )
                )

        return anomalies

    # -----------------------------------------------------
    # DRIVER ANOMALIES
    # -----------------------------------------------------

    def detect_driver_anomalies(
        self,
        drivers,
        analytics
    ):
        """
        Detect anomalies in driver-level metrics.

        Checks:
        - High cancellation rate
        - Low utilization
        - Unusually high trip count
        - Low rating
        """

        anomalies = []

        # -----------------------------------------------------
        # IMPORTANT:
        # AnalyticsService.get_driver_utilization()
        # returns utilization for ALL drivers.
        #
        # Build a dictionary so each driver can be looked up
        # in O(1) time.
        # -----------------------------------------------------

        utilization_results = (
            analytics.get_driver_utilization()
        )

        utilization_by_driver = {
            item["driver_id"]: item["utilization"]
            for item in utilization_results
        }

        for driver in drivers:

            performance = analytics.get_driver_performance(
                driver.driver_id
            )

            if not performance:
                continue

            cancellation_rate = performance.get(
                "cancellation_rate",
                0
            )

            total_trips = performance.get(
                "total_trips",
                0
            )

            rating = driver.rating

            # -------------------------------------------------
            # High cancellation rate
            # -------------------------------------------------

            if (
                cancellation_rate
                > self.config.high_cancellation_rate
            ):

                anomalies.append(
                    AnomalyResult(
                        anomaly_type="Driver",
                        entity_id=driver.driver_id,
                        issue="High cancellation rate",
                        severity="High",
                        details=(
                            f"Cancellation rate is "
                            f"{cancellation_rate:.2f}%."
                        ),
                        metadata={
                            "cancellation_rate":
                                cancellation_rate
                        }
                    )
                )

            # -------------------------------------------------
            # Low utilization
            # -------------------------------------------------

            utilization = utilization_by_driver.get(
                driver.driver_id
            )

            if utilization is not None:

                if (
                    utilization
                    < self.config.low_utilization_rate
                ):

                    anomalies.append(
                        AnomalyResult(
                            anomaly_type="Driver",
                            entity_id=driver.driver_id,
                            issue="Low utilization",
                            severity="Medium",
                            details=(
                                f"Utilization is "
                                f"{utilization:.2f}%."
                            ),
                            metadata={
                                "utilization":
                                    utilization
                            }
                        )
                    )

            # -------------------------------------------------
            # High trip count
            # -------------------------------------------------

            if (
                total_trips
                > self.config.high_trip_count
            ):

                anomalies.append(
                    AnomalyResult(
                        anomaly_type="Driver",
                        entity_id=driver.driver_id,
                        issue="Unusually high trip count",
                        severity="Medium",
                        details=(
                            f"Driver has "
                            f"{total_trips} total trips."
                        ),
                        metadata={
                            "total_trips": total_trips
                        }
                    )
                )

            # -------------------------------------------------
            # Low rating
            # -------------------------------------------------

            if rating < self.config.low_rating:

                anomalies.append(
                    AnomalyResult(
                        anomaly_type="Driver",
                        entity_id=driver.driver_id,
                        issue="Low rating",
                        severity="Medium",
                        details=(
                            f"Driver rating is "
                            f"{rating}."
                        ),
                        metadata={
                            "rating": rating
                        }
                    )
                )

        return anomalies

    # -----------------------------------------------------
    # ALL ANOMALIES
    # -----------------------------------------------------

    def detect_all(
        self,
        drivers,
        trips,
        analytics
    ):
        """
        Run all anomaly checks and return
        a structured summary.
        """

        trip_anomalies = self.detect_trip_anomalies(
            trips,
            drivers
        )

        driver_anomalies = self.detect_driver_anomalies(
            drivers,
            analytics
        )

        all_anomalies = (
            trip_anomalies
            + driver_anomalies
        )

        severity_counts = {
            "High": 0,
            "Medium": 0
        }

        issue_counts = {}

        for anomaly in all_anomalies:

            severity_counts[
                anomaly.severity
            ] = (
                severity_counts.get(
                    anomaly.severity,
                    0
                )
                + 1
            )

            issue_counts[
                anomaly.issue
            ] = (
                issue_counts.get(
                    anomaly.issue,
                    0
                )
                + 1
            )

        return {
            "total_anomalies": len(all_anomalies),

            "trip_anomalies": len(
                trip_anomalies
            ),

            "driver_anomalies": len(
                driver_anomalies
            ),

            "severity_counts": severity_counts,

            "issue_counts": issue_counts,

            "thresholds": self.get_thresholds(),

            "anomalies": [
                {
                    "anomaly_type":
                        anomaly.anomaly_type,

                    "entity_id":
                        anomaly.entity_id,

                    "issue":
                        anomaly.issue,

                    "severity":
                        anomaly.severity,

                    "details":
                        anomaly.details,

                    "metadata":
                        anomaly.metadata
                }

                for anomaly in all_anomalies
            ]
        }