# Flira Dataverse Python Project

This project contains a small set of Python scripts for working with Microsoft Dataverse using the client credentials flow. It includes a shared Dataverse client, metadata lookups, and a sample property creation script.

## Project structure

- `dataverse_client.py` - shared authentication and Dataverse API wrapper
- `test_connection.py` - validates token acquisition
- `get_property_metadata.py` - lists Dataverse tables/entities
- `get_property_columns.py` - lists property-related attributes
- `create_property.py` - creates a sample property record
- `test_dataverse_client.py` - unit tests for the shared client
- `.env.example` - template for local configuration

## Prerequisites

- Python 3.9+
- Git
- Access to a Microsoft Dataverse environment
- An Azure app registration with app permissions for Dataverse

## 1. Clone the project

```bash
git clone https://github.com/Nesaganesh/flira-dataverse.git
cd flira-dataverse
```

## 2. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

## 3. Install dependencies

```bash
pip install requests python-dotenv
```

## 4. Configure environment variables

Copy the example environment file and fill in your real Dataverse values:

```bash
cp .env.example .env
```

Then edit `.env` and replace the placeholders with your values:

```env
TENANT_ID=<your-tenant-id>
CLIENT_ID=<your-app-registration-client-id>
CLIENT_SECRET=<your-app-registration-client-secret>
DATAVERSE_URL=https://<your-dataverse-env>.crm.dynamics.com
```

Important:
- Do not commit `.env`
- Keep secrets in your local environment only
- The project already ignores `.env` via `.gitignore`

## 5. Verify the setup

Run the smoke test:

```bash
python test_connection.py
```

This should print a success message if the app registration and Dataverse URL are valid.

## 6. Run the scripts

### Check Dataverse metadata

```bash
python get_property_metadata.py
```

### Check property-related columns

```bash
python get_property_columns.py
```

### Create a sample property record

```bash
python create_property.py
```

## 7. Run tests

```bash
python -m unittest test_dataverse_client.py
```

## Notes

- The shared authentication logic lives in `dataverse_client.py`.
- This project follows a generic pattern where the scripts call a reusable API class rather than writing raw `GET` or `POST` calls inline.
- If you create or update scripts, keep secrets in `.env` and never paste credentials into tracked files.

## Troubleshooting

### Authentication errors

- Check that `TENANT_ID`, `CLIENT_ID`, and `CLIENT_SECRET` are correct.
- Confirm the app registration has Dataverse API permissions and the secret is valid.
- Ensure `DATAVERSE_URL` matches your Dataverse environment.

### Import issues

```bash
pip install --upgrade pip
pip install requests python-dotenv
```

### Script not running

Make sure your virtual environment is active before running Python commands.
