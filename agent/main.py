import os
import enum
import argparse

from agent import handlers


class AgentAction(enum.Enum):
    """This class is a simple enumeration
    of the possible action to perform by the agent
    """

    STATUS = "status"
    START = "start"
    STOP = "stop"
    RESTART = "RESTART"


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
    service = handlers.Service(repository)

    if action == AgentAction.STOP:
        service.stop()

    if action == AgentAction.START:
        service.start()

    if action == AgentAction.RESTART:
        service.restart()

    if action == AgentAction.STATUS:
        service.status()
