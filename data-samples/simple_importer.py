import csv
from pymongo import MongoClient


def import_csv_to_mongo(
    file_path, db_name="brevetdb", collection_name="brevetCollection"
):
    # Connect to MongoDB
    client = MongoClient("mongodb://localhost:27017/")
    db = client[db_name]
    collection = db[collection_name]

    # Open the CSV file
    with open(file_path, "r") as csvfile:
        reader = csv.DictReader(csvfile)

        # List to hold multiple document dictionaries
        documents = []

        # Read through each row in the CSV
        for row in reader:
            # Convert the flat structure into a nested structure
            brevet_entry = {
                "distance": row["brevets/distance"],
                "begin_date": row["brevets/begin_date"],
                "begin_time": row["brevets/begin_time"],
                "controls": [],
            }

            # Add all control points
            num_controls = (len(row) - 3) // 5  # Adjusting for non-control columns
            for i in range(num_controls):
                control_point = {
                    "km": row.get(f"brevets/controls/{i}/km"),
                    "mi": row.get(f"brevets/controls/{i}/mi"),
                    "location": row.get(f"brevets/controls/{i}/location"),
                    "open": row.get(f"brevets/controls/{i}/open"),
                    "close": row.get(f"brevets/controls/{i}/close"),
                }
                brevet_entry["controls"].append(control_point)

            # Add the structured data to our list
            documents.append(brevet_entry)

        # Insert data into the MongoDB collection
        if documents:
            collection.insert_many(documents)

    print(
        f"Successfully imported {len(documents)} records into the {collection_name} collection."
    )


# Example usage:
import_csv_to_mongo("sample-data.csv")
