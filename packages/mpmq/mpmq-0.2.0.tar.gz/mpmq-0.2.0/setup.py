#!/usr/bin/env python
#   -*- coding: utf-8 -*-

from setuptools import setup
from setuptools.command.install import install as _install

class install(_install):
    def pre_install_script(self):
        pass

    def post_install_script(self):
        pass

    def run(self):
        self.pre_install_script()

        _install.run(self)

        self.post_install_script()

if __name__ == '__main__':
    setup(
        name = 'mpmq',
        version = '0.2.0',
        description = 'Mpmq is an abstraction of the Python multiprocessing library providing execution pooling and message queuing capabilities.',
        long_description = '# mpmq #\n[![GitHub Workflow Status](https://github.com/soda480/mpmq/workflows/build/badge.svg)](https://github.com/soda480/mpmq/actions)\n[![Code Coverage](https://codecov.io/gh/soda480/mpmq/branch/main/graph/badge.svg?token=SAEJLS4FCM)](https://codecov.io/gh/soda480/mpmq)\n[![Code Grade](https://www.code-inspector.com/project/12270/status/svg)](https://frontend.code-inspector.com/project/12270/dashboard)\n[![PyPI version](https://badge.fury.io/py/mpmq.svg)](https://badge.fury.io/py/mpmq)\n[![python](https://img.shields.io/badge/python-3.9-teal)](https://www.python.org/downloads/)\n\nMpmq is an abstraction of the Python multiprocessing library providing execution pooling and message queuing capabilities. Mpmq can scale execution of a specified function across multiple background processes. It creates a log handler that sends all log messages from the running processes to a thread-safe queue. The main process reads the messages off the queue for processing. The number of processes along with the arguments to provide each process is specified as a list of dictionaries. The number of elements in the list will dictate the total number of processes to execute. The result of each function is read from the result queue and written to the respective dictionary element upon completion.\n\nThe main features are:\n\n* execute function across multiple processes\n* queue function execution\n* create log handler that sends function log messages to thread-safe message queue\n* process messages from log message queue\n* maintain result of all executed functions\n* terminate execution using keyboard interrupt\n\n\n### Installation ###\n```bash\npip install mpmq\n```\n\n### Examples ###\n\nA simple example using mpmq:\n\n```python\nfrom mpmq import MPmq\nimport sys, logging\nlogger = logging.getLogger(__name__)\nlogging.basicConfig(\n    stream=sys.stdout,\n    level=logging.INFO,\n    format="%(asctime)s %(processName)s [%(funcName)s] %(levelname)s %(message)s")\n\ndef do_work(*args):\n    logger.info(f"hello from process {args[0][\'pid\']}")\n    return 10 + int(args[0][\'pid\'])\n\nprocess_data = [{\'pid\': item} for item in range(3)]\nMPmq(function=do_work, process_data=process_data).execute()\nprint(f"Total items processed {sum([item[\'result\'] for item in process_data])}")\n ```\n\nExecuting the code above results in the following (for conciseness only INFO level messages are shown):\n\n```Python\nMainProcess [start_next_process] INFO started background process at offset:0 with id:1967 name:Process-1\nMainProcess [start_next_process] INFO started background process at offset:1 with id:1968 name:Process-2\nProcess-1 [do_work] INFO hello from process 0\nMainProcess [start_next_process] INFO started background process at offset:2 with id:1969 name:Process-3\nMainProcess [start_processes] INFO started 3 background processes\nProcess-1 [_queue_handler] DEBUG adding \'do_work\' offset:0 result to result queue\nProcess-1 [_queue_handler] DEBUG execution of do_work offset:0 ended\nProcess-1 [_queue_handler] DEBUG DONE\nMainProcess [remove_active_process] INFO process at offset:0 id:1967 name:Process-1 has completed\nProcess-2 [do_work] INFO hello from process 1\nProcess-3 [do_work] INFO hello from process 2\nProcess-2 [_queue_handler] DEBUG adding \'do_work\' offset:1 result to result queue\nProcess-3 [_queue_handler] DEBUG adding \'do_work\' offset:2 result to result queue\nProcess-2 [_queue_handler] DEBUG execution of do_work offset:1 ended\nProcess-2 [_queue_handler] DEBUG DONE\nProcess-3 [_queue_handler] DEBUG execution of do_work offset:2 ended\nProcess-3 [_queue_handler] DEBUG DONE\nMainProcess [process_control_message] INFO the to process queue is empty\nMainProcess [remove_active_process] INFO process at offset:1 id:1968 name:Process-2 has completed\nMainProcess [process_control_message] INFO the to process queue is empty\nMainProcess [remove_active_process] INFO process at offset:2 id:1969 name:Process-3 has completed\nMainProcess [process_control_message] INFO the to process queue is empty\nMainProcess [run] INFO there are no more active processses - quitting\nMainProcess [join_processes] INFO joined process at offset:0 with id:1967 name:Process-1\nMainProcess [join_processes] INFO joined process at offset:1 with id:1968 name:Process-2\nMainProcess [join_processes] INFO joined process at offset:2 with id:1969 name:Process-3\n>>> print(f"Total items processed {sum([item[\'result\'] for item in process_data])}")\nTotal items processed 33\n```\n\n### Projects using `mpmq` ###\n\n* [`mpcurses`](https://pypi.org/project/mpcurses/) An abstraction of the Python curses and multiprocessing libraries providing function execution and runtime visualization capabilities\n\n* [`mp4ansi`](https://pypi.org/project/mp4ansi/) A simple ANSI-based terminal emulator that provides multi-processing capabilities.\n\n### Development ###\n\nClone the repository and ensure the latest version of Docker is installed on your development server.\n\nBuild the Docker image:\n```sh\ndocker image build \\\n-t \\\nmpmq:latest .\n```\n\nRun the Docker container:\n```sh\ndocker container run \\\n--rm \\\n-it \\\n-v $PWD:/code \\\nmpmq:latest \\\n/bin/sh\n```\n\nExecute the build:\n```sh\npyb -X\n```\n',
        long_description_content_type = 'text/markdown',
        classifiers = [
            'Development Status :: 4 - Beta',
            'Environment :: Console',
            'Environment :: Console :: Curses',
            'Environment :: Other Environment',
            'Intended Audience :: Developers',
            'Intended Audience :: System Administrators',
            'License :: OSI Approved :: Apache Software License',
            'Operating System :: POSIX :: Linux',
            'Programming Language :: Python',
            'Programming Language :: Python :: 3.9',
            'Topic :: Software Development :: Libraries',
            'Topic :: Software Development :: Libraries :: Python Modules',
            'Topic :: System :: Networking',
            'Topic :: System :: Systems Administration'
        ],
        keywords = '',

        author = 'Emilio Reyes',
        author_email = 'emilio.reyes@intel.com',
        maintainer = '',
        maintainer_email = '',

        license = 'Apache License, Version 2.0',

        url = 'https://github.com/soda480/mpmq',
        project_urls = {},

        scripts = [],
        packages = ['mpmq'],
        namespace_packages = [],
        py_modules = [],
        entry_points = {},
        data_files = [],
        package_data = {},
        install_requires = [],
        dependency_links = [],
        zip_safe = True,
        cmdclass = {'install': install},
        python_requires = '',
        obsoletes = [],
    )
