from src.dataverse_client import DataverseClient

client = DataverseClient.from_environment()
token = client.get_access_token()

print("Status: 200")
print("SUCCESS - Access token received!")
print("Token length:", len(token))