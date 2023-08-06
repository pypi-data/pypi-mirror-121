"""A callable script for starting a worker within the current process."""

import sys

from .commands import start_worker


try:
    queue_name = sys.argv[1]
except IndexError:
    raise RuntimeError(f"Necessary arguments not passed to {__file__}")

start_worker(queue_name)
