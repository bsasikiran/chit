from getpass import getpass
import sys

from chit_store import EncryptedHouseholdStore
from chit_store.auth import OwnerAuth


def main() -> int:
    auth = OwnerAuth(EncryptedHouseholdStore())
    if auth.is_configured():
        print("The household owner account is already configured.", file=sys.stderr)
        return 1
    username = input("Owner username: ").strip()
    password = getpass("Owner password (minimum 12 characters): ")
    confirmation = getpass("Confirm owner password: ")
    if password != confirmation:
        print("Passwords did not match.", file=sys.stderr)
        return 1
    try:
        auth.create_owner(username, password)
    except ValueError as error:
        print(str(error), file=sys.stderr)
        return 1
    print("Owner account created. Start Chit and sign in with that username and password.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
