import os
import argparse

from agent.service import Service, ServiceAction


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.HelpFormatter,
        description="""
        Generate a Linux service and cron job to handle deployment
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

    options = parser.parse_args()
    action = ServiceAction(options.action)
    repository = os.path.normpath(options.repository)
    service = Service(repository)

    if action == ServiceAction.STOP:
        service.stop()

    if action == ServiceAction.START:
        service.start()

    if action == ServiceAction.RESTART:
        service.restart()

    if action == ServiceAction.STATUS:
        service.status()
