from src.dataverse_client import DataverseApi, DataverseClient

client = DataverseClient.from_environment()
api = DataverseApi(client)
api.get_access_token()
print("Authentication successful")

response = api.get_property_metadata()

print("Metadata Status:", response.status_code)
response.raise_for_status()

tables = response.json()["value"]

print("\nProperty tables found:")

for table in tables:
    logical_name = table.get("LogicalName", "")
    schema_name = table.get("SchemaName", "")
    entity_set = table.get("EntitySetName", "")

    if "property" in logical_name.lower() or "property" in schema_name.lower():
        print("\n---------------------------")
        print("Logical Name :", logical_name)
        print("Schema Name  :", schema_name)
        print("Entity Set   :", entity_set)