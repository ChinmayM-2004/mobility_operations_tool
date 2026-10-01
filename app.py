from pathlib import Path

from flask import Flask, render_template, request

from services.data_loader import DataLoader
from services.validation_service import DataValidator
from services.analytics_service import AnalyticsService
from services.anomaly_service import AnomalyConfig, AnomalyDetector
from services.insights_service import InsightsEngine


app = Flask(__name__)


# ---------------------------------------------------------
# PROJECT PATHS
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

DRIVERS_FILE = DATA_DIR / "drivers.csv"
TRIPS_FILE = DATA_DIR / "trips.csv"
ACTIVITY_FILE = DATA_DIR / "driver_activity.csv"

UPLOAD_DIR = DATA_DIR / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

ALLOWED_EXTENSIONS = {".csv"}


# ---------------------------------------------------------
# ACTIVE DATASET
# ---------------------------------------------------------

ACTIVE_DRIVERS_FILE = DRIVERS_FILE
ACTIVE_TRIPS_FILE = TRIPS_FILE
ACTIVE_ACTIVITY_FILE = ACTIVITY_FILE

ACTIVE_DATA_SOURCE = "Sample Data"


# ---------------------------------------------------------
# DAY 4 — ANOMALY CONFIGURATION
# ---------------------------------------------------------

ANOMALY_CONFIG = AnomalyConfig()


# ---------------------------------------------------------
# HELPER FUNCTIONS
# ---------------------------------------------------------

def allowed_file(filename):
    """Return True if the uploaded file is a CSV file."""
    return Path(filename).suffix.lower() in ALLOWED_EXTENSIONS


def get_active_paths():
    """Return the currently active dataset paths."""
    return (
        ACTIVE_DRIVERS_FILE,
        ACTIVE_TRIPS_FILE,
        ACTIVE_ACTIVITY_FILE
    )


def get_data_source():
    """Return the name of the currently active dataset."""
    return ACTIVE_DATA_SOURCE


def load_active_data():
    """Load and validate the currently active dataset."""

    (
        drivers_path,
        trips_path,
        activity_path
    ) = get_active_paths()

    return load_and_validate(
        drivers_path,
        trips_path,
        activity_path
    )


def load_and_validate(
    drivers_path,
    trips_path,
    activity_path
):
    """
    Load CSV files, create Python objects,
    validate the data, and create analytics.
    """

    loader = DataLoader()

    data = loader.load_all(
        str(drivers_path),
        str(trips_path),
        str(activity_path)
    )

    validator = DataValidator()

    validation_result = validator.validate_all(
        data["drivers"],
        data["trips"],
        data["driver_activity"]
    )

    analytics = AnalyticsService(data)

    summary = {
        "drivers": len(data["drivers"]),
        "trips": len(data["trips"]),
        "zones": len(data["zones"]),
        "activity_records": len(data["driver_activity"]),

        "total_drivers": len(data["drivers"]),
        "total_trips": len(data["trips"]),
        "total_zones": len(data["zones"]),
        "total_activity": len(data["driver_activity"])
    }

    return (
        data,
        validation_result,
        summary,
        analytics
    )


# ---------------------------------------------------------
# DASHBOARD DATA
# ---------------------------------------------------------

def get_dashboard_data(analytics):
    """Prepare all analytics required by the dashboard."""

    return {
        "kpis": analytics.get_dashboard_kpis(),

        "trip_status_counts": (
            analytics.get_trip_status_counts()
        ),

        "cancellation_reasons": (
            analytics.get_cancellation_reasons()
        ),

        "top_revenue_drivers": (
            analytics.get_driver_rankings(
                "revenue",
                5
            )
        ),

        "top_trip_drivers": (
            analytics.get_driver_rankings(
                "completed_trips",
                5
            )
        ),

        "zone_demand": (
            analytics.get_zone_demand()
        )
    }


# ---------------------------------------------------------
# ADVANCED ANALYTICS DATA
# ---------------------------------------------------------

def get_advanced_analytics_data(analytics):
    """Prepare all Day 3 advanced analytics."""

    return {
        "top_revenue_drivers": (
            analytics.get_driver_rankings(
                "revenue",
                10
            )
        ),

        "top_completed_trip_drivers": (
            analytics.get_driver_rankings(
                "completed_trips",
                10
            )
        ),

        "top_cancellation_drivers": (
            analytics.get_driver_rankings(
                "cancellation_rate",
                10
            )
        ),

        "top_zones": (
            analytics.get_top_k_zones(10)
        ),

        "peak_demand": (
            analytics.get_peak_demand(
                top_k=10
            )
        ),

        "driver_utilization": (
            analytics.get_top_utilized_drivers(10)
        ),

        "idle_time": (
            analytics.get_idle_time_analysis()
        ),

        "consecutive_trips": (
            analytics.get_consecutive_trip_analysis()
        ),

        "cancellation_intelligence": (
            analytics.get_cancellation_intelligence()
        )
    }


