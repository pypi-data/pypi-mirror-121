"""Implements task classes.

Classes:
BaseTask - Base task class.
"""

import abc
import pickle
import uuid

from .broker import Broker
from .utils import echo


class BaseTask(abc.ABC):
    """Base task class.

    Example Usage:
        class AdderTask(BaseTask):
            def run(self, a, b):
                result = a + b
                return result

        adder = AdderTask()
        adder.delay(9, 34)
    """

    # Status options are:
    #   detached - Instantiated, not queued.
    #   enqueued - Queued via Broker.
    #   dequeued - Dequeued via Worker.
    #   running - Running via Worker.
    #   error - Exception encountered during run.
    #   complete - Run complete.
    _status_options = (
        "detached",
        "enqueued",
        "dequeued",
        "running",
        "error",
        "complete",
    )

    def __init__(self):
        self.broker = Broker()
        self.set_status("detached")

    @property
    def task_name(self):
        return type(self).__name__

    def scrub_inputs(self, args, kwargs):
        """Subclasses can override. By default, this does nothing."""
        return args, kwargs

    @abc.abstractmethod
    def run(self, *args, **kwargs):
        """Subclasses must implement their business logic here."""
        pass

    def delay(self, *args, **kwargs):
        """Have the broker enqueue this task, thereby delaying its
        execution until some future time.
        """
        args, kwargs = self.scrub_inputs(args, kwargs)
        try:
            self.task_id = str(uuid.uuid4())
            task = dict(
                task_id=self.task_id,
                args=args,
                kwargs=kwargs,
            )
            self.broker.enqueue(item=task, queue_name=self.task_name)
            self.set_status("enqueued")
            echo(f"Queued task: {self.task_id}")
        except Exception:
            raise RuntimeError(
                f"Unable to publish task {self.task_id} to the broker."
            )

    def dequeue(self):
        """Dequeue one task of this type."""
        item = self.broker.dequeue(queue_name=self.task_name)
        try:
            self.task_id = item["task_id"]
        except TypeError:
            self.task_id = None
        return item

    def slate(self, args, kwargs):
        """Add this task to the work table with the given arguments and
        keyword arguments.
        """
        self.broker.add_work(self, "running", args, kwargs)

    def set_status(self, status):
        """Set status of the BaseTask instance."""
        if status not in self._status_options:
            raise ValueError(f"Task status {status!r} not recognized.")
        self.status = status
        if status == "complete":
            self.broker.update_status(self, status)
            self.broker.remove_work(self)

    def record_exc(self, tb_text):
        """Record the given traceback information."""
        self.broker.update_exc_info(self, tb_text)

    def __repr__(self):
        return f"<{self.__class__.__name__}(status={self.status})>"
