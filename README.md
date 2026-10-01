# Mobility Marketplace Operations Intelligence Engine

A Flask-based operations intelligence platform for analyzing mobility marketplace data across drivers, trips, zones, demand, cancellations, utilization, idle time, anomalies, and operational performance.

The application combines object-oriented Python design, data validation, dictionary-based indexing, aggregation, sorting, heap-based Top-K analysis, consecutive-trip analysis, idle-time detection, anomaly detection, and dynamic business insights into a single operational analytics platform.

---

## 1. Business Problem

Mobility marketplaces generate large volumes of operational data involving:

* Drivers
* Trips
* Riders
* Cities
* Pickup and drop zones
* Driver activity
* Trip status
* Cancellation reasons
* Revenue
* Distance
* Trip duration

Raw operational data alone does not immediately provide actionable visibility into marketplace performance.

Operations teams need to understand:

* Where demand is concentrated
* When demand peaks
* Which drivers generate the most revenue
* Which drivers complete the most trips
* Where cancellations are concentrated
* Which drivers have low utilization
* Where drivers experience extended idle periods
* Which drivers have consecutive trip opportunities
* Which records contain data-quality problems
* Which operational patterns require investigation

The goal of this project is to transform raw mobility marketplace datasets into an interactive operations intelligence system.

---

## 2. Project Objective

The Mobility Marketplace Operations Intelligence Engine provides a single application for:

1. Loading mobility marketplace CSV datasets
2. Validating data quality
3. Converting raw records into Python objects
4. Building reusable analytics indexes
5. Calculating marketplace KPIs
6. Performing driver analytics
7. Performing zone analytics
8. Performing demand analysis
9. Performing cancellation analysis
10. Calculating driver utilization
11. Detecting idle periods
12. Detecting consecutive trip sequences
13. Detecting operational anomalies
14. Generating business insights
15. Presenting results through a Flask web application

---

## 3. Key Features

### 3.1 Data Management

* CSV upload
* Sample dataset loading
* Driver data loading
* Trip data loading
* Driver activity loading
* Automatic zone creation

### 3.2 Data Validation

The application validates:

* Required columns
* Empty datasets
* Missing values
* Duplicate driver IDs
* Duplicate trip IDs
* Duplicate activity records
* Invalid driver IDs
* Invalid timestamps
* Missing pickup timestamps
* Negative fares
* Negative distances
* Invalid driver ratings
* Invalid driver status
* Invalid activity status
* Invalid trip timing

### 3.3 Dashboard Analytics

The dashboard provides:

* Total drivers
* Active drivers
* Total riders
* Total trips
* Completed trips
* Cancelled trips
* Completion rate
* Cancellation rate
* Total revenue
* Average fare
* Average distance
* Average trip duration
* Trip status distribution
* Cancellation reason distribution
* Top revenue drivers
* Top completed-trip drivers
* Zone demand

### 3.4 Driver Analytics

The driver analytics module provides:

* Driver profile
* Driver city
* Vehicle type
* Rating
* Driver status
* Total trips
* Completed trips
* Cancelled trips
* Cancellation rate
* Revenue
* Average fare
* Average distance

Driver rankings are available for multiple performance metrics.

### 3.5 Zone Analytics

The zone analytics module provides:

* City
* Zone
* Total requests
* Completed trips
* Cancelled trips
* Completion rate
* Cancellation rate
* Revenue
* Average fare

### 3.6 Advanced Analytics

The application supports:

* Top-K driver rankings
* Top-K zones
* Peak demand analysis
* Driver utilization
* Idle-time analysis
* Consecutive-trip analysis
* Cancellation intelligence
* Driver trip frequency
* Rider trip frequency

### 3.7 Anomaly Detection

The anomaly detection engine identifies issues such as:

