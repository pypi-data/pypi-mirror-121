"""Contains commands that can be used within other Python modules. This is particularly
useful for initializing subprocesses, since only a Python interpreter executable is
required, rather than a particular command line implementation. (For example, think of
Poetry, which requires prefixing commands with "poetry run" to have access to the
virtual environment.)

Classes:
QueueItem
WorkItem

Functions:
clear_queue - Clear the queue.
clear_work - Clear the table of work.
task_items - Info about items in the queue.
tabulate_task_items - Tabulate info about items in the queue.
work_items - Info about items in the table of work.
run_work - Run a given BaseTask instance.
start_worker - Start a Worker in the current process.
stop_all_workers - Stop all Workers working on a given queue.
"""

import pickle
import sqlite3

from soonq.config import (
    DB_PATH, QUEUE_TABLENAME, WORK_TABLENAME, WORKER_TABLENAME,
)
from soonq.utils import echo, get_taskclass, tabulate_data
from soonq.worker import Worker


# TODO: Dynamically create QueueItem and WorkItem classes based on
# configured database column names.
# This will also involve updating __repr__ to dynamically reference the
# signature of __init__.


class QueueItem:
    def __init__(self, task_id, queue_name, position, published, args, kwargs):
        self.task_id = task_id
        self.queue_name = queue_name
        self.position = position
        self.published = published
        self.args = pickle.loads(args)
        self.kwargs = pickle.loads(kwargs)

    @classmethod
    def from_tuple(cls, tuple_):
        return cls(*tuple_)

    @classmethod
    def fields(cls):
        """A list of fields."""
        return [
            "task_id", "queue_name", "position", "published", "args", "kwargs"
        ]

    def __repr__(self):
        return "QueueItem({}={}, {}={}, {}={}, {}={}, {}={}, {}={})".format(
            "task_id",
            self.task_id,
            "queue_name",
            self.queue_name,
            "position",
            self.position,
            "published",
            self.published,
            "args",
            self.args,
            "kwargs",
            self.kwargs,
        )


class WorkItem:
    def __init__(
        self,
        task_id,
        queue_name,
        started,
        status,
        args,
        kwargs,
        err,
    ):
        self.task_id = task_id
        self.queue_name = queue_name
        self.started = started
        self.status = status
        self.args = args
        self.kwargs = kwargs
        self.err = err

    @classmethod
    def from_tuple(cls, tuple_):
        return cls(*tuple_)

    @classmethod
    def fields(cls):
        """A list of fields."""
        return [
            "task_id",
            "queue_name",
            "started",
            "status",
            "args",
            "kwargs",
            "err",
        ]

    def __repr__(self):
        return (
            "WorkItem({}={}, {}={}, {}={}, {}={}, {}={}, {}={}, {}={})".format(
                "task_id",
                self.task_id,
                "queue_name",
                self.queue_name,
                "started",
                self.started,
                "status",
                self.status,
                "args",
                self.args,
                "kwargs",
                self.kwargs,
                "err",
                "..." if self.err else "''",
            )
        )


def clear_queue():
    """Clear the task queue."""
    con = sqlite3.connect(str(DB_PATH))
    with con:
        con.execute(
            f"""
            DELETE FROM {QUEUE_TABLENAME}
            """
        )
    con.close()
    echo("Cleared the queue.")


def clear_work():
    """Clear the table of work."""
    con = sqlite3.connect(str(DB_PATH))
    with con:
        con.execute(
            f"""
            DELETE FROM {WORK_TABLENAME}
            """
        )
    con.close()
    echo("Cleared table of work.")


def task_items(max_entries=None):
    """Information about the items in the task queue. Returns a
    generator of QueueItems.

    Keyword arguments:
    max_entries - (int) (Default: None) Maximum number of items to
        return. Default is to return all entries.
    """
    con = sqlite3.connect(str(DB_PATH))
    with con:
        c = con.execute(
            f"""
            SELECT task_id, queue_name, position, published, args, kwargs
            FROM {QUEUE_TABLENAME}
            ORDER BY position DESC
            """
        )
    if max_entries:
        items = map(QueueItem.from_tuple, c.fetchmany(size=max_entries))
    else:
        items = map(QueueItem.from_tuple, c.fetchall())
    con.close()
    return items


def tabulate_task_items(*args, **kwargs):
    """Return a string containing tabulated data about task items."""
    tasks = task_items(*args, **kwargs)
    headers = QueueItem.fields()
    data = [
        [getattr(task, h) for h in headers]
        for task in tasks
    ]
    return tabulate_data(data, headers=headers)


def work_items(max_entries=None):
    """Information about the items in the work queue. Returns a
    generator of WorkItems.

    Keyword arguments:
    max_entries - (int) (Default: None) Maximum number of items to
        return. Default is to return all entries.
    """
    con = sqlite3.connect(str(DB_PATH))
    with con:
        c = con.execute(
            f"""
            SELECT
                task_id,
                queue_name,
                started,
                status,
                args,
                kwargs,
                err
            FROM {WORK_TABLENAME}
            ORDER BY started ASC
            """
        )
    if max_entries:
        items = map(WorkItem.from_tuple, c.fetchmany(size=max_entries))
    else:
        items = map(WorkItem.from_tuple, c.fetchall())
    con.close()
    return items

def remove_work(self, task):
    """Remove the given task from the work table."""
    con = sqlite3.connect(str(DB_PATH))
    with con:
        con.execute(
            f"""
            DELETE FROM {WORK_TABLENAME}
            WHERE task_id = ?
            """,
            (task.task_id,),
        )
    con.close()


def run_work(task_clsname, task_id):
    """Run the task in the work table with the given ID."""
    # Get task from work table.
    con = sqlite3.connect(str(DB_PATH))
    with con:
        c = con.execute(
            f"""
            SELECT
                task_id,
                queue_name,
                started,
                status,
                args,
                kwargs,
                err
            FROM {WORK_TABLENAME}
            WHERE task_id = ?
            """,
            (task_id,),
        )
        _, _, _, _, task_args, task_kwargs, _ = c.fetchone()
    con.close()
    # Run task.
    task_args = pickle.loads(task_args)
    task_kwargs = pickle.loads(task_kwargs)
    exc_info = None
    task = get_taskclass(task_clsname)()
    task.run(*task_args, **task_kwargs)
    return exc_info


def start_worker(queue_name):
    """Start a worker on the named queue in the current process."""
    task_cls = get_taskclass(queue_name)
    inst = task_cls()
    worker = Worker(inst)
    worker.start()


def stop_all_workers(queue_name, terminate=False):
    """Stop all Workers working on the named queue.

    Positional arguments:
    queue_name - (str) Queue name to stop work on.

    Keyword arguments:
    terminate - (bool) (Default: False) Whether to immediately terminate
        the currently running task.
    """
    con = sqlite3.connect(str(DB_PATH))
    with con:
        con.execute(
            f"""
            UPDATE {WORKER_TABLENAME}
            SET directive = ?
            WHERE queue_name = ?
            """,
            (
                Worker.DRV_TERM if terminate else Worker.DRV_QUIT,
                queue_name,
            ),
        )
    con.close()
