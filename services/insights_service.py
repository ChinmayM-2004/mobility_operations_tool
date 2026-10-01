
class InsightsEngine:
    """
    Converts analytics and anomaly results into concise,
    dynamically generated operational insights.
    """

    def __init__(self, analytics, anomaly_results):
        self.analytics = analytics
        self.anomaly_results = anomaly_results

    def generate_insights(self):
        """
        Generate operational insights dynamically.

        Every insight is calculated from the current dataset.
        """

        insights = []

        self._add_peak_demand_insight(insights)
        self._add_cancellation_insight(insights)
        self._add_zone_cancellation_insight(insights)
        self._add_low_utilization_insight(insights)
        self._add_anomaly_insight(insights)
        self._add_revenue_insight(insights)

        if not insights:
            insights.append(
                {
                    "category": "General",
                    "severity": "Info",
                    "message": (
                        "No significant operational insights "
                        "were detected from the current dataset."
                    )
                }
            )

        for index, insight in enumerate(
            insights,
            start=1
        ):
            insight["number"] = index

        return insights

    # ------------------------------------------------------------------
    # Peak demand
    # ------------------------------------------------------------------

    def _add_peak_demand_insight(self, insights):

        try:
            peak_demand = self.analytics.get_peak_demand(
                top_k=1
            )
        except Exception:
            peak_demand = []

        if not peak_demand:
            return

        peak = peak_demand[0]

        hour_label = peak.get(
            "hour_label",
            "Peak period"
        )

        requests = peak.get(
            "requests",
            0
        )

        insights.append(
            {
                "category": "Demand",
                "severity": "Info",
                "message": (
                    f"{hour_label} has the highest observed "
                    f"trip demand with {requests} requests."
                )
            }
        )

    # ------------------------------------------------------------------
    # Cancellation category
    # ------------------------------------------------------------------

    def _add_cancellation_insight(self, insights):

        cancellation_data = (
            self.analytics
            .get_cancellation_intelligence()
        )

        by_reason = cancellation_data.get(
            "by_reason",
            []
        )

        if not by_reason:
            return

        top_reason = by_reason[0]

        reason = top_reason.get(
            "reason",
            "Unknown"
        )

        percentage = top_reason.get(
            "percentage",
            0
        )

        insights.append(
            {
                "category": "Cancellation",
                "severity": "Warning",
                "message": (
                    f"{reason} represents the largest "
                    f"cancellation category at "
                    f"{percentage:.2f}% of cancellations."
                )
            }
        )

    # ------------------------------------------------------------------
    # Zone cancellation
    # ------------------------------------------------------------------

    def _add_zone_cancellation_insight(self, insights):

        cancellation_data = (
            self.analytics
            .get_cancellation_intelligence()
        )

        zones = cancellation_data.get(
            "by_zone",
            []
        )

        if not zones:
            return

        valid_zones = [
            zone
            for zone in zones
            if zone.get("total_trips", 0) > 0
        ]

        if not valid_zones:
            return

        top_zone = max(
            valid_zones,
            key=lambda item: item.get(
                "cancellation_rate",
                0
            )
        )

        insights.append(
            {
                "category": "Zone",
                "severity": "Warning",
                "message": (
                    f"{top_zone.get('city', 'Unknown')} - "
                    f"{top_zone.get('zone', 'Unknown')} has the "
                    f"highest cancellation rate at "
                    f"{top_zone.get('cancellation_rate', 0):.2f}%."
                )
            }
        )

    # ------------------------------------------------------------------
    # Low utilization
    # ------------------------------------------------------------------

    def _add_low_utilization_insight(self, insights):

        try:
            utilization_data = (
                self.analytics
                .get_top_utilized_drivers(
                    len(self.analytics.drivers)
                )
            )
        except Exception:
            utilization_data = []

        if not utilization_data:
            return

        threshold = 50.0

        low_utilized_count = sum(
            1
            for driver in utilization_data
            if driver.get("utilization", 0) < threshold
        )

        if low_utilized_count == 0:
            return

        insights.append(
            {
                "category": "Utilization",
                "severity": "Warning",
                "message": (
                    f"{low_utilized_count} drivers have "
                    f"utilization below {threshold:.0f}%."
                )
            }
        )

    # ------------------------------------------------------------------
    # Anomalies
    # ------------------------------------------------------------------

    def _add_anomaly_insight(self, insights):

        total_anomalies = (
            self.anomaly_results.get(
                "total_anomalies",
                0
            )
        )

        if total_anomalies == 0:
            return

        insights.append(
            {
                "category": "Anomaly",
                "severity": "High",
                "message": (
                    f"{total_anomalies} trips or drivers "
                    f"have been flagged for data or "
                    f"operational anomalies."
                )
            }
        )

    # ------------------------------------------------------------------
    # Revenue
    # ------------------------------------------------------------------

    def _add_revenue_insight(self, insights):

        try:
            revenue_drivers = (
                self.analytics
                .get_driver_rankings(
                    "revenue",
                    1
                )
            )
        except Exception:
            revenue_drivers = []

        if not revenue_drivers:
            return

        driver = revenue_drivers[0]

        driver_name = driver.get(
            "driver_name",
            driver.get("driver_id", "Unknown driver")
        )

        revenue = driver.get(
            "revenue",
            0
        )

        insights.append(
            {
                "category": "Revenue",
                "severity": "Info",
                "message": (
                    f"{driver_name} currently has the highest "
                    f"recorded driver revenue at "
                    f"₹{revenue:,.2f}."
                )
            }
        )

