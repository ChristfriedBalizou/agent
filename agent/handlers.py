import os
import sys
import shutil
import traceback
from subprocess import PIPE, Popen


BLUE = '\033[94m'
GREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'


def repository_name(repository):
    """This function take as input a path to the
    repository and output a repository directory name

    Arguments:
        repository (str): a file directory path

    Return:
        a string of the repository name
    """

    assert os.path.isdir(repository), f"{repository} should be a directory"
    return os.path.basename(repository)


class Command:
    """The command class is an Linux command line helper
    base on subprocess which handle shell command output and
    errors
    """

    def __init__(self, program: str):
        """This function will make sure the program exist
        or raise an error
        """
        self.program = shutil.which(program)
        assert self.program, f"Can't find installation of: {program}"

    def command(self, *args,  stdout=PIPE, stderr=PIPE, **kwargs):
        """Using subprocess.Popen this function will execute
        the given command line
        """

        communicate = kwargs.pop("communicate", {})
        cmd = (self.program,) + args

        with Popen(cmd, stdout=stdout, stderr=stderr, **kwargs) as proc:
            return proc.communicate(**communicate)


class Service:
    """This class will imitate the behaviour of
    a Linux service. In addition will also create
    and delete a service
    """

    def __init__(self, repository: str):
        """Initiate a ServiceController with the given repository
        Arguments:
            repository (str): a file directory path

        Return:
            a ServiceControler instance
        """

        self.name = os.path.basename(repository)
        self.repository = repository
        self.program = Command(program="systemctl")

    def status(self):
        """This function return a given
        service status.

        None: The service does not exist
        True: The service is up and running
        False: The service is disabled or not stopped
        """

        try:
            outs, errs = self.program.command("status", self.name)

            assert errs == b"", errs
            # We want to raise and exception if an error
            # occur from the command execution

            for line in outs.split("\n"):

                if "Active" not in line:
                    # We are looking for a line containing
                    # Active .* string
                    continue

                return "running" in line
                # If the command is Running or not

        except Exception as exception:

            if isinstance(exception, AssertionError):
                return None

            raise exception

    def start(self):
        raise NotImplementedError("Start function is not Yet implemented")

    def stop(self):
        raise NotImplementedError("Stop function is not Yet implemented")

    def restart(self):
        raise NotImplementedError("Restart function is not Yet implemented")


def status(service: Service):
    """This function check for a status of a given
    service and output the result
    """
    try:
        status = service.status()
    except Exception:
        traceback.print_exc(file=sys.stderr)
        sys.exit(0)

    label = f"{BLUE}Service {service.name}{ENDC}"

    if status is None:
        print(f"{label}:{FAIL} Not found.{ENDC}", file=sys.stderr)

    if status:
        print(f"{label}:{BOLD}{GREEN} Running.{ENDC}", file=sys.stdout)

    if status is False:
        print(f"{label}:{BOLD}{WARNING} Inactive.{ENDC}", file=sys.stdout)

    return status


def stop(service: Service):
    pass


def start(service: Service):
    pass


def restart(service: Service):
    pass