* Unknown drivers
* Negative fares
* Negative distances
* Zero-distance trips
* Missing timestamps
* Invalid trip timing
* Excessively long trips
* Unusually high fares
* High driver cancellation rates
* Low driver utilization
* High driver trip counts
* Low driver ratings

---

## 4. Technology Stack

### Backend

* Python
* Flask
* CSV processing
* Object-oriented programming
* Python data structures
* Heap-based Top-K algorithms

### Frontend

* HTML
* CSS
* JavaScript
* Jinja2 templates

### Testing

* Python `unittest`

### Data

* CSV datasets

---

## 5. Project Architecture

The application follows a layered architecture.

### High-Level Flow

```text
User
  ↓
Flask Web Application
  ↓
Data Loading
  ↓
Data Validation
  ↓
Python Objects
  ↓
Analytics Service
  ↓
Anomaly Detection / Insights
  ↓
HTML Dashboard
```

The architecture separates data loading, validation, business logic, anomaly detection, and presentation.

---

## 6. Project Structure

```text
mobility_operations_tool/
├── app.py
├── models/
│   ├── __init__.py
│   ├── driver.py
│   ├── trip.py
│   └── zone.py
├── services/
│   ├── __init__.py
│   ├── data_loader.py
│   ├── validation_service.py
│   ├── analytics_service.py
│   ├── anomaly_service.py
│   └── insights_service.py
├── templates/
│   ├── index.html
│   ├── dashboard.html
│   ├── driver.html
│   ├── zone.html
│   ├── analytics.html
│   └── operations.html
├── static/
│   └── style.css
├── data/
│   ├── drivers.csv
│   ├── trips.csv
│   ├── driver_activity.csv
│   └── generate_data.py
├── tests/
│   ├── __init__.py
│   ├── test_analytics.py
│   ├── test_anomalies.py
│   └── test_validation.py
├── docs/
│   └── complexity.md
├── requirements.txt
└── README.md
```

---

## 7. Object-Oriented Design

The project uses Python classes to represent core business entities.

### 7.1 Driver

The `Driver` class represents a mobility driver.

**Main attributes:**

* `driver_id`
* `driver_name`
* `city`
* `vehicle_type`
* `rating`
* `status`

**Main methods:**

* `is_active()`
* `get_profile()`

### 7.2 Trip

The `Trip` class represents a marketplace trip.

**Main attributes:**

* `trip_id`
* `driver_id`
* `rider_id`
* `city`
* `pickup_zone`
* `drop_zone`
* `request_time`
* `pickup_time`
* `drop_time`
* `distance_km`
* `fare`
* `status`
* `cancellation_reason`

The class also converts timestamp values into Python `datetime` objects.

### 7.3 Zone

The `Zone` class represents a marketplace operating zone.

A zone is identified by:

* City
* Zone name

Zones are automatically created from pickup and drop-zone information in the trip dataset.

---

## 8. Data Loading

The `DataLoader` service is responsible for reading CSV files and creating Python objects.

The loader provides:

* `load_drivers()`
* `load_trips()`
* `load_driver_activity()`
* `create_zones()`
* `load_all()`

The application converts raw CSV records into reusable Python objects before analytics are performed.

---

## 9. Data Validation

The `DataValidator` validates the uploaded datasets before they are used for operational analysis.

The validation layer checks:

* Required columns
* Empty datasets
* Missing values
* Duplicate records
* Driver references
* Numeric values
* Timestamp validity
* Driver status
* Driver ratings
* Trip timing
* Activity status

The validation system returns:

* Validation status
* Errors
* Warnings
* Validation summary

The sample dataset intentionally contains invalid records so that the validation and anomaly-detection functionality can be demonstrated.

---

## 10. Analytics Service

The `AnalyticsService` contains the main marketplace analytics logic.

It maintains indexes such as:

* Driver index
* Trip index
* Zone index
* Trips by driver
* Trips by city
* Trips by zone
* Driver activity

These indexes allow frequently accessed records to be retrieved efficiently.