# ---------------------------------------------------------
# DAY 4 — ANOMALY + INSIGHTS DATA
# ---------------------------------------------------------

def get_day4_data(data, analytics):
    """Prepare all Day 4 anomaly and insight information."""

    anomaly_detector = AnomalyDetector(
        config=ANOMALY_CONFIG
    )

    anomaly_results = anomaly_detector.detect_all(
        drivers=data["drivers"],
        trips=data["trips"],
        analytics=analytics
    )

    insights_engine = InsightsEngine(
        analytics=analytics,
        anomaly_results=anomaly_results
    )

    insights = insights_engine.generate_insights()

    return {
        "anomaly_results": anomaly_results,
        "insights": insights,
        "anomaly_thresholds": (
            anomaly_detector.get_thresholds()
        )
    }


# ---------------------------------------------------------
# OPERATIONS DATA
# ---------------------------------------------------------

def get_operations_data(analytics):
    """
    Prepare all data required by operations.html.
    """

    return {
        "peak_demand": (
            analytics.get_peak_demand(
                top_k=10
            )
        ),

        "cancellation_intelligence": (
            analytics.get_cancellation_intelligence()
        ),

        "zone_demand": (
            analytics.get_zone_demand()
        ),

        "utilization": (
            analytics.get_top_utilized_drivers(10)
        ),

        "idle_analysis": (
            analytics.get_idle_time_analysis()
        ),

        "consecutive_trips": (
            analytics.get_consecutive_trip_analysis()
        )
    }


# ---------------------------------------------------------
# OPERATIONS PAGE RENDERING
# ---------------------------------------------------------

def render_operations_page(
    data,
    validation_result,
    summary,
    analytics,
    search_result=None
):
    """
    Render the Operations Intelligence page.
    """

    day4_data = get_day4_data(
        data,
        analytics
    )

    operations_data = get_operations_data(
        analytics
    )

    return render_template(
        "operations.html",

        summary=summary,

        validation=validation_result,

        data_source=get_data_source(),

        search_result=search_result,

        **day4_data,

        **operations_data
    )


# ---------------------------------------------------------
# ZONE SEARCH HELPER
# ---------------------------------------------------------

def find_zone_by_name(
    analytics,
    zone_name,
    city=None
):
    """
    Find a zone using the AnalyticsService zone index.
    """

    if city:

        return analytics.get_zone(
            city,
            zone_name
        )

    for (
        zone_city,
        indexed_zone_name
    ), zone in analytics.zone_index.items():

        if (
            indexed_zone_name.lower()
            == zone_name.lower()
        ):

            return zone

    return None


# ---------------------------------------------------------
# HOME PAGE
# ---------------------------------------------------------

@app.route("/")
def index():
    """Display the application home page."""

    return render_template(
        "index.html"
    )


# ---------------------------------------------------------
# DASHBOARD
# ---------------------------------------------------------

@app.route("/dashboard")
def dashboard():
    """Load the active dataset and display the dashboard."""

    try:

        (
            data,
            validation_result,
            summary,
            analytics
        ) = load_active_data()

        dashboard_data = get_dashboard_data(
            analytics
        )

        return render_template(
            "dashboard.html",

            summary=summary,

            validation=validation_result,

            data_source=get_data_source(),

            **dashboard_data
        )

    except Exception as error:

        return render_template(
            "index.html",

            error=(
                f"Unable to load data: {error}"
            )
        )


# ---------------------------------------------------------
# DAY 3 — ADVANCED ANALYTICS
# ---------------------------------------------------------

@app.route("/analytics")
def analytics_dashboard():
    """
    Display Day 3 advanced analytics.
    """

    try:

        (
            data,
            validation_result,
            summary,
            analytics
        ) = load_active_data()

        advanced_data = get_advanced_analytics_data(
            analytics
        )

        return render_template(
            "analytics.html",

            summary=summary,

            validation=validation_result,

            data_source=get_data_source(),

            **advanced_data
        )

    except Exception as error:

        return render_template(
            "index.html",

            error=(
                "Unable to load advanced analytics: "
                f"{error}"
            )
        )


# ---------------------------------------------------------
# DAY 4 — OPERATIONS INTELLIGENCE
# ---------------------------------------------------------

@app.route("/operations")
def operations():
    """
    Display the Operations Intelligence page.
    """

    try:

        (
            data,
            validation_result,
            summary,
            analytics
        ) = load_active_data()

        return render_operations_page(
            data,
            validation_result,
            summary,
            analytics
        )

    except Exception as error:

        return render_template(
            "index.html",

            error=(
                "Unable to load operations intelligence: "
                f"{error}"
            )
        )


