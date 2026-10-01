
import heapq
from collections import defaultdict
from datetime import datetime


class AnalyticsService:
    """
    Core analytics engine for the mobility marketplace.

    Handles:
    - Dashboard KPIs
    - Driver analytics
    - Trip analytics
    - Zone analytics
    - Top-K analysis using heaps
    - Consecutive-trip analysis
    - Idle-time detection
    - Peak-demand analysis
    - Driver utilization
    - Cancellation intelligence
    """

    def __init__(self, data):
        self.drivers = data["drivers"]
        self.trips = data["trips"]
        self.zones = data["zones"]
        self.driver_activity = data["driver_activity"]

        self._build_indexes()

    # =========================================================
    # DICTIONARY INDEXES
    # =========================================================

    def _build_indexes(self):
        """Create dictionary indexes for faster searching."""

        self.driver_index = {
            driver.driver_id: driver
            for driver in self.drivers
        }

        self.trip_index = {
            trip.trip_id: trip
            for trip in self.trips
        }

        self.zone_index = {
            (zone.city, zone.zone_name): zone
            for zone in self.zones
        }

        self.trips_by_driver = defaultdict(list)

        for trip in self.trips:
            self.trips_by_driver[trip.driver_id].append(trip)

        self.trips_by_city = defaultdict(list)

        for trip in self.trips:
            self.trips_by_city[trip.city].append(trip)

        self.trips_by_zone = defaultdict(list)

        for trip in self.trips:
            key = (
                trip.city,
                trip.pickup_zone
            )

            self.trips_by_zone[key].append(trip)

        self.activity_by_driver = defaultdict(list)

        for record in self.driver_activity:
            self.activity_by_driver[
                record["driver_id"]
            ].append(record)

    # =========================================================
    # SEARCH
    # =========================================================

    def get_driver(self, driver_id):
        """Return a driver by driver ID."""

        return self.driver_index.get(driver_id)

    def get_trip(self, trip_id):
        """Return a trip by trip ID."""

        return self.trip_index.get(trip_id)

    def get_zone(self, city, zone_name):
        """Return a zone by city and zone name."""

        return self.zone_index.get(
            (city, zone_name)
        )

    # =========================================================
    # DASHBOARD KPIs
    # =========================================================

    def get_dashboard_kpis(self):
        """Calculate the main marketplace KPIs."""

        total_drivers = len(self.drivers)

        active_drivers = sum(
            1
            for driver in self.drivers
            if driver.is_active()
        )

        total_trips = len(self.trips)

        completed_trips = sum(
            1
            for trip in self.trips
            if trip.is_completed()
        )

        cancelled_trips = sum(
            1
            for trip in self.trips
            if trip.is_cancelled()
        )

        riders = {
            trip.rider_id
            for trip in self.trips
            if trip.rider_id
        }

        total_revenue = sum(
            trip.fare
            for trip in self.trips
            if trip.is_completed()
        )

        completed_fares = [
            trip.fare
            for trip in self.trips
            if trip.is_completed()
        ]

        completed_distances = [
            trip.distance_km
            for trip in self.trips
            if trip.is_completed()
        ]

        durations = [
            trip.calculate_duration()
            for trip in self.trips
            if (
                trip.is_completed()
                and trip.calculate_duration() is not None
                and trip.calculate_duration() >= 0
            )
        ]

        average_fare = (
            sum(completed_fares) / len(completed_fares)
            if completed_fares
            else 0
        )

        average_distance = (
            sum(completed_distances)
            / len(completed_distances)
            if completed_distances
            else 0
        )

        average_duration = (
            sum(durations) / len(durations)
            if durations
            else 0
        )

        completion_rate = (
            completed_trips / total_trips * 100
            if total_trips
            else 0
        )

        cancellation_rate = (
            cancelled_trips / total_trips * 100
            if total_trips
            else 0
        )

        return {
            "total_drivers": total_drivers,
            "active_drivers": active_drivers,
            "total_riders": len(riders),
            "total_trips": total_trips,
            "completed_trips": completed_trips,
            "cancelled_trips": cancelled_trips,
            "completion_rate": completion_rate,
            "cancellation_rate": cancellation_rate,
            "total_revenue": total_revenue,
            "average_fare": average_fare,
            "average_distance": average_distance,
            "average_trip_duration": average_duration
        }

    # =========================================================
    # TRIP ANALYTICS
    # =========================================================

    def get_trip_status_counts(self):
        """Return trip counts grouped by status."""

        status_counts = defaultdict(int)

        for trip in self.trips:
            status_counts[trip.status] += 1

        return dict(status_counts)

    def get_cancellation_reasons(self):
        """Return cancellation frequency by reason."""

        reason_counts = defaultdict(int)

        for trip in self.trips:
            if trip.is_cancelled():

                reason = (
                    trip.cancellation_reason
                    or "Unknown"
                )

                reason_counts[reason] += 1

        return dict(
            sorted(
                reason_counts.items(),
                key=lambda item: item[1],
                reverse=True
            )
        )

    def get_trip_revenue_by_city(self):
        """Return completed-trip revenue grouped by city."""

        revenue_by_city = defaultdict(float)

        for trip in self.trips:

            if trip.is_completed():
                revenue_by_city[trip.city] += trip.fare

        return dict(
            sorted(
                revenue_by_city.items(),
                key=lambda item: item[1],
                reverse=True
            )
        )

    # =========================================================
    # DRIVER ANALYTICS
    # =========================================================

    def get_driver_performance(self, driver_id):
        """Return detailed performance metrics for one driver."""

        driver = self.get_driver(driver_id)

        if driver is None:
            return None

        driver_trips = self.trips_by_driver.get(
            driver_id,
            []
        )

        completed_trips = [
            trip
            for trip in driver_trips
            if trip.is_completed()
        ]

        cancelled_trips = [
            trip
            for trip in driver_trips
            if trip.is_cancelled()
        ]

        revenue = sum(
            trip.fare
            for trip in completed_trips
        )

        cancellation_rate = (
            len(cancelled_trips)
            / len(driver_trips)
            * 100
            if driver_trips
            else 0
        )

        average_fare = (
            sum(
                trip.fare
                for trip in completed_trips
            )
            / len(completed_trips)
            if completed_trips
            else 0
        )

        average_distance = (
            sum(
                trip.distance_km
                for trip in completed_trips
            )
            / len(completed_trips)
            if completed_trips
            else 0
        )

        return {
            "driver": driver,
            "total_trips": len(driver_trips),
            "completed_trips": len(completed_trips),
            "cancelled_trips": len(cancelled_trips),
            "cancellation_rate": cancellation_rate,
            "revenue": revenue,
            "average_fare": average_fare,
            "average_distance": average_distance
        }

    def _build_driver_metrics(self):
        """Build reusable metrics for every driver."""

        results = []

        for driver in self.drivers:

            performance = self.get_driver_performance(
                driver.driver_id
            )

            if performance is None:
                continue

            results.append({
                "driver_id": driver.driver_id,
                "driver_name": driver.driver_name,
                "city": driver.city,
                "status": driver.status,
                "completed_trips": (
                    performance["completed_trips"]
                ),
                "total_trips": (
                    performance["total_trips"]
                ),
                "cancelled_trips": (
                    performance["cancelled_trips"]
                ),
                "revenue": performance["revenue"],
                "cancellation_rate": (
                    performance["cancellation_rate"]
                )
            })

        return results

    # =========================================================
    # TOP-K DRIVER ANALYSIS
    # =========================================================

    def get_driver_rankings(
        self,
        metric,
        top_k=10
    ):
        """
        Return Top-K drivers using heapq.

        Supported metrics:
        - completed_trips
        - revenue
        - cancellation_rate
        """

        results = self._build_driver_metrics()

        if metric == "completed_trips":

            return heapq.nlargest(
                top_k,
                results,
                key=lambda item: item["completed_trips"]
            )

        if metric == "revenue":

            return heapq.nlargest(
                top_k,
                results,
                key=lambda item: item["revenue"]
            )

        if metric == "cancellation_rate":

            return heapq.nlargest(
                top_k,
                results,
                key=lambda item: item["cancellation_rate"]
            )

        raise ValueError(
            f"Unsupported driver ranking metric: {metric}"
        )

    # =========================================================
    # ZONE ANALYTICS
    # =========================================================

    def get_zone_performance(
        self,
        city,
        zone_name
    ):
        """Return demand and performance metrics for a zone."""

        zone = self.get_zone(
            city,
            zone_name
        )

        if zone is None:
            return None

        pickup_trips = self.trips_by_zone.get(
            (city, zone_name),
            []
        )

        completed_trips = [
            trip
            for trip in pickup_trips
            if trip.is_completed()
        ]

        cancelled_trips = [
            trip
            for trip in pickup_trips
            if trip.is_cancelled()
        ]

        revenue = sum(
            trip.fare
            for trip in completed_trips
        )

        average_fare = (
            revenue / len(completed_trips)
            if completed_trips
            else 0
        )

        completion_rate = (
            len(completed_trips)
            / len(pickup_trips)
            * 100
            if pickup_trips
            else 0
        )

        cancellation_rate = (
            len(cancelled_trips)
            / len(pickup_trips)
            * 100
            if pickup_trips
            else 0
        )

        return {
            "zone": zone,
            "requests": len(pickup_trips),
            "completed_trips": len(completed_trips),
            "cancelled_trips": len(cancelled_trips),
            "completion_rate": completion_rate,
            "cancellation_rate": cancellation_rate,
            "revenue": revenue,
            "average_fare": average_fare
        }

    def get_zone_demand(self):
        """Return pickup demand frequency by city and zone."""

        demand = defaultdict(int)

        for trip in self.trips:

            if not trip.pickup_zone:
                continue

            key = (
                trip.city,
                trip.pickup_zone
            )

            demand[key] += 1

        results = []

        for (
            city,
            zone
        ), count in demand.items():

            results.append({
                "city": city,
                "zone": zone,
                "requests": count
            })

        results.sort(
            key=lambda item: item["requests"],
            reverse=True
        )

        return results

    # =========================================================
    # TOP-K ZONE ANALYSIS
    # =========================================================

    def get_top_k_zones(self, top_k=10):
        """Return the highest-demand zones using a heap."""

        zones = self.get_zone_demand()

        return heapq.nlargest(
            top_k,
            zones,
            key=lambda item: item["requests"]
        )

    # =========================================================
    # CONSECUTIVE TRIP ANALYSIS
    # =========================================================

    def get_consecutive_trip_analysis(
        self,
        driver_id=None,
        max_gap_minutes=30
    ):
        """
        Find sequences of completed trips where the next trip
        starts within max_gap_minutes after the previous trip ends.
        """

        if driver_id:
            driver_ids = [driver_id]

        else:
            driver_ids = [
                driver.driver_id
                for driver in self.drivers
            ]

        sequences = []

        for current_driver_id in driver_ids:

            trips = [
                trip
                for trip in self.trips_by_driver.get(
                    current_driver_id,
                    []
                )
                if (
                    trip.is_completed()
                    and trip.pickup_time
                    and trip.drop_time
                )
            ]

            trips.sort(
                key=lambda trip: trip.pickup_time
            )

            if not trips:
                continue

            current_sequence = [trips[0]]

            for trip in trips[1:]:

                previous_trip = current_sequence[-1]

                gap_minutes = (
                    trip.pickup_time
                    - previous_trip.drop_time
                ).total_seconds() / 60

                if 0 <= gap_minutes <= max_gap_minutes:

                    current_sequence.append(trip)

                else:

                    if len(current_sequence) >= 2:

                        sequences.append(
                            self._format_trip_sequence(
                                current_driver_id,
                                current_sequence
                            )
                        )

                    current_sequence = [trip]

            if len(current_sequence) >= 2:

                sequences.append(
                    self._format_trip_sequence(
                        current_driver_id,
                        current_sequence
                    )
                )

        sequences.sort(
            key=lambda item: (
                item["sequence_length"],
                -item["total_turnaround_minutes"]
            ),
            reverse=True
        )

        return sequences

    def _format_trip_sequence(
        self,
        driver_id,
        trips
    ):
        """Format one consecutive-trip sequence."""

        first_trip = trips[0]
        last_trip = trips[-1]

        turnaround_minutes = 0

        for index in range(
            1,
            len(trips)
        ):

            gap = (
                trips[index].pickup_time
                - trips[index - 1].drop_time
            ).total_seconds() / 60

            turnaround_minutes += gap

        driver = self.driver_index.get(
            driver_id
        )

        return {
            "driver_id": driver_id,
            "driver_name": (
                driver.driver_name
                if driver
                else "Unknown"
            ),
            "sequence_start_trip": (
                first_trip.trip_id
            ),
            "sequence_end_trip": (
                last_trip.trip_id
            ),
            "sequence_length": len(trips),
            "start_time": first_trip.pickup_time,
            "end_time": last_trip.drop_time,
            "total_turnaround_minutes": (
                turnaround_minutes
            ),
            "trip_ids": [
                trip.trip_id
                for trip in trips
            ]
        }

    # =========================================================
    # IDLE-TIME DETECTION
    # =========================================================

    @staticmethod
    def _parse_activity_timestamp(value):
        """Convert an activity timestamp into datetime."""

        if isinstance(value, datetime):
            return value

        return datetime.strptime(
            value,
            "%Y-%m-%d %H:%M:%S"
        )

    def get_idle_time_analysis(
        self,
        min_idle_minutes=30
    ):
        """
        Detect idle periods from driver activity records.

        An idle period lasts from an 'idle' activity record
        until the next activity record for that driver.
        """

        idle_periods = []

        for driver_id, records in (
            self.activity_by_driver.items()
        ):

            parsed_records = []

            for record in records:

                try:

                    timestamp = (
                        self._parse_activity_timestamp(
                            record["timestamp"]
                        )
                    )

                    parsed_records.append({
                        "driver_id": driver_id,
                        "timestamp": timestamp,
                        "status": record["status"]
                    })

                except (
                    TypeError,
                    ValueError
                ):

                    continue

            parsed_records.sort(
                key=lambda item: item["timestamp"]
            )

            for index in range(
                len(parsed_records) - 1
            ):

                current = parsed_records[index]
                next_record = parsed_records[
                    index + 1
                ]

                if current["status"].lower() != "idle":
                    continue

                duration_minutes = (
                    next_record["timestamp"]
                    - current["timestamp"]
                ).total_seconds() / 60

                if duration_minutes >= min_idle_minutes:

                    driver = self.driver_index.get(
                        driver_id
                    )

                    idle_periods.append({
                        "driver_id": driver_id,
                        "driver_name": (
                            driver.driver_name
                            if driver
                            else "Unknown"
                        ),
                        "start_time": (
                            current["timestamp"]
                        ),
                        "end_time": (
                            next_record["timestamp"]
                        ),
                        "idle_minutes": duration_minutes
                    })

        idle_periods.sort(
            key=lambda item: item["idle_minutes"],
            reverse=True
        )

        return idle_periods

    def get_driver_idle_summary(
        self,
        min_idle_minutes=30
    ):
        """Aggregate idle time by driver."""

        idle_periods = self.get_idle_time_analysis(
            min_idle_minutes
        )

        summary = defaultdict(
            lambda: {
                "idle_periods": 0,
                "total_idle_minutes": 0
            }
        )

        for period in idle_periods:

            driver_id = period["driver_id"]

            summary[driver_id]["idle_periods"] += 1

            summary[driver_id][
                "total_idle_minutes"
            ] += period["idle_minutes"]

        results = []

        for driver_id, values in summary.items():

            driver = self.driver_index.get(
                driver_id
            )

            results.append({
                "driver_id": driver_id,
                "driver_name": (
                    driver.driver_name
                    if driver
                    else "Unknown"
                ),
                "city": (
                    driver.city
                    if driver
                    else "Unknown"
                ),
                "idle_periods": (
                    values["idle_periods"]
                ),
                "total_idle_minutes": (
                    values["total_idle_minutes"]
                )
            })

        results.sort(
            key=lambda item: item["total_idle_minutes"],
            reverse=True
        )

        return results

    # =========================================================
    # PEAK DEMAND
    # =========================================================

    def get_peak_demand(
        self,
        top_k=10,
        city=None
    ):
        """
        Analyze demand by hour of day.

        If city is provided, only that city's trips
        are included.
        """

        hourly_demand = defaultdict(int)

        for trip in self.trips:

            if not trip.request_time:
                continue

            if city and trip.city != city:
                continue

            hour = trip.request_time.hour

            hourly_demand[hour] += 1

        results = []

        for hour, requests in hourly_demand.items():

            results.append({
                "hour": hour,
                "hour_label": (
                    f"{hour:02d}:00 - "
                    f"{(hour + 1) % 24:02d}:00"
                ),
                "requests": requests
            })

        return heapq.nlargest(
            top_k,
            results,
            key=lambda item: item["requests"]
        )

    def get_peak_demand_by_city(
        self,
        top_k=5
    ):
        """Return peak demand hours for each city."""

        cities = sorted({
            trip.city
            for trip in self.trips
            if trip.city
        })

        results = []

        for city in cities:

            results.append({
                "city": city,
                "peak_hours": self.get_peak_demand(
                    top_k=top_k,
                    city=city
                )
            })

        return results

    # =========================================================
    # DRIVER UTILIZATION
    # =========================================================

    def get_driver_utilization(self):
        """
        Calculate driver utilization.

        Utilization =
            Busy Time / Online Time * 100

        Busy and idle intervals are calculated from
        consecutive driver activity records.
        """

        results = []

        for driver in self.drivers:

            records = []

            for record in self.activity_by_driver.get(
                driver.driver_id,
                []
            ):

                try:

                    records.append({
                        "timestamp": (
                            self._parse_activity_timestamp(
                                record["timestamp"]
                            )
                        ),
                        "status": record[
                            "status"
                        ].lower()
                    })

                except (
                    TypeError,
                    ValueError
                ):

                    continue

            records.sort(
                key=lambda item: item["timestamp"]
            )

            busy_minutes = 0
            online_minutes = 0

            for index in range(
                len(records) - 1
            ):

                current = records[index]
                next_record = records[
                    index + 1
                ]

                duration_minutes = (
                    next_record["timestamp"]
                    - current["timestamp"]
                ).total_seconds() / 60

                if duration_minutes < 0:
                    continue

                if current["status"] == "busy":

                    busy_minutes += duration_minutes
                    online_minutes += duration_minutes

                elif current["status"] == "idle":

                    online_minutes += duration_minutes

                elif current["status"] == "online":

                    online_minutes += duration_minutes

            utilization = (
                busy_minutes
                / online_minutes
                * 100
                if online_minutes
                else 0
            )

            results.append({
                "driver_id": driver.driver_id,
                "driver_name": driver.driver_name,
                "city": driver.city,
                "busy_minutes": busy_minutes,
                "online_minutes": online_minutes,
                "utilization": utilization
            })

        results.sort(
            key=lambda item: item["utilization"],
            reverse=True
        )

        return results

    def get_top_utilized_drivers(
        self,
        top_k=10
    ):
        """Return Top-K drivers by utilization."""

        utilization = self.get_driver_utilization()

        return heapq.nlargest(
            top_k,
            utilization,
            key=lambda item: item["utilization"]
        )

    # =========================================================
    # CANCELLATION INTELLIGENCE
    # =========================================================

    def get_cancellation_intelligence(self):
        """
        Analyze cancellations by:
        - reason
        - city
        - zone
        - driver
        """

        total_trips = len(self.trips)

        cancelled_trips = [
            trip
            for trip in self.trips
            if trip.is_cancelled()
        ]

        overall_rate = (
            len(cancelled_trips)
            / total_trips
            * 100
            if total_trips
            else 0
        )

        # -----------------------------------------------------
        # Cancellation by reason
        # -----------------------------------------------------

        reason_counts = defaultdict(int)

        for trip in cancelled_trips:

            reason = (
                trip.cancellation_reason
                or "Unknown"
            )

            reason_counts[reason] += 1

        reason_analysis = []

        for reason, count in reason_counts.items():

            percentage = (
                count
                / len(cancelled_trips)
                * 100
                if cancelled_trips
                else 0
            )

            reason_analysis.append({
                "reason": reason,
                "cancelled_trips": count,
                "percentage": percentage
            })

        reason_analysis.sort(
            key=lambda item: item["cancelled_trips"],
            reverse=True
        )

        # -----------------------------------------------------
        # Cancellation by city
        # -----------------------------------------------------

        city_totals = defaultdict(int)
        city_cancelled = defaultdict(int)

        for trip in self.trips:

            city_totals[trip.city] += 1

            if trip.is_cancelled():
                city_cancelled[trip.city] += 1

        city_analysis = []

        for city, total in city_totals.items():

            cancelled = city_cancelled[city]

            rate = (
                cancelled
                / total
                * 100
                if total
                else 0
            )

            city_analysis.append({
                "city": city,
                "total_trips": total,
                "cancelled_trips": cancelled,
                "cancellation_rate": rate
            })

        city_analysis.sort(
            key=lambda item: item["cancellation_rate"],
            reverse=True
        )

        # -----------------------------------------------------
        # Cancellation by zone
        # -----------------------------------------------------

        zone_totals = defaultdict(int)
        zone_cancelled = defaultdict(int)

        for trip in self.trips:

            key = (
                trip.city,
                trip.pickup_zone
            )

            zone_totals[key] += 1

            if trip.is_cancelled():
                zone_cancelled[key] += 1

        zone_analysis = []

        for (
            city,
            zone
        ), total in zone_totals.items():

            cancelled = zone_cancelled[
                (city, zone)
            ]

            rate = (
                cancelled
                / total
                * 100
                if total
                else 0
            )

            zone_analysis.append({
                "city": city,
                "zone": zone,
                "total_trips": total,
                "cancelled_trips": cancelled,
                "cancellation_rate": rate
            })

        zone_analysis.sort(
            key=lambda item: item["cancellation_rate"],
            reverse=True
        )

        # -----------------------------------------------------
        # Cancellation by driver
        # -----------------------------------------------------

        driver_analysis = []

        for driver in self.drivers:

            driver_trips = self.trips_by_driver.get(
                driver.driver_id,
                []
            )

            cancelled = sum(
                1
                for trip in driver_trips
                if trip.is_cancelled()
            )

            total = len(driver_trips)

            rate = (
                cancelled
                / total
                * 100
                if total
                else 0
            )

            driver_analysis.append({
                "driver_id": driver.driver_id,
                "driver_name": driver.driver_name,
                "city": driver.city,
                "total_trips": total,
                "cancelled_trips": cancelled,
                "cancellation_rate": rate
            })

        driver_analysis.sort(
            key=lambda item: (
                item["cancellation_rate"],
                item["cancelled_trips"]
            ),
            reverse=True
        )

        return {
            "total_trips": total_trips,
            "cancelled_trips": len(cancelled_trips),
            "overall_rate": overall_rate,
            "by_reason": reason_analysis,
            "by_city": city_analysis,
            "by_zone": zone_analysis,
            "by_driver": driver_analysis
        }

    # =========================================================
    # FREQUENCY ANALYSIS
    # =========================================================

    def get_driver_trip_frequency(self):
        """Return total trips handled by each driver."""

        frequency = defaultdict(int)

        for trip in self.trips:
            frequency[trip.driver_id] += 1

        return dict(
            sorted(
                frequency.items(),
                key=lambda item: item[1],
                reverse=True
            )
        )

    def get_rider_trip_frequency(self):
        """Return total trips requested by each rider."""

        frequency = defaultdict(int)

        for trip in self.trips:
            frequency[trip.rider_id] += 1

        return dict(
            sorted(
                frequency.items(),
                key=lambda item: item[1],
                reverse=True
            )
        )

