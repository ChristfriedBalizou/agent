"""Testing repository_name function
"""
from agent.handlers import repository_name


def test_repository_name():
    assert repository_name("/agent/repository/foo") == "foo"