# ---------------------------------------------------------
# DAY 4 — CONFIGURE ANOMALY THRESHOLDS
# ---------------------------------------------------------

@app.route(
    "/configure-thresholds",
    methods=["POST"]
)
def configure_thresholds():
    """Update anomaly detection thresholds."""

    try:

        max_trip_duration_minutes = float(
            request.form.get(
                "max_trip_duration_minutes",
                ""
            )
        )

        unusual_fare = float(
            request.form.get(
                "unusual_fare",
                ""
            )
        )

        high_cancellation_rate = float(
            request.form.get(
                "high_cancellation_rate",
                ""
            )
        )

        low_utilization_rate = float(
            request.form.get(
                "low_utilization_rate",
                ""
            )
        )

        high_trip_count = int(
            request.form.get(
                "high_trip_count",
                ""
            )
        )

        low_rating = float(
            request.form.get(
                "low_rating",
                ""
            )
        )

        min_distance_km = float(
            request.form.get(
                "min_distance_km",
                ""
            )
        )

        if max_trip_duration_minutes <= 0:
            raise ValueError(
                "Maximum trip duration must be greater than 0."
            )

        if unusual_fare < 0:
            raise ValueError(
                "Unusual fare cannot be negative."
            )

        if not 0 <= high_cancellation_rate <= 100:
            raise ValueError(
                "High cancellation rate must be between 0 and 100."
            )

        if not 0 <= low_utilization_rate <= 100:
            raise ValueError(
                "Low utilization rate must be between 0 and 100."
            )

        if high_trip_count <= 0:
            raise ValueError(
                "High trip count must be greater than 0."
            )

        if not 0 <= low_rating <= 5:
            raise ValueError(
                "Low rating must be between 0 and 5."
            )

        if min_distance_km < 0:
            raise ValueError(
                "Minimum distance cannot be negative."
            )

        detector = AnomalyDetector(
            config=ANOMALY_CONFIG
        )

        detector.update_thresholds(
            max_trip_duration_minutes=(
                max_trip_duration_minutes
            ),

            unusual_fare=(
                unusual_fare
            ),

            high_cancellation_rate=(
                high_cancellation_rate
            ),

            low_utilization_rate=(
                low_utilization_rate
            ),

            high_trip_count=(
                high_trip_count
            ),

            low_rating=(
                low_rating
            ),

            min_distance_km=(
                min_distance_km
            )
        )

        (
            data,
            validation_result,
            summary,
            analytics
        ) = load_active_data()

        return render_operations_page(
            data,
            validation_result,
            summary,
            analytics
        )

    except (ValueError, TypeError):

        return render_template(
            "index.html",

            error=(
                "Invalid threshold values. "
                "Please enter valid numeric values."
            )
        )

    except Exception as error:

        return render_template(
            "index.html",

            error=(
                "Unable to update anomaly thresholds: "
                f"{error}"
            )
        )


# ---------------------------------------------------------
# DAY 4 — SEARCH ENGINE
# ---------------------------------------------------------

@app.route("/search")
def search():
    """Search for a Driver, Trip, or Zone."""

    entity_type = request.args.get(
        "entity_type",
        ""
    ).strip().lower()

    entity_id = request.args.get(
        "entity_id",
        ""
    ).strip()

    city = request.args.get(
        "city",
        ""
    ).strip()

    search_result = None

    if entity_type and entity_id:

        try:

            (
                data,
                validation_result,
                summary,
                analytics
            ) = load_active_data()

            # DRIVER SEARCH
            if entity_type == "driver":

                result = analytics.get_driver(
                    entity_id
                )

                if result:

                    search_result = {
                        "found": True,
                        "data": result.get_profile()
                    }

                else:

                    search_result = {
                        "found": False,
                        "message": (
                            f"Driver '{entity_id}' "
                            "was not found."
                        )
                    }

            # TRIP SEARCH
            elif entity_type == "trip":

                result = analytics.get_trip(
                    entity_id
                )

                if result:

                    search_result = {
                        "found": True,

                        "data": {
                            "trip_id": result.trip_id,
                            "driver_id": result.driver_id,
                            "rider_id": result.rider_id,
                            "city": result.city,
                            "pickup_zone": result.pickup_zone,
                            "drop_zone": result.drop_zone,
                            "request_time": result.request_time,
                            "pickup_time": result.pickup_time,
                            "drop_time": result.drop_time,
                            "distance_km": result.distance_km,
                            "fare": result.fare,
                            "status": result.status,
                            "cancellation_reason": (
                                result.cancellation_reason
                            )
                        }
                    }

                else:

                    search_result = {
                        "found": False,
                        "message": (
                            f"Trip '{entity_id}' "
                            "was not found."
                        )
                    }

            # ZONE SEARCH
            elif entity_type == "zone":

                result = find_zone_by_name(
                    analytics,
                    entity_id,
                    city if city else None
                )

                if result:

                    search_result = {
                        "found": True,
                        "data": result.get_profile()
                    }

                else:

                    search_result = {
                        "found": False,
                        "message": (
                            f"Zone '{entity_id}' "
                            "was not found."
                        )
                    }

            else:

                search_result = {
                    "found": False,
                    "message": (
                        "Invalid search type. "
                        "Please select Driver, Trip, or Zone."
                    )
                }

            return render_operations_page(
                data,
                validation_result,
                summary,
                analytics,
                search_result
            )

        except Exception as error:

            return render_template(
                "index.html",

                error=(
                    "Unable to perform search: "
                    f"{error}"
                )
            )

    return render_template(
        "index.html",

        error=(
            "Please provide both an entity type "
            "and an entity ID."
        )
    )


