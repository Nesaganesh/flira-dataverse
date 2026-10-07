import os

import requests
from dotenv import load_dotenv


class DataverseClient:
    def __init__(
        self,
        tenant_id=None,
        client_id=None,
        client_secret=None,
        dataverse_url=None,
        token=None,
    ):
        self.tenant_id = tenant_id or os.getenv("TENANT_ID")
        self.client_id = client_id or os.getenv("CLIENT_ID")
        self.client_secret = client_secret or os.getenv("CLIENT_SECRET")
        self.dataverse_url = dataverse_url or os.getenv("DATAVERSE_URL")
        self.token = token
        self.headers = {}

        if self.token:
            self.headers = self.get_headers()

    @classmethod
    def from_environment(cls):
        load_dotenv()
        return cls(
            tenant_id=os.getenv("TENANT_ID"),
            client_id=os.getenv("CLIENT_ID"),
            client_secret=os.getenv("CLIENT_SECRET"),
            dataverse_url=os.getenv("DATAVERSE_URL"),
        )

    @property
    def token_url(self):
        if not self.tenant_id:
            raise ValueError("TENANT_ID is required to authenticate with Dataverse.")
        return (
            f"https://login.microsoftonline.com/"
            f"{self.tenant_id}/oauth2/v2.0/token"
        )

    def get_access_token(self):
        if self.token:
            return self.token

        missing = [
            name
            for name, value in {
                "TENANT_ID": self.tenant_id,
                "CLIENT_ID": self.client_id,
                "CLIENT_SECRET": self.client_secret,
                "DATAVERSE_URL": self.dataverse_url,
            }.items()
            if not value
        ]

        if missing:
            raise ValueError(
                "Missing Dataverse configuration values: " + ", ".join(missing)
            )

        response = requests.post(
            self.token_url,
            data={
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "grant_type": "client_credentials",
                "scope": f"{self.dataverse_url}/.default",
            },
        )
        response.raise_for_status()

        self.token = response.json()["access_token"]
        self.headers = self.get_headers()
        return self.token

    def get_headers(self, include_content_type=False):
        token = self.get_access_token()
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
            "OData-MaxVersion": "4.0",
            "OData-Version": "4.0",
        }

        if include_content_type:
            headers["Content-Type"] = "application/json"

        return headers

    def request(self, method, url, use_auth=True, **kwargs):
        request_headers = kwargs.pop("headers", {})
        headers = self.get_headers() if use_auth else {}
        headers.update(request_headers)
        return requests.request(method, url, headers=headers, **kwargs)


class DataverseApi:
    def __init__(self, client):
        self.client = client
        self.base_url = f"{self.client.dataverse_url}/api/data/v9.2"

    def _build_url(self, path, params=None):
        url = f"{self.base_url}/{path.lstrip('/')}"
        if params:
            query = "&".join(f"{key}={value}" for key, value in params.items())
            return f"{url}?{query}"
        return url

    def fetch(self, path, params=None, **kwargs):
        url = self._build_url(path, params)
        return self.client.request("GET", url, **kwargs)

    def create(self, entity_set, payload, **kwargs):
        url = f"{self.base_url}/{entity_set.lstrip('/')}"
        return self.client.request("POST", url, json=payload, **kwargs)

    def get_property_columns(self):
        params = {
            "$select": "LogicalName,SchemaName,DisplayName,AttributeType",
        }
        return self.fetch(
            "EntityDefinitions(LogicalName='flira_property')/Attributes",
            params=params,
        )

    def get_property_metadata(self):
        params = {
            "$select": "LogicalName,SchemaName,EntitySetName",
        }
        return self.fetch("EntityDefinitions", params=params)

    def create_property(self, property_data):
        return self.create("flira_properties", property_data)

    def get_access_token(self):
        return self.client.get_access_token()
