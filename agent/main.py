import os
import argparse

from agent.service import Service, ServiceAction


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.HelpFormatter,
        description="""
        Generate a Linux service to handle deployment
        of a given repository
        """
    )

    parser.add_argument(
        "--repository",
        required=True,
        help="The path to the repository directory to handle"
    )

    parser.add_argument(
        "--action",
        choices=(
            "status",
            "start",
            "stop",
            "restart",
        )
    )

    parser.add_argument(
        "--service-type",
        choices=("simple"),
        default="simple",
        help="""
        The type of service to create please visit systemd service
        In you choose notify you must create a notify function every
        5s.
        """
    )

    options = parser.parse_args()
    action = ServiceAction(options.action)
    repository = os.path.normpath(options.repository)
    service = Service(repository, service=options.service_type)

    if action == ServiceAction.STOP:
        service.stop()

    if action == ServiceAction.START:
        service.start()

    if action == ServiceAction.RESTART:
        service.restart()

    if action == ServiceAction.STATUS:
        service.status()