# ---------------------------------------------------------
# FILE UPLOAD
# ---------------------------------------------------------

@app.route(
    "/upload",
    methods=["POST"]
)
def upload():
    """Handle CSV file uploads."""

    global ACTIVE_DRIVERS_FILE
    global ACTIVE_TRIPS_FILE
    global ACTIVE_ACTIVITY_FILE
    global ACTIVE_DATA_SOURCE

    drivers_file = request.files.get(
        "drivers_file"
    )

    trips_file = request.files.get(
        "trips_file"
    )

    activity_file = request.files.get(
        "activity_file"
    )

    if (
        not drivers_file
        or not trips_file
        or not activity_file
    ):

        return render_template(
            "index.html",

            error=(
                "Please upload all three CSV files."
            )
        )

    if (
        not drivers_file.filename
        or not trips_file.filename
        or not activity_file.filename
    ):

        return render_template(
            "index.html",

            error=(
                "Please select valid CSV files."
            )
        )

    if not all([
        allowed_file(drivers_file.filename),
        allowed_file(trips_file.filename),
        allowed_file(activity_file.filename)
    ]):

        return render_template(
            "index.html",

            error=(
                "Only CSV files are allowed."
            )
        )

    drivers_path = (
        UPLOAD_DIR / "drivers.csv"
    )

    trips_path = (
        UPLOAD_DIR / "trips.csv"
    )

    activity_path = (
        UPLOAD_DIR / "driver_activity.csv"
    )

    drivers_file.save(
        drivers_path
    )

    trips_file.save(
        trips_path
    )

    activity_file.save(
        activity_path
    )

    try:

        (
            data,
            validation_result,
            summary,
            analytics
        ) = load_and_validate(
            drivers_path,
            trips_path,
            activity_path
        )

        ACTIVE_DRIVERS_FILE = drivers_path
        ACTIVE_TRIPS_FILE = trips_path
        ACTIVE_ACTIVITY_FILE = activity_path

        ACTIVE_DATA_SOURCE = "Uploaded Data"

        dashboard_data = get_dashboard_data(
            analytics
        )

        return render_template(
            "dashboard.html",

            summary=summary,

            validation=validation_result,

            data_source=get_data_source(),

            **dashboard_data
        )

    except Exception as error:

        return render_template(
            "index.html",

            error=(
                "Unable to process uploaded data: "
                f"{error}"
            )
        )


# ---------------------------------------------------------
# DRIVER ANALYTICS
# ---------------------------------------------------------

@app.route("/driver")
def driver():

    driver_id = request.args.get(
        "driver_id",
        ""
    ).strip()

    try:

        (
            data,
            validation_result,
            summary,
            analytics
        ) = load_active_data()

        performance = None

        if driver_id:

            performance = analytics.get_driver_performance(
                driver_id
            )

        return render_template(
            "driver.html",

            driver_id=driver_id,

            performance=performance
        )

    except Exception as error:

        return render_template(
            "index.html",

            error=(
                "Unable to load driver data: "
                f"{error}"
            )
        )


# ---------------------------------------------------------
# ZONE ANALYTICS
# ---------------------------------------------------------

@app.route("/zone")
def zone():

    city = request.args.get(
        "city",
        ""
    ).strip()

    zone_name = request.args.get(
        "zone",
        ""
    ).strip()

    try:

        (
            data,
            validation_result,
            summary,
            analytics
        ) = load_active_data()

        performance = None

        if city and zone_name:

            performance = analytics.get_zone_performance(
                city,
                zone_name
            )

        return render_template(
            "zone.html",

            city=city,

            zone_name=zone_name,

            performance=performance
        )

    except Exception as error:

        return render_template(
            "index.html",

            error=(
                "Unable to load zone data: "
                f"{error}"
            )
        )


# ---------------------------------------------------------
# APPLICATION ENTRY POINT
# ---------------------------------------------------------

if __name__ == "__main__":

    app.run(
        debug=True
    )