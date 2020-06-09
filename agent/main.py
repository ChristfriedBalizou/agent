import os
import argparse

from agent.service import Service, AgentAction


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
    action = AgentAction(options.action)
    repository = os.path.normpath(options.repository)
    service = Service(repository)

    if action == AgentAction.STOP:
        service.stop()

    if action == AgentAction.START:
        service.start()

    if action == AgentAction.RESTART:
        service.restart()

    if action == AgentAction.STATUS:
        service.status()
