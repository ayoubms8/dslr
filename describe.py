import csv
import sys
import math


def calculate_mean(data):
    return sum(data) / len(data) if data else 0

def calculate_std(data, Mean):
    return math.sqrt(sum((x - Mean) ** 2 for x in data) / (len(data) - 1)) if data and len(data) > 1 else 0

def calculate_percentile(data, percentage):
    sorted_data = sorted(data)
    position = (len(sorted_data) - 1) * percentage

    lower_index = int(position)
    upper_index = lower_index + 1

    if upper_index >= len(sorted_data):
        return sorted_data[lower_index]

    fraction = position - lower_index

    return (
        sorted_data[lower_index]
        + fraction
        * (sorted_data[upper_index] - sorted_data[lower_index])
    )

def calculate_min(data):
    res = data[0]
    for x in data[1:]:
        if x < res:
            res = x
    return res

def calculate_max(data):
    res = data[0]
    for x in data[1:]:
        if x > res:
            res = x
    return res



def load_csv(filename):
    features = {}

    with open(filename, mode='r') as file:
        csv_reader = csv.DictReader(file)
        for column in csv_reader.fieldnames:
            if column not in ("Index", "Hogwarts House", "First Name", "Last Name", "Birthday", "Best Hand"):
                features[column] = []
        for row in csv_reader:
            for column in features:
                value = row[column]
                if value == "" or value.lower() == "nan":
                    continue
                features[column].append(float(value))

    return features

if len(sys.argv) != 2:
    print("Usage: python describe.py <filename>")
    sys.exit(1)

filename = sys.argv[1]
data = load_csv(filename)

Count = {column: len(data[column]) for column in data}

Mean = {column: calculate_mean(data[column]) for column in data}

Std = {column: calculate_std(data[column], Mean[column]) for column in data}

minimum = {column: calculate_min(data[column]) for column in data}

maximum = {column: calculate_max(data[column]) for column in data}

percentiles = {column: {
    "25%": calculate_percentile(data[column], 0.25),
    "50%": calculate_percentile(data[column], 0.50),
    "75%": calculate_percentile(data[column], 0.75)
} for column in data}

def print_statistics():
    rows = [
        ("Count", Count),
        ("Mean", Mean),
        ("Std", Std),
        ("Min", minimum),
        ("25%", {
            column: percentiles[column]["25%"]
            for column in data
        }),
        ("50%", {
            column: percentiles[column]["50%"]
            for column in data
        }),
        ("75%", {
            column: percentiles[column]["75%"]
            for column in data
        }),
        ("Max", maximum),
    ]

    label_width = 8
    column_widths = {
        column: max(18, len(column) + 2)
        for column in data
    }

    header = " " * label_width

    for column in data:
        header += column.rjust(column_widths[column])

    print(header)

    for label, values in rows:
        line = label.ljust(label_width)

        for column in data:
            line += f"{values[column]:>{column_widths[column]}.6f}"

        print(line)

print_statistics()