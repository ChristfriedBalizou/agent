import os
import enum
import shutil
from subprocess import PIPE, Popen


BLUE = '\033[94m'
GREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'


BASE_DIRECTORY = os.path.dirname(os.path.realpath(__file__))


class AgentAction(enum.Enum):
    """This class is a simple enumeration
    of the possible action to perform by the agent
    """

    STATUS = "status"
    START = "start"
    STOP = "stop"
    RESTART = "RESTART"



class ServiceStat(enum.Enum):
    """Enumeration of service possible state
    """

    NONEXISTENT = None
    RUNNING = True
    INACTIVE = False


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


def pprint(func):
    """This function aim to print the output of the cli command
    """
    def wrapper(*args, **kwargs):
        outs, errs = func(*args, **kwargs)

        if not outs:
            # YOLO just don't wanted to have a nested for loop
            return outs, errs

        for line in outs.split("\n"):
            print(line)

        return outs, errs

    return wrapper


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

    @pprint
    def command(self, *args,  stdout=PIPE, stderr=PIPE, **kwargs):
        """Using subprocess.Popen this function will execute
        the given command line
        """

        communicate = kwargs.pop("communicate", {})
        cmd = (self.program,) + args

        with Popen(cmd,
                   stdout=stdout,
                   stderr=stderr,
                   encoding="utf8",
                   **kwargs) as proc:
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
        self.location = (
            f"/lib/systemd/system/{self.name}.service",
            "/etc/systemd/system/{self.name}.service",
        )

    def status(self) -> ServiceStat:
        """This function return a given
        service status.

        None: The service does not exist
        True: The service is up and running
        False: The service is disabled or not stopped
        """

        try:
            outs, errs = self.program.command("status", self.name)

            assert errs == "", errs
            # We want to raise and exception if an error
            # occur from the command execution

            for line in outs.split("\n"):

                if "Active" not in line:
                    # We are looking for a line containing
                    # Active .* string
                    continue

                if "running" in line:
                    return ServiceStat.RUNNING

                return ServiceStat.INACTIVE
                # If the command is Running or not

        except Exception as exception:

            if isinstance(exception, AssertionError):
                return ServiceStat.NONEXISTENT

            raise exception

    def start(self):
        """This function will create a new service for the
        current repository
        """

        self.stop()
        # First we want to start stopping the service
        # which will clean an remove any other thing

        with open(os.path.join(BASE_DIRECTORY, "service.template")) as output:
            template = output.read().format(
                description=f"Service {self.name}",
                makefile=os.path.join(self.repository, "Makefile")
            )

        with open(self.location[0], "w") as out:
            out.write(template)

        shutil.copy(*self.location)
        os.chmod(self.location[1], 644)

        self.program.command("start", self.name)

    def stop(self):
        """This function aim to stop a service
        and completely clear the service files

        The next status of a stopped service will be ServiceStat.NONEXISTENT
        """
        if self.status() == ServiceStat.NONEXISTENT:
            # There is nothing to at this state
            # the service does not even exist
            return

        if self.status() == ServiceStat.RUNNING:
            # The service is running and we need
            # to stop it
            self.program.command("stop", self.name)

        if os.path.exists(self.location[0]):
            os.remove(self.location[0])

        if os.path.exists(self.location[1]):
            os.remove(self.location[1])

    def restart(self):
        """This function will simply call the stop and the start function
        """
        self.stop()
        self.start()
