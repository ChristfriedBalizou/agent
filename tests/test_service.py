"""Test all services features
"""
import os

from agent.handlers import (
    ServiceStat,
    Service,
)


def test_service_does_not_exists():
    service = Service(os.path.join("agent", "handlers"))
    service.stop()

    assert service.status() == ServiceStat.NONEXISTENT
