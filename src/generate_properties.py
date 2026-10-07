import csv
import random

towns = [
    ("Ipswich", "IP"),
    ("Colchester", "CO"),
    ("Chelmsford", "CM"),
    ("London", "E"),
    ("Cambridge", "CB"),
    ("Norwich", "NR")
]

streets = [
    "London Road",
    "High Street",
    "Station Road",
    "Church Road",
    "Victoria Road",
    "Park Road",
    "Mill Lane",
    "King Street",
    "Queen Street",
    "Springfield Road"
]

property_types = [
    "House",
    "Apartment",
    "Bungalow",
    "Cottage"
]

with open("properties.csv", "w", newline="") as file:

    writer = csv.writer(file)

    writer.writerow([
        "Name",
        "AddressLine1",
        "TownCity",
        "Postcode",
        "AskingPrice"
    ])

    for i in range(1, 10001):

        town, postcode_prefix = random.choice(towns)
        street = random.choice(streets)
        property_type = random.choice(property_types)

        bedrooms = random.randint(1, 6)
        house_number = random.randint(1, 300)

        price = random.randrange(
            150000,
            1500000,
            5000
        )

        postcode = (
            f"{postcode_prefix}{random.randint(1,9)} "
            f"{random.randint(1,9)}AB"
        )

        writer.writerow([
            f"{bedrooms} Bedroom {property_type} {town}",
            f"{house_number} {street}",
            town,
            postcode,
            price
        ])

print("SUCCESS - 10,000 properties generated")