Context
-------

The agent package aim to easily create a Linux (systemd) service.

This package will perform the following actions:

- status
- stop
- start
- restart

This package is developed for my personal use. Being working in collaboration
with some freinds we wanted to be able to deploy continuosly (prod and dev)
based on commits or tags. Docker and Kubernetes are the first which pops. We
decide to use systemd-service for the simple reason it does exactly what we need
whitout the need of installing and managing an external application. Lunix is
safer and provide all we need.

Each project must contain a Makefile with a "all" or "DEFAULT_GOAL" or "PHONY"
case. The service ExecStart will only execute:

.. code:: bash
    
    make --makefile=<path to your makefile>
    

Also You should implement a notify function which will call systemd-notify is
you choose to use a service type notify. This will automatically restart your
service when down or broken.

Note: we are working on an agent based on https://wiki.archlinux.org/index.php/systemd-nspawn.


Requirements
------------

To use this package you must:
   - Use a Linux machine (tested with debian buster)
   - The user should be chown /lib/systemd/system and /etc/systemd/system
   - Make sure you have systemd
   - python3 (tested and wrote with python3.7)
   - Your project directory must have a Makefile


Installation
------------

.. code:: bash
    
   pip install git+https://github.com/ChristfriedBalizou/agent.git#egg=agent
   
   # or
   
   git clone https://github.com/ChristfriedBalizou/agent.git
   python agent/setup.py install


Usage
-----

.. code:: bash
    
    # to get status of a service
    python agent --repository <path to your directory> --action status
    
    # to start a service
    python agent --repository <path to your directory> --action start
    
    # use --service notify or simple (default: simple) to start you service
    # Note that for notify you need to develop a notify function
    # "systemd-notify --ready" which should notify the service manager for liveness
   
.. code:: python

    from agent.service import Service, ServiceStat
    
    service = Service("your direcory")
    
    service.stop()
    assert service.status() == ServiceStat.NONEXISTENT
    
    service.start()
    assert service.status() == ServiceStat.RUNNING

::

    usage: agent [-h] --repository REPOSITORY
                 [--action {status,start,stop,restart}]
                 [--service-type {notify,simple}]

    Generate a Linux service to handle deployment of a given repository

    optional arguments:
      -h, --help            show this help message and exit
      --repository REPOSITORY
                            The path to the repository directory to handle
      --action {status,start,stop,restart}
      --service-type {notify,simple}
                            The type of service to create please visit systemd
                            service In you choose notify you must create a notify
                            function every 5s.


Service
-------

A service can be simple or notify. A notify service type will handle the health
check as described  https://www.freedesktop.org/software/systemd/man/systemd.service.html#Options

*We set a timeout of 5s second this can't be currently updated.*

- status:
  Will perform a systemctl status <your service>.

- stop:
  Will stop and delete all systemd services file created.

- start:
  Will first call stop and create systemd service file for your application.
  Will then systemd start <your service>

- restart:
  Will reproduce stop and start.
