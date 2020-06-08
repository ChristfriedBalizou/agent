"""Test all services features
"""
import os

from agent.handlers import (
    ServiceStat,
    Service,
    status,
)


def test_service_does_not_exists():
    service = Service(os.path.join("agent", "handlers"))
    assert status(service) == ServiceStat.NONEXISTENT
