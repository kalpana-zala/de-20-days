# 1. Variables and types
city = "Mumbai"          # str  (like VARCHAR)
trips = 120              # int  (like INT64)
fare = 245.50            # float (like FLOAT64)
is_paid = True           # bool (like BOOL)
print(city, trips, fare, is_paid, type(fare))

# 2. Lists: an ordered collection, like one column of values
fares = [120.0, 245.5, 89.9, 310.0]
print("first:", fares[0], "count:", len(fares), "total:", sum(fares))

# 3. Dicts: key -> value, like one row of a table
trip = {"id": 1, "city": "Mumbai", "fare": 245.5}
print(trip["fare"])

# 4. A list of dicts = a table. This is how JSON from APIs looks.
trips_table = [
    {"id": 1, "city": "Mumbai", "fare": 245.5},
    {"id": 2, "city": "Pune",   "fare": 120.0},
    {"id": 3, "city": "Mumbai", "fare": 89.9},
]

# 5. Loop + if = SELECT ... WHERE
for row in trips_table:
    if row["city"] == "Mumbai":
        print(row)

# 6. Functions: reusable logic. Every pipeline step is a function.
def total_fare(rows, city):
    """Like: SELECT SUM(fare) FROM rows WHERE city = @city"""
    total = 0
    for row in rows:
        if row["city"] == city:
            total += row["fare"]
    return total

print("Mumbai total:", total_fare(trips_table, "Mumbai"))

# 7. GROUP BY with a dict
totals = {}
for row in trips_table:
    totals[row["city"]] = totals.get(row["city"], 0) + row["fare"]
print(totals)