---

## 11. Dashboard KPIs

The current sample dataset produces the following metrics:

| KPI                   |      Value |
| --------------------- | ---------: |
| Total Drivers         |        250 |
| Active Drivers        |        196 |
| Total Riders          |      2,717 |
| Total Trips           |      4,500 |
| Completed Trips       |      3,998 |
| Cancelled Trips       |        502 |
| Completion Rate       |     88.84% |
| Cancellation Rate     |     11.16% |
| Total Revenue         | ₹1,280,474 |
| Average Fare          |    ₹320.28 |
| Average Distance      |   13.46 km |
| Average Trip Duration |  43.28 min |

These values are generated from the currently loaded sample dataset.

---

## 12. DSA Techniques Used

The project intentionally uses Python data structures and algorithms rather than relying entirely on external analytical libraries.

### 12.1 Dictionary Indexing

Dictionaries are used for fast lookup of:

* Drivers
* Trips
* Zones
* Driver trips
* City trips
* Zone trips
* Driver activity

Average lookup complexity:

```text
O(1)
```

### 12.2 Dictionary-Based Deduplication

Zones are identified using:

```text
(city, zone_name)
```

as a dictionary key.

This avoids repeatedly searching through the existing zone collection.

### 12.3 Heap-Based Top-K

The project uses:

```python
heapq.nlargest()
```

for Top-K driver rankings.

This is useful when the application needs only the highest-performing `K` records rather than a completely sorted list.

### 12.4 Sorting

Sorting is used for:

* Driver rankings
* Chronological trip sequences
* Activity records
* Idle-time analysis
* Consecutive-trip analysis

### 12.5 Grouping

Records are grouped by:

* Driver
* City
* Zone
* Rider

This supports efficient aggregation and frequency analysis.

### 12.6 Consecutive Sequence Detection

Completed trips are ordered chronologically for each driver.

The application compares consecutive trips to identify sequences with short turnaround gaps.

---

## 13. Operational Analytics

### 13.1 Peak Demand

The system groups trips by hour and calculates demand for each period.

Current sample result:

**13:00–14:00 → 213 requests**

Other high-demand periods include:

| Time        | Requests |
| ----------- | -------: |
| 13:00–14:00 |      213 |
| 11:00–12:00 |      210 |
| 20:00–21:00 |      209 |
| 03:00–04:00 |      209 |

### 13.2 Cancellation Intelligence

Current sample data:

* Total cancelled trips: **502**
* Cancellation rate: **11.16%**

Cancellation breakdown:

| Reason           | Trips | Share |
| ---------------- | ----: | ----: |
| Driver Cancelled |   180 | 35.9% |
| Rider Cancelled  |   118 | 23.5% |
| Driver Not Found |    99 | 19.7% |
| Other            |    55 | 11.0% |
| Payment Issue    |    50 | 10.0% |

### 13.3 Zone Demand

The highest-requested zone in the current dataset is:

**Delhi — Connaught Place: 342 requests**

Other high-demand zones include:

| City      | Zone            | Requests |
| --------- | --------------- | -------: |
| Delhi     | Connaught Place |      342 |
| Delhi     | Rohini          |      339 |
| Delhi     | Vasant Kunj     |      339 |
| Delhi     | Dwarka          |      330 |
| Delhi     | Saket           |      311 |
| Bangalore | Indiranagar     |      308 |
| Bangalore | HSR Layout      |      303 |
| Mumbai    | Andheri         |      299 |

### 13.4 Driver Utilization

Utilization is calculated using online and busy time.

The highest-utilized driver in the displayed Top-K results is:

**Karan (D333) — 62.8%**

The utilization analysis also identifies drivers with significantly lower utilization, allowing operations teams to investigate supply allocation.

### 13.5 Idle-Time Analysis

The system detects extended periods between driver activity states.

For example:

**Anjali (D101)** had a detected idle period of:

