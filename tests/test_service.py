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


def test_create_service():

    service = Service(os.path.join("agent", "handlers"))
    service.stop()

    assert not os.path.exists(service.location[1])
    assert os.path.exists(service.location[1])
