Mobility Marketplace Operations Intelligence Engine
Optimization and Complexity Analysis

This document describes the main optimization techniques used in the Mobility Marketplace Operations Intelligence Engine.

The project uses Python objects, dictionaries, indexing, grouping, sorting, and heap-based Top-K selection to process driver, trip, zone, and activity data efficiently.

1. Data Loading
Function

DataLoader.load_drivers()

Approach

The function reads the drivers CSV file once using csv.DictReader.

For every row, it creates one Driver object and appends it to the drivers list.

Time Complexity

O(D)

Where D is the number of driver records.

Each driver record is processed exactly once.

Space Complexity

O(D)

The created Driver objects are stored in memory.

2. Trip Loading
Function

DataLoader.load_trips()

Approach

The function scans the trips CSV once and creates one Trip object for every record.

Time Complexity

O(T)

Where T is the number of trip records.

Space Complexity

O(T)

All trip objects are stored in memory for subsequent analytics.

3. Zone Creation
Function

DataLoader.create_zones()

Approach

Zones are identified using a dictionary key:

(city, zone_name)

A dictionary is used to avoid repeatedly scanning the existing zone list.

For every trip, the function performs dictionary membership checks for the pickup and drop zones.

Time Complexity

O(T) average

Dictionary lookup is O(1) on average.

Since each trip is processed once, the overall operation is approximately linear in the number of trips.

Space Complexity

O(Z)

Where Z is the number of unique city-zone combinations.

4. Loading the Complete Dataset
Function

DataLoader.load_all()

Approach

The function sequentially loads:

Drivers
Trips
Driver activity
Zones
Time Complexity

O(D + T + A)

Where:

D = number of drivers
T = number of trips
A = number of driver activity records

Each dataset is scanned once.

Space Complexity

O(D + T + A + Z)

The application stores the loaded objects and activity records in memory.

5. Analytics Index Construction
Function

AnalyticsService._build_indexes()

Approach

The analytics service builds dictionary-based indexes for frequently accessed entities.

Examples include:

Driver ID → Driver
Trip ID → Trip
City → Trips
Zone → Trips
Driver → Trips
Driver → Activity

This avoids repeatedly scanning the complete dataset.

Time Complexity

O(D + T + Z + A)

Each dataset is processed approximately once while building the indexes.

Space Complexity

O(D + T + Z + A)

The indexes require additional memory to store references/groupings.

6. Driver Lookup
Function

AnalyticsService.get_driver(driver_id)

Approach

The driver is retrieved directly from the dictionary index using the driver ID.

Time Complexity

O(1) average

Dictionary lookup provides constant average-time access.

Space Complexity

O(1)

No additional data structure proportional to the dataset is created.

7. Top-K Driver Rankings
Function

AnalyticsService.get_driver_rankings(metric, top_k=10)

Approach

The function first calculates driver metrics and then uses Python's heapq.nlargest() to retrieve only the required Top-K drivers.

This avoids completely sorting all drivers when only the top few results are required.

Time Complexity

O(D + D log K)

Where:

D = number of drivers
K = requested number of top drivers

For small K values such as 5 or 10, this is more efficient than sorting the complete driver list.

Space Complexity

O(D)

Driver metrics are maintained in memory, with additional heap-related space dependent on K.

8. Consecutive Trip Analysis
Function

AnalyticsService.get_consecutive_trip_analysis()

Approach

The function:

Groups completed trips by driver.
Sorts trips chronologically.
Scans the sorted trips.
Identifies consecutive trips based on the configured time gap.
Time Complexity

O(T log T)

The dominant operation is sorting the trip records.

Space Complexity

O(T)

Trip groups and intermediate sequences are maintained in memory.

9. Idle-Time Analysis
Function

AnalyticsService.get_idle_time_analysis()

Approach

Driver activity records are grouped by driver and ordered chronologically.

The function scans consecutive activity records and calculates periods where the driver remained idle beyond the configured threshold.

Time Complexity

O(A log A)

The dominant operation is sorting activity records.

Space Complexity

O(A)

Activity records and grouped data are stored during analysis.

10. Driver Utilization
Function

AnalyticsService.get_driver_utilization()

Approach

The function processes driver activity records, calculates online and busy periods, and derives utilization metrics.

The calculation uses activity timestamps rather than repeatedly querying the complete trip dataset.

Time Complexity

O(A log A + D)

Where:

A = activity records
D = drivers

The sorting of activity records is the dominant operation.

Space Complexity

O(A + D)

Activity information and driver-level utilization results are stored in memory.

Optimization Techniques Used
1. Dictionary Indexing

Frequently accessed entities are indexed using dictionaries.

Example:

driver_index[driver_id]

This changes repeated driver searches from a linear scan to approximately constant-time lookup.

2. Dictionary-Based Zone Deduplication

Zones are identified using:

(city, zone_name)

as the dictionary key.

This avoids repeatedly searching through a list of existing zones.

3. Heap-Based Top-K Selection

The application uses:

heapq.nlargest()

for Top-K driver rankings.

Instead of sorting every driver when only the top few are required, the algorithm maintains the required top K values.

4. Grouped Analytics

Trips and activity records are grouped by useful dimensions such as:

Driver
City
Zone

This prevents repeatedly scanning the entire dataset for every individual query.

5. Reusable Analytics Service

Analytics calculations are centralized inside AnalyticsService.

The Flask routes do not independently recalculate metrics.

This improves:

Reusability
Maintainability
Performance
Separation of concerns
Optimization Summary
Function	Approach	Time Complexity	Space Complexity
load_drivers()	Single CSV pass	O(D)	O(D)
load_trips()	Single CSV pass	O(T)	O(T)
create_zones()	Dictionary-based deduplication	O(T) average	O(Z)
load_all()	Sequential dataset loading	O(D + T + A)	O(D + T + A + Z)
_build_indexes()	Dictionary/group indexes	O(D + T + Z + A)	O(D + T + Z + A)
get_driver()	Dictionary lookup	O(1) average	O(1)
get_driver_rankings()	Heap-based Top-K	O(D + D log K)	O(D)
get_consecutive_trip_analysis()	Group + chronological sort	O(T log T)	O(T)
get_idle_time_analysis()	Group + chronological sort	O(A log A)	O(A)
get_driver_utilization()	Activity sorting + aggregation	O(A log A + D)	O(A + D)
Final Optimization Takeaway

The application is optimized primarily through pre-built dictionary indexes, dictionary-based grouping, heap-based Top-K selection, and single-pass dataset processing.

The main trade-off is increased memory usage because indexes and loaded Python objects are retained in memory. This is appropriate for the current local analytics application and sample dataset size.

2. Verify the file

After saving, run:

ls docs

You should see:

complexity.md

Then run the tests one more time:

python -m unittest discover -s tests -v