**120 minutes**

The analysis identifies:

* Driver
* Start time
* End time
* Idle duration

### 13.6 Consecutive Trip Analysis

The system identifies completed-trip sequences where the turnaround between trips is below the configured threshold.

Example:

**Pooja (D107)**

* Sequence length: 2 trips
* Turnaround: 0 minutes

The analysis provides:

* Driver
* Sequence length
* Start time
* End time
* Total turnaround time

---

## 14. Anomaly Detection

The current sample dataset intentionally contains data-quality and operational anomalies.

The anomaly engine currently reports:

| Category         | Count |
| ---------------- | ----: |
| Total anomalies  | 1,314 |
| High severity    |    60 |
| Medium severity  | 1,254 |
| Trip anomalies   |   993 |
| Driver anomalies |   321 |

Examples of detected problems include:

* Negative fares
* Unknown driver IDs
* Missing pickup timestamps
* Drop time before pickup time
* Unusually high fares
* Driver-level operational anomalies

The unusual fare threshold is configured at:

**₹500**

---

## 15. Dynamic Business Insights

The application derives operational insights from analytics results rather than relying only on manually entered observations.

### Insight 1 — Demand Concentration

The highest observed marketplace demand occurs during:

**13:00–14:00**

with **213 requests**.

### Insight 2 — Driver Cancellation Contribution

Driver cancellations represent the largest cancellation category:

**180 trips / 35.9% of cancellations**

This provides a specific operational area for investigation.

### Insight 3 — High-Demand Zone

Delhi — Connaught Place records the highest observed pickup demand:

**342 requests**

### Insight 4 — Driver Utilization

The highest displayed driver utilization is:

**Karan (D333) — 62.8%**

The utilization analysis also identifies drivers with significantly lower utilization, allowing operations teams to investigate supply allocation.

### Insight 5 — Idle-Time Opportunities

The idle-time engine detects extended periods of inactivity, including multiple 120-minute idle periods.

This can help identify potential opportunities for better driver positioning and supply allocation.

### Insight 6 — Consecutive Trip Opportunities

The consecutive-trip analysis identifies drivers completing trips with short turnaround times.

These sequences can be used to understand driver productivity and potential marketplace supply patterns.

### Insight 7 — Data Quality and Operational Anomalies

The current dataset produces:

**1,314 detected anomalies**

This demonstrates the importance of combining marketplace analytics with data-quality monitoring.

---

## 16. Optimization

The project uses several optimization techniques.

### Dictionary Indexing

Frequently accessed records are indexed once rather than searched repeatedly.

### Single-Pass Processing

CSV records are processed sequentially where possible.

### Dictionary-Based Deduplication

Zones are deduplicated using dictionary keys.

### Heap-Based Top-K

`heapq.nlargest()` avoids completely sorting the dataset when only Top-K results are required.

### Reusable Analytics Layer

Analytics calculations are centralized in `AnalyticsService`, avoiding duplicated calculations across Flask routes.

Detailed complexity analysis is available in:

```text
docs/complexity.md
```

---

## 17. Time and Space Complexity

| Function                          | Approach                         | Time Complexity  | Space Complexity |
| --------------------------------- | -------------------------------- | ---------------- | ---------------- |
| `load_drivers()`                  | Single CSV pass                  | O(D)             | O(D)             |
| `load_trips()`                    | Single CSV pass                  | O(T)             | O(T)             |
| `create_zones()`                  | Dictionary deduplication         | O(T) average     | O(Z)             |
| `load_all()`                      | Sequential loading               | O(D + T + A)     | O(D + T + A + Z) |
| `_build_indexes()`                | Dictionary/group indexes         | O(D + T + Z + A) | O(D + T + Z + A) |
| `get_driver()`                    | Dictionary lookup                | O(1) average     | O(1)             |
| `get_driver_rankings()`           | Heap-based Top-K                 | O(D + D log K)   | O(D)             |
| `get_consecutive_trip_analysis()` | Group and sort                   | O(T log T)       | O(T)             |
| `get_idle_time_analysis()`        | Group and sort                   | O(A log A)       | O(A)             |
| `get_driver_utilization()`        | Activity sorting and aggregation | O(A log A + D)   | O(A + D)         |

