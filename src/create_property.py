from src.dataverse_client import DataverseApi, DataverseClient

client = DataverseClient.from_environment()
api = DataverseApi(client)

api.get_access_token()
print("Authentication successful")

property_data = {
    "flira_name": "3 Bedroom House Ipswich",
    "flira_addressline1": "10 London Road",
    "flira_towncity": "Ipswich",
    "flira_postcode": "IP1 2AB",
    "flira_askingprice": 425000,
}

response = api.create_property(property_data)

print("Create Status:", response.status_code)

if response.status_code == 204:
    print("SUCCESS - Property created!")

    record_url = response.headers.get("OData-EntityId")

    if record_url:
        print("Record:", record_url)

else:
    print("FAILED")
    print(response.text)