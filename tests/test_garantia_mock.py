from datetime import UTC, datetime, timedelta
from unittest.mock import Mock

import pytest

from src.application import GuaranteeRejected, ReservationService
from src.domain import Reservation

NOW = datetime(2026, 11, 1, 12, 0, tzinfo=UTC)


def pre():
    return Reservation(1, 1500.0, NOW + timedelta(days=5), NOW - timedelta(hours=1))


def test_guarantee_approved():
    v = Mock()
    v.is_valid.return_value = True
    r = pre()
    assert ReservationService(v).guarantee(r, "tok_demo", NOW) == "CONFIRMADA"
    v.is_valid.assert_called_once_with("tok_demo")


def test_guarantee_rejected_keeps_pre_reservation():
    v = Mock()
    v.is_valid.return_value = False
    r = pre()
    with pytest.raises(GuaranteeRejected):
        ReservationService(v).guarantee(r, "tok_demo", NOW)
    assert r.status == "PRE_RESERVA"