Where:

* **D** = number of drivers
* **T** = number of trips
* **A** = number of activity records
* **Z** = number of zones
* **K** = requested Top-K value

---

## 18. Testing

The project includes automated tests covering:

* Analytics
* Anomaly detection
* Data validation

The final test suite contains:

**65 tests**

Current result:

**65/65 tests passing**

### Test Breakdown

| Test Module       |  Tests |
| ----------------- | -----: |
| Analytics         |     28 |
| Anomaly Detection |     19 |
| Validation        |     18 |
| **Total**         | **65** |

Run the complete suite with:

```bash
python -m unittest discover -s tests -v
```

---

## 19. Validation Test Coverage

The validation tests cover requirements including:

* Empty files
* Missing columns
* Missing values
* Invalid IDs
* Duplicate records
* Invalid timestamps
* Negative values
* Invalid ratings
* Invalid status values
* Invalid trip timing
* Valid records

The project intentionally contains invalid sample records so that the validation and anomaly-detection functionality can be demonstrated.

---

## 20. Sample Dataset

The generated sample dataset contains:

| Dataset         | Records |
| --------------- | ------: |
| Drivers         |     250 |
| Trips           |   4,500 |
| Zones           |      15 |
| Driver Activity |  16,191 |

The dataset generator is available at:

```text
data/generate_data.py
```

The generated data covers:

* Bangalore
* Mumbai
* Delhi

with multiple operating zones per city.

---

## 21. Application Pages

### Home / Upload

Allows users to:

* Upload driver CSV
* Upload trip CSV
* Upload driver activity CSV
* Load sample data

### Dashboard

Provides a marketplace-level overview including:

* KPIs
* Revenue
* Trip status
* Cancellation reasons
* Top drivers
* Zone demand

### Driver Analytics

Provides driver-level performance analysis.

Users can search for a driver using the driver ID.

Example:

```text
D283
```

### Zone Analytics

Provides zone-level operational metrics.

Users can select a city and zone.

Example:

```text
Delhi → Connaught Place
```

### Advanced Analytics

Provides:

* Top-K rankings
* Peak demand
* Utilization
* Cancellation analysis
* Zone analysis

### Operations Intelligence

Provides:

* Peak demand
* Demand by time
* Cancellation intelligence
* Zone demand
* Driver utilization
* Idle-time analysis
* Consecutive-trip analysis

### Anomaly Detection

Provides:

* Anomaly counts
* Severity distribution
* Trip anomalies
* Driver anomalies
* Individual anomaly records
* Configurable thresholds

---

## 22. Application Flow

The application follows this flow:

```text
Upload Data
     ↓
Load CSV Records
     ↓
Validate Data
     ↓
Create Driver / Trip / Zone Objects
     ↓
Build Analytics Indexes
     ↓
Calculate Marketplace KPIs
     ↓
Run Advanced Analytics
     ↓
Detect Anomalies
     ↓
Generate Business Insights
     ↓
Display Results in Flask UI
```

---

## 23. How to Run

### Step 1 — Navigate to the project

```bash
cd ~/mobility_operations_tool
```

### Step 2 — Activate the virtual environment

```bash
source venv/bin/activate
```

### Step 3 — Install dependencies

```bash
pip install -r requirements.txt
```

### Step 4 — Run the Flask application

```bash
python app.py
```

### Step 5 — Open the application

Open:

```text
http://127.0.0.1:5000/
```

---

## 24. Running Tests

Run:

```bash
python -m unittest discover -s tests -v
```

Expected result:

