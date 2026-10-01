
from datetime import datetime


class DataValidator:
    """Validates mobility datasets before analytics processing."""

    REQUIRED_DRIVER_COLUMNS = {
        "driver_id",
        "driver_name",
        "city",
        "vehicle_type",
        "rating",
        "status"
    }

    REQUIRED_TRIP_COLUMNS = {
        "trip_id",
        "driver_id",
        "rider_id",
        "city",
        "pickup_zone",
        "drop_zone",
        "request_time",
        "pickup_time",
        "drop_time",
        "distance_km",
        "fare",
        "status",
        "cancellation_reason"
    }

    REQUIRED_ACTIVITY_COLUMNS = {
        "driver_id",
        "timestamp",
        "status"
    }

    def __init__(self):
        self.errors = []
        self.warnings = []

    def reset(self):
        """Clear previous validation results."""

        self.errors = []
        self.warnings = []

    def validate_required_columns(
        self,
        columns,
        required_columns,
        dataset_name
    ):
        """
        Check whether all required columns are present.

        This method is intended for CSV/header-level validation.
        """

        missing_columns = (
            required_columns - set(columns)
        )

        for column in sorted(missing_columns):

            self.errors.append(
                f"{dataset_name}: Missing required column "
                f"'{column}'."
            )

    # =========================================================
    # DRIVER VALIDATION
    # =========================================================

    def validate_drivers(self, drivers):
        """Validate Driver objects."""

        seen_driver_ids = set()

        for driver in drivers:

            # -------------------------------------------------
            # Missing driver ID
            # -------------------------------------------------

            if not driver.driver_id:

                self.errors.append(
                    "Drivers: Missing driver_id."
                )

            else:

                # ---------------------------------------------
                # Duplicate driver ID
                # ---------------------------------------------

                if driver.driver_id in seen_driver_ids:

                    self.errors.append(
                        f"Drivers: Duplicate driver_id "
                        f"'{driver.driver_id}'."
                    )

                seen_driver_ids.add(
                    driver.driver_id
                )

            # -------------------------------------------------
            # Missing driver name
            # -------------------------------------------------

            if not driver.driver_name:

                self.errors.append(
                    f"Drivers: Missing driver_name for "
                    f"{driver.driver_id}."
                )

            # -------------------------------------------------
            # Rating validation
            # -------------------------------------------------

            if driver.rating < 0 or driver.rating > 5:

                self.errors.append(
                    f"Drivers: Invalid rating for "
                    f"{driver.driver_id}: "
                    f"{driver.rating}."
                )

            # -------------------------------------------------
            # Status validation
            # -------------------------------------------------

            if driver.status.lower() not in {
                "active",
                "inactive"
            }:

                self.errors.append(
                    f"Drivers: Invalid status for "
                    f"{driver.driver_id}: "
                    f"{driver.status}."
                )

    # =========================================================
    # TRIP VALIDATION
    # =========================================================

    def validate_trips(
        self,
        trips,
        drivers
    ):
        """Validate Trip objects."""

        driver_ids = {
            driver.driver_id
            for driver in drivers
        }

        seen_trip_ids = set()

        for trip in trips:

            # -------------------------------------------------
            # Duplicate trip ID
            # -------------------------------------------------

            if trip.trip_id in seen_trip_ids:

                self.errors.append(
                    f"Trips: Duplicate trip_id "
                    f"'{trip.trip_id}'."
                )

            seen_trip_ids.add(
                trip.trip_id
            )

            # -------------------------------------------------
            # Check whether driver exists
            # -------------------------------------------------

            if trip.driver_id not in driver_ids:

                self.errors.append(
                    f"Trips: Unknown driver_id "
                    f"'{trip.driver_id}' "
                    f"for trip {trip.trip_id}."
                )

            # -------------------------------------------------
            # Fare validation
            # -------------------------------------------------

            if trip.fare < 0:

                self.errors.append(
                    f"Trips: Negative fare for "
                    f"{trip.trip_id}: "
                    f"{trip.fare}."
                )

            # -------------------------------------------------
            # Distance validation
            # -------------------------------------------------

            if trip.distance_km < 0:

                self.errors.append(
                    f"Trips: Negative distance for "
                    f"{trip.trip_id}: "
                    f"{trip.distance_km}."
                )

            # -------------------------------------------------
            # Request timestamp
            # -------------------------------------------------

            if trip.request_time is None:

                self.errors.append(
                    f"Trips: Missing request_time for "
                    f"{trip.trip_id}."
                )

            # -------------------------------------------------
            # Completed trip validation
            # -------------------------------------------------

            if trip.is_completed():

                if trip.pickup_time is None:

                    self.errors.append(
                        f"Trips: Missing pickup_time "
                        f"for completed trip "
                        f"{trip.trip_id}."
                    )

                if trip.drop_time is None:

                    self.errors.append(
                        f"Trips: Missing drop_time "
                        f"for completed trip "
                        f"{trip.trip_id}."
                    )

                # ---------------------------------------------
                # Validate trip duration
                # ---------------------------------------------

                if (
                    trip.pickup_time
                    and trip.drop_time
                ):

                    if (
                        trip.drop_time
                        < trip.pickup_time
                    ):

                        self.errors.append(
                            f"Trips: Invalid trip duration "
                            f"for {trip.trip_id}: "
                            f"drop_time occurs before "
                            f"pickup_time."
                        )

            # -------------------------------------------------
            # Cancelled trip validation
            # -------------------------------------------------

            if trip.is_cancelled():

                if not trip.cancellation_reason:

                    self.warnings.append(
                        f"Trips: Missing cancellation "
                        f"reason for cancelled trip "
                        f"{trip.trip_id}."
                    )

    # =========================================================
    # DRIVER ACTIVITY VALIDATION
    # =========================================================

    def validate_activity(self, activity):
        """Validate driver activity records."""

        valid_statuses = {
            "online",
            "busy",
            "idle",
            "offline"
        }

        seen_activity_records = set()

        for record in activity:

            driver_id = record.get(
                "driver_id"
            )

            timestamp = record.get(
                "timestamp"
            )

            status = record.get(
                "status"
            )

            # -------------------------------------------------
            # Duplicate activity record
            # -------------------------------------------------

            activity_key = (
                driver_id,
                timestamp
            )

            if activity_key in seen_activity_records:

                self.errors.append(
                    "Driver Activity: Duplicate record "
                    f"for driver {driver_id} "
                    f"at timestamp {timestamp}."
                )

            seen_activity_records.add(
                activity_key
            )

            # -------------------------------------------------
            # Driver ID
            # -------------------------------------------------

            if not driver_id:

                self.errors.append(
                    "Driver Activity: Missing driver_id."
                )

            # -------------------------------------------------
            # Timestamp
            # -------------------------------------------------

            if not timestamp:

                self.errors.append(
                    "Driver Activity: Missing timestamp "
                    f"for driver {driver_id}."
                )

            else:

                try:

                    datetime.strptime(
                        timestamp,
                        "%Y-%m-%d %H:%M:%S"
                    )

                except (
                    TypeError,
                    ValueError
                ):

                    self.errors.append(
                        "Driver Activity: Invalid timestamp "
                        f"'{timestamp}' for driver "
                        f"{driver_id}."
                    )

            # -------------------------------------------------
            # Activity status
            # -------------------------------------------------

            if not status:

                self.errors.append(
                    "Driver Activity: Missing status "
                    f"for driver {driver_id}."
                )

            elif status.lower() not in valid_statuses:

                self.errors.append(
                    "Driver Activity: Invalid status "
                    f"'{status}' for driver "
                    f"{driver_id}."
                )

    # =========================================================
    # COMPLETE VALIDATION
    # =========================================================

    def validate_all(
        self,
        drivers,
        trips,
        activity
    ):
        """
        Run all object-level validation checks.

        Required-column validation should be performed
        before objects are created, using
        validate_required_columns().

        Returns a dictionary containing errors and warnings.
        """

        self.reset()

        self.validate_drivers(
            drivers
        )

        self.validate_trips(
            trips,
            drivers
        )

        self.validate_activity(
            activity
        )

        return {
            "valid": len(self.errors) == 0,
            "errors": self.errors,
            "warnings": self.warnings,
            "error_count": len(self.errors),
            "warning_count": len(self.warnings)
        }
