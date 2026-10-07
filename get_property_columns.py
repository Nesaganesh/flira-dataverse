from dataverse_client import DataverseApi, DataverseClient

client = DataverseClient.from_environment()
api = DataverseApi(client)
api.get_access_token()
print("Authentication successful")

response = api.get_property_columns()

print("Column Metadata Status:", response.status_code)
response.raise_for_status()

attributes = response.json()["value"]

wanted = {
    "name",
    "address line 1",
    "town / city",
    "postcode",
    "asking price",
}

print("\nProperty columns:")
print("-" * 70)

for attribute in attributes:
    display_name = ""

    labels = attribute.get("DisplayName", {}).get("LocalizedLabels", [])

    if labels:
        display_name = labels[0].get("Label", "")

    if display_name.lower() in wanted:
        print("Display Name :", display_name)
        print("Logical Name :", attribute.get("LogicalName"))
        print("Schema Name  :", attribute.get("SchemaName"))
        print("Type         :", attribute.get("AttributeType"))
        print("-" * 70)