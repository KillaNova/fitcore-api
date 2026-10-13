"""Keep the database password encrypted in the OS keyring, not in a file.

On Windows it is stored in Credential Manager, encrypted with your Windows
login. Save or change it once with:

    python db_password.py
"""
import keyring
from keyring.errors import KeyringError

SERVICE = "fitcore-api"
USERNAME = "database"


def get_password() -> str | None:
    try:
        return keyring.get_password(SERVICE, USERNAME)
    except KeyringError:
        # No keyring available (e.g. a Linux server); fall back to .env.
        return None


if __name__ == "__main__":
    import getpass

    password = getpass.getpass("Database password: ")
    if not password:
        raise SystemExit("No password entered, nothing saved.")
    keyring.set_password(SERVICE, USERNAME, password)
    print("Password saved encrypted in your OS keyring.")
