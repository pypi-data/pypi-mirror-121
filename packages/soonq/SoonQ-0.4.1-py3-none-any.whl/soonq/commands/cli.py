"""Command line interface.

Command groups:
soonq
    clear
    view
    enq
    worker
    run
    stop
"""

import click

from .commands import (
    clear_queue,
    tabulate_task_items,
    start_worker,
    stop_all_workers,
)
from ..utils import get_taskclass
from ..worker import start_worker_process, Worker


@click.group()
def soonq():
    """SoonQ: Subprocess-based queueing."""
    pass


@soonq.command()
@click.confirmation_option(prompt="Clear the entire queue?")
def clear():
    """Clear the queue."""
    clear_queue()


@soonq.command()
@click.option(
    "-a/-A",
    "--all-entries/--head-only",
    default=False,
    show_default=True,
    help="Whether to show all entries.",
)
def view(all_entries):
    """View tasks in the queue."""
    max_entries = None if all_entries else 5
    click.echo(tabulate_task_items(max_entries=max_entries))


@soonq.command()
@click.argument("queue_name")
@click.argument("args", nargs=-1)
def enq(queue_name, args):
    """Enqueue a single task in the named queue."""
    task_cls = get_taskclass(queue_name)
    inst = task_cls()
    inst.delay(*args)


@soonq.command()
@click.argument("queue_name")
def worker(queue_name):
    """Start a worker on the named queue in the current process."""
    start_worker(queue_name)


@soonq.command()
@click.argument("queue_name")
def run(queue_name):
    """Spawn a worker on the named queue."""
    start_worker_process(queue_name)


@soonq.command()
@click.argument("queue_name")
@click.option(
    "-t",
    "--terminate",
    is_flag=True,
    help="Whether to immediately terminate the currently running task.",
)
def stop(queue_name, terminate):
    """Stop all Workers on the named task."""
    stop_all_workers(queue_name, terminate)
