# Local encrypted datastore

The datastore is a local Python repository backed by SQLCipher-encrypted SQLite. It is not yet exposed through an HTTP API, and it does not implement application authentication or member authorization.

## Setup

Use Python 3.9 or newer in a project virtual environment:

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
```

Generate a development key outside the repository and provide it to the process:

```sh
export CHIT_DB_KEY_HEX="$(openssl rand -hex 32)"
export CHIT_DB_PATH="$PWD/data/chit.db"
```

The key must be exactly 32 random bytes encoded as 64 hexadecimal characters. Do not put the value in a checked-in config file, shell script, or `.env` file. For production, inject it from an operating-system secret store or deployment secret mechanism; key rotation, recovery, backups and unattended service startup need deployment-specific design.

## Create the local owner login

After the virtual environment, database key and `CHIT_DB_PATH` are set, and before starting the server, create the one local owner account once:

```sh
PYTHONPATH=server python server/bootstrap_owner.py
```

Enter a username and a password of at least 12 characters at the terminal prompts. The password is hashed with Argon2id and stored inside the encrypted database; it is not saved to a config file. Account recovery is not implemented yet.

## Start the setup page

On macOS, reload the Keychain key into the current terminal and start the loopback-only server:

```sh
source .venv/bin/activate
export CHIT_DB_KEY_HEX="$(security find-generic-password -a "$USER" -s chit-db-key -w)"
export CHIT_DB_PATH="$PWD/data/chit.db"
PYTHONPATH=server python server/run.py
```

Open <http://127.0.0.1:8765/login.html>, sign in, then open <http://127.0.0.1:8765/dashboard/household-setup.html>. The server applies pending encrypted database migrations when it starts. Submit the page once to create the household and save its members, profile settings, calendar mappings, and chore rules in one transaction. The server listens on `127.0.0.1` only; stop it with Ctrl+C.

Stop any currently running older local server with Ctrl+C before upgrading it. After the owner account has been bootstrapped, start the new server using the command above. Do not run `bootstrap_owner.py` a second time; it refuses to replace the owner account.

To preview the latest household's connected calendars on a home-style agenda, open <http://127.0.0.1:8765/dashboard/calendar-home.html>. The server reads each saved feed on page load, parses upcoming events for the next three weeks, and returns event summaries without exposing feed URLs. Calendar occurrences are not persisted; only source health and last-checked time are updated.

Initialize/use the store from Python:

```python
from chit_store import EncryptedHouseholdStore

store = EncryptedHouseholdStore()
household = store.create_household(
    name="Meyer household",
    owner_name="Nina Meyer",
    timezone_name="Europe/Berlin",
    country_code="DE",
    region="Bayern",
)
```

Set `PYTHONPATH=server` when running scripts from the repository root. The database directory is restricted to the current user where supported; the database file is created with owner-only permissions. SQLite WAL sidecars remain inside that protected directory and are encrypted by SQLCipher.

## Data boundary

Migrations live in `chit_store/migrations/` and are applied at store initialization. The schema stores household/member settings, adult work patterns, child care/activity schedules, read-only calendar subscriptions and member mappings, configured chore rules, and Chit-owned chores with assignees and provenance.

Subscribed calendar occurrences are not mirrored into an event table. A generated chore stores its source occurrence reference and generation-rule reference, and repeated ingestion updates the same chore. Completed or manually edited chores are retained without upstream overwrite.

The repository layer performs storage validation and household referential-integrity checks only. Authentication, authorization, consent and household access policy are deliberately not implemented here.

## Tests

```sh
PYTHONPATH=server python -m unittest discover -s server/tests -v
```
