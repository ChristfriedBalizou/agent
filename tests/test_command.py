"""This file aim to test Command class works
as expected
"""

import pytest
from agent.handlers import Command


def test_program_exist():
    """Test a given program exist
    """

    assert "ls" in Command("ls").program
    assert "cat" in Command("cat").program


def test_program_does_not_exist():
    """Test a given program is not installed
    """

    with pytest.raises(AssertionError, match=r".* installation of: foo$"):
        Command("foo")

    with pytest.raises(AssertionError, match=r".* installation of: bar$"):
        Command("bar")


def test_program_command():
    """This function will make sure a command
    is correctly executed
    """

    _, errs = Command("systemctl").command("status", "ssh")
    assert errs == ""
