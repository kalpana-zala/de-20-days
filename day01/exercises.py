import csv

def to_fahrenheit(celsius):
    return celsius * 9 / 5 + 32

def count_words(path):
    text = open(path).read()
    words = text.split()
    return len(words)       # count the items in the list

def read_sales(path):
    rows = []
    with open(path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["amount"] = float(row["amount"])
            rows.append(row)
    return rows


def dedupe(rows):
    seen = set()              # order_ids we've already kept
    clean = []                # the rows we keep
    for row in rows:
        if row["order_id"] not in seen:
            clean.append(row)
            seen.add(row["order_id"])
    return clean

def sales_by_city(rows):
    totals = {}
    for row in rows:
        city = row["city"]
        totals[city] = totals.get(city, 0) + row["amount"]
    return totals

if __name__ == "__main__":
    print(to_fahrenheit(30))
    print(count_words("day01/sales.csv"))
    sales = dedupe(read_sales("day01/sales.csv"))
    for row in sales:
        print(row)
    print(sales_by_city(sales))