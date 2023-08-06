"""Implements worker classes.

Classes:
Worker

Functions:
start_worker_process - Start a Worker on a given queue.
"""

import datetime as dt
import platform
import sqlite3
from subprocess import Popen, TimeoutExpired, CREATE_NEW_CONSOLE, PIPE
import sys
import uuid

from .utils import echo
from .config import DB_PATH, WORKER_TABLENAME


class Worker:
    """Basic worker class.

    Example Usage:
        task = AdderTask()
        worker = Worker(task=task)
        worker.start()
    """

    # Directive codes.
    DRV_WORK = 0  # Keep working.
    DRV_QUIT = 7  # Quit (when finished with current task).
    DRV_TERM = 8  # Terminate (now).
    # Status codes.
    STA_WAIT = 0  # Waiting for next task.
    STA_WORK = 1  # Working on a task.

    def __init__(self, task, comm_timeout=1):
        """A Worker instance.

        Positional arguments:
        task - (BaseTask) Task instance whose queue should be worked on.

        Keyword arguments:
        comm_timeout - (float) (Default: 1) Number of seconds to wait
            for communication with task process at each polling.
        """
        self.task = task
        self.comm_timeout = comm_timeout
        self.worker_id = str(uuid.uuid4())
        # Until cleanup happens, the instance will remain alive.
        self.alive = True
        self.task_subp = None
        self._register()

    def _register(self):
        con = sqlite3.connect(str(DB_PATH))
        with con:
            con.execute(
                f"""
                INSERT INTO {WORKER_TABLENAME} (
                    worker_id,
                    queue_name,
                    started,
                    status,
                    directive
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    self.worker_id,
                    self.task.task_name,
                    dt.datetime.now(),
                    self.STA_WAIT,
                    self.DRV_WORK,
                ),
            )
        con.close()

    @property
    def started(self):
        return self._get_dbinfo("started")

    @started.setter
    def started(self, value):
        return self._set_dbinfo("started", value)

    @property
    def waiting(self):
        return self._get_dbinfo("status") == self.STA_WAIT

    @waiting.setter
    def waiting(self, value):
        return self._set_dbinfo("status", value == self.STA_WAIT)

    @property
    def directive(self):
        return self._get_dbinfo("directive")

    def _get_dbinfo(self, col):
        con = sqlite3.connect(str(DB_PATH))
        with con:
            c = con.execute(
                f"""
                SELECT {col}
                FROM {WORKER_TABLENAME}
                WHERE worker_id = ?
                """,
                (self.worker_id,),
            )
            info = c.fetchone()[0]
        con.close()
        return info

    def _set_dbinfo(self, col, value):
        con = sqlite3.connect(str(DB_PATH))
        with con:
            con.execute(
                f"""
                UPDATE {WORKER_TABLENAME}
                SET {col} = ?
                WHERE worker_id = ?
                """,
                (value, self.worker_id),
            )
        con.close()

    def start(self):
        """Begin working on the assigned type of task."""
        while self.alive and self.directive == self.DRV_WORK:
            try:
                # Read database.
                dequeued_item = self.task.dequeue()
                if not dequeued_item:
                    if not self.waiting:
                        self.waiting = True
                        echo(f"Waiting for next task...\n")
                    continue
                self.waiting = False
                self.task.set_status("dequeued")
                task_id, _, _, _, task_args, task_kwargs = dequeued_item
                # Run.
                self.task.slate(task_args, task_kwargs)
                echo(f"Running task: {task_id}")
                # Pass off execution to subprocess.
                exc_txt = self.subprocess_run(task_id)
                if exc_txt:
                    echo(f"Error in task: {task_id}\n")
                    self.task.set_status("error")
                    self.task.record_exc(exc_txt)
                else:
                    echo(f"Finished task: {task_id}\n")
                    self.task.set_status("complete")
            except KeyboardInterrupt:
                self.terminate()
                break
        else:
            if self.alive and self.directive == self.DRV_QUIT:
                self.quit()

    def subprocess_run(self, task_id):
        popen_kwargs = dict(
            args=[
                # To use the same interpreter as the current process, use
                # sys.executable.
                # https://stackoverflow.com/a/27123973/7232335
                sys.executable,
                "-m",
                "soonq.commands.run_task",
                self.task.task_name,
                str(task_id),
            ],
        )
        if platform.system() == "Windows":
            popen_kwargs["creationflags"] = CREATE_NEW_CONSOLE
        else:
            # "If shell is True, it is recommended to pass args as a
            # string rather than as a sequence."
            # https://docs.python.org/3/library/subprocess.html#subprocess.Popen
            popen_kwargs["args"] = " ".join(popen_kwargs["args"])
            popen_kwargs["shell"] = True
        popen_kwargs["stdin"] = PIPE
        popen_kwargs["stderr"] = PIPE
        popen_kwargs["universal_newlines"] = True
        # Poll for task completion and further directives.
        self.task_subp = Popen(**popen_kwargs)
        errs = None
        while True:
            # Poll for completion.
            try:
                outs, errs = self.task_subp.communicate(
                    timeout=self.comm_timeout
                )
                break
            except TimeoutExpired:
                pass
            # Look for directives.
            if self.directive == self.DRV_TERM:
                self.terminate()
                break
        self.task_subp = None
        return errs

    def cleanup(self):
        """Remove self from database."""
        con = sqlite3.connect(str(DB_PATH))
        with con:
            con.execute(
                f"""
                DELETE FROM {WORKER_TABLENAME}
                WHERE worker_id = ?
                """,
                (self.worker_id,),
            )
        con.close()
        self.alive = False

    def quit(self):
        """Stop working."""
        echo("Quitting")
        self.cleanup()

    def terminate(self):
        """Terminate self and running task."""
        echo("Terminating")
        if self.task_subp:
            self.task_subp.terminate()
        self.cleanup()


def start_worker_process(queue_name):
    """Start a process with a Worker on the queue of the given name."""
    popen_kwargs = dict(
        args=[sys.executable, "-m", "soonq.commands.start_worker", queue_name],
    )
    if platform.system() == "Windows":
        popen_kwargs["creationflags"] = CREATE_NEW_CONSOLE
    else:
        # "If shell is True, it is recommended to pass args as a
        # string rather than as a sequence."
        # https://docs.python.org/3/library/subprocess.html#subprocess.Popen
        popen_kwargs["args"] = " ".join(popen_kwargs["args"])
        popen_kwargs["shell"] = True
    popen_kwargs["universal_newlines"] = True
    # Poll for task completion and further directives.
    Popen(**popen_kwargs)
