# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['soonq', 'soonq.commands']

package_data = \
{'': ['*'], 'soonq': ['instance/*']}

install_requires = \
['click>=7.0', 'tabulate>=0.8.9,<0.9.0']

entry_points = \
{'console_scripts': ['soonq = soonq.commands.cli:soonq']}

setup_kwargs = {
    'name': 'soonq',
    'version': '0.4.1',
    'description': 'Subprocess-based task queue.',
    'long_description': '# SoonQ\n\nA subprocess-based task queue.\n\n## Introduction\n\nSoonQ implements a simple first-in-first-out (FIFO) queue using SQLite. It was created primarily to give a user direct control over running long simulations.\n\n## Installation\n\n`pip install soonq`\n\n## Usage\n\nUsers must create their own subclass of `soonq.BaseTask`. Subclasses must define a `run()` method, which contains the business logic for the task (what we care about). Input arguments to this method are restricted to being serializable via the [pickle module](https://docs.python.org/3/library/pickle.html).\n\n## Running the examples\n\nExample files are included in the examples directory. Clone SoonQ in your desired location.\n\n`C:\\desired\\location>git clone https://github.com/n8jhj/SoonQ.git`\n\nOptionally create a virtual environment within this directory. Then navigate into the `SoonQ` directory and install it, being careful to include the dot.\n\n`pip install .`\n\nNow run the same command a couple times in a terminal to enqueue two `TimerTask`s (the source code is in the examples directory):\n\n    C:\\...\\SoonQ>soonq enq TimerTask 3 3\n    Queued task: 913d56e9-a609-4b84-b937-479a94716527\n\n    C:\\...\\SoonQ>soonq enq TimerTask 3 3\n    Queued task: da952424-98d9-42e1-8851-91a30924b94b\n\n    C:\\...\\SoonQ>\n\nYou\'ll be able to see the tasks in the queue.\n\n    C:\\...\\SoonQ>soonq view\n    +--------------------------------------+------------+----------+----------------------------+--------+--------+\n    |               task_id                | queue_name | position |         published          |  args  | kwargs |\n    +--------------------------------------+------------+----------+----------------------------+--------+--------+\n    | da952424-98d9-42e1-8851-91a30924b94b | TimerTask  |    1     | 2021-05-04 14:45:51.749038 | (3, 3) |   {}   |\n    | 913d56e9-a609-4b84-b937-479a94716527 | TimerTask  |    0     | 2021-05-04 14:45:50.658199 | (3, 3) |   {}   |\n    +--------------------------------------+------------+----------+----------------------------+--------+--------+\n\nNow begin a worker process.\n\n    C:\\...\\SoonQ>soonq run TimerTask\n\nA separate terminal will spawn to run the worker. In turn, the worker terminal will spawn task terminals as it works. So there are three levels of processes:\n\n1. The **master** process. Controls workers.\n2. The **worker** process. Runs a single worker. Can spawn tasks.\n3. The **task** process. Runs a single task.\n\nIn the task terminal you will see the runtime text:\n\n    1/3 Sleeping 3 seconds...\n    2/3 Sleeping 3 seconds...\n    3/3 Sleeping 3 seconds...\n    Slept 9 seconds total.\n\nMeanwhile, the worker terminal will show:\n\n    Running task: 913d56e9-a609-4b84-b937-479a94716527\n    Finished task: 913d56e9-a609-4b84-b937-479a94716527\n\n    Running task: da952424-98d9-42e1-8851-91a30924b94b\n    Finished task: da952424-98d9-42e1-8851-91a30924b94b\n\nWith the worker running, more tasks can be enqueued and will be processed as the worker gets to them. You can spawn more workers if you want. Enqueue more `TimerTask`s and try it out!\n\nTo stop all workers working on a certain queue at any time:\n\n    C:\\...\\SoonQ>soonq stop TimerTask\n\nThis will have each worker finish its current task and then shut down. If the `--terminate` or `-t` option is used, the workers will stop working and shut down immediately.\n\n## Etymology\n\nThis project is named after my friend Soon-Kyoo, with whom I enjoyed countless bouts of epic ping-pong in college. He goes by "Q".\n',
    'author': 'Nathaniel Jones',
    'author_email': 'nathaniel.j.jones@wsu.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/n8jhj/SoonQ',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