```text
65 tests passed
```

---

## 25. Assumptions

The application makes the following assumptions:

* CSV files follow the expected schema.
* Driver IDs are intended to uniquely identify drivers.
* Trip IDs are intended to uniquely identify trips.
* Timestamps use the expected datetime format.
* A completed trip has valid pickup and drop timestamps.
* Driver utilization is derived from driver activity records.
* A zone is identified by city and zone name.
* Cancellation analysis uses the cancellation reason recorded in the trip dataset.
* Top-K analysis uses the requested K value.
* Idle periods are determined using the configured minimum idle duration.
* Consecutive trips are determined using the configured maximum turnaround gap.

---

## 26. Limitations

The current application is designed as a local analytics and operations intelligence prototype.

Current limitations include:

* CSV-based data ingestion
* Local Flask deployment
* In-memory analytics indexes
* No production database
* No authentication/authorization
* No real-time streaming data
* No external marketplace API integration
* No distributed processing
* No persistent user/session management
* Analytics are based on the supplied/generated dataset

For production deployment, the architecture could be extended with a database, API layer, authentication, scheduled pipelines, and real-time event processing.

---

## 27. Future Improvements

Potential future improvements include:

* PostgreSQL integration
* Real-time trip/event ingestion
* Redis caching
* REST API layer
* Authentication and role-based access
* Real-time operational alerts
* Interactive charts
* Geospatial visualization
* Driver supply forecasting
* Demand forecasting
* Automated anomaly alerts
* Production deployment using Docker
* Cloud deployment
* Historical trend analysis
* Automated reporting

---

## 28. Final Project Demonstration

The recommended demonstration flow is:

### 1. Business Problem

Explain the marketplace operations problem and why raw trip data needs to be converted into operational intelligence.

### 2. Architecture

Show:

```text
Data
  ↓
Validation
  ↓
Objects
  ↓
Analytics
  ↓
Anomaly Detection
  ↓
Insights
  ↓
UI
```

### 3. OOP

Explain:

* `Driver`
* `Trip`
* `Zone`
* `DataLoader`
* `DataValidator`
* `AnalyticsService`
* `AnomalyDetector`
* `InsightsEngine`

### 4. DSA

Demonstrate:

* Dictionaries
* Indexing
* Grouping
* Sorting
* Heap-based Top-K
* Consecutive sequence detection

### 5. Live Demo

Demonstrate:

* Upload
* Dashboard
* Driver Analytics
* Zone Analytics
* Advanced Analytics
* Operations Intelligence
* Anomaly Detection

### 6. Business Insights

Highlight:

* Peak demand
* Cancellation behavior
* Zone demand
* Driver utilization
* Idle time
* Consecutive trips
* Data-quality anomalies

---

## 29. Project Outcome

The Mobility Marketplace Operations Intelligence Engine transforms raw mobility marketplace datasets into a structured operational intelligence platform.

The application demonstrates:

* Data ingestion
* Data validation
* Object-oriented programming
* Dictionary indexing
* Aggregation
* Ranking
* Heap-based Top-K analysis
* Sequential analysis
* Anomaly detection
* Operational analytics
* Dynamic business insights
* Flask application development
* Automated testing

The final implementation contains:

* **250 drivers**
* **4,500 trips**
* **15 zones**
* **16,191 activity records**
* **65 automated tests**
* **65/65 tests passing**

---

## 30. Conclusion

The Mobility Marketplace Operations Intelligence Engine provides an end-to-end example of how raw mobility marketplace data can be transformed into operational intelligence.

The architecture separates data loading, validation, business logic, anomaly detection, and presentation while using appropriate data structures and algorithms for efficient analytics.

The resulting application allows operations teams to explore marketplace performance across:

* Drivers
* Zones
* Demand
* Cancellations
* Utilization
* Idle time
* Consecutive trips
* Anomalies

through a single Flask-based interface.
