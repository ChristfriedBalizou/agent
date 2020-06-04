import os
import shutil
from subprocess import PIPE, Popen


def repository_name(repository):
    """This function take as input a path to the
    repository and output a repository directory name

    Arguments:
        repository (str): a file directory path

    Return:
        a string of the repository name
    """
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


def status(repository):
    pass


def start(repository):
    pass


def stop(repository):
    pass


def restart(repository):
    pass
