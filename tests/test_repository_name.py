"""Testing repository_name function
"""
import os
import pytest

from agent.handlers import repository_name


def test_repository_name():
    assert repository_name(os.path.join(".", "agent")) == "agent"


def test_repository_is_a_directory():
    with pytest.raises(AssertionError, match=r".* be a directory"):
        repository_name(os.path.join(".", "agent", "handlers.py"))


def test_repository_is_exist():
    with pytest.raises(AssertionError):
        repository_name(os.path.join(".", "agent", "foobar"))
