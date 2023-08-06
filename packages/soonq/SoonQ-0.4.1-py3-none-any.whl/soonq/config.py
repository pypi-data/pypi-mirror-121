"""Configuration variables.
"""

from collections import OrderedDict as ODict
import pathlib


# Database location.
here = pathlib.Path(__file__)
DB_PATH = here.parent / "instance" / "queue.sqlite"

# Database schema.
# NOTE: Changing this configuration will not change the database schema.
# In order to do so, the database must be re-initialized.
QUEUE_TABLENAME = "queue"
WORK_TABLENAME = "work"
WORKER_TABLENAME = "worker"
SCHEMA = ODict(
    [
        (
            QUEUE_TABLENAME,
            ODict(
                task_id="TEXT PRIMARY KEY NOT NULL",
                queue_name="TEXT",
                position="INTEGER UNIQUE NOT NULL",
                published="TIMESTAMP NOT NULL",
                args="BLOB",
                kwargs="BLOB",
            ),
        ),
        (
            WORK_TABLENAME,
            ODict(
                task_id="TEXT PRIMARY KEY NOT NULL",
                queue_name="TEXT",
                started="TIMESTAMP NOT NULL",
                status="TEXT",
                args="BLOB",
                kwargs="BLOB",
                err="TEXT",
            ),
        ),
        (
            WORKER_TABLENAME,
            ODict(
                worker_id="TEXT PRIMARY KEY NOT NULL",
                queue_name="TEXT",
                started="TIMESTAMP NOT NULL",
                status="INTEGER NOT NULL",
                task_id="TEXT",
                directive="INTEGER NOT NULL",
            ),
        ),
    ]
)

# Tabulate formatting.
TABULATE_FORMATTING = dict(
    tablefmt="pretty",
)
