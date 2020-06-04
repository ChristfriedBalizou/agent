import shutil
from subprocess import PIPE, Popen


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


def status(repository):
    pass


def start(repository):
    pass


def stop(repository):
    pass


def restart(repository):
    pass
