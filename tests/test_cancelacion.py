from datetime import UTC, datetime, timedelta

import pytest

from src.domain import Reservation

NOW = datetime(2026, 11, 1, 12, 0, tzinfo=UTC)


def make(hours_to_arrival, status="CONFIRMADA"):
    return Reservation(1, 1500.0, NOW + timedelta(hours=hours_to_arrival), NOW - timedelta(hours=1), status)


def test_cancel_72h_free():                      # éxito
    r = make(72)
    assert r.cancel(NOW) == 0
    assert r.status == "CANCELADA"


def test_cancel_with_chief_authorization_free():  # éxito (excepción)
    assert make(10).cancel(NOW, authorized_by="JEFE_RESERVACIONES") == 0


def test_cancel_late_charges_one_night():         # éxito (regla del cargo)
    assert make(10).cancel(NOW) == 1500.0


def test_cancel_already_cancelled_error():        # error
    with pytest.raises(ValueError):
        make(72, "CANCELADA").cancel(NOW)


def test_cancel_unauthorized_role_error():        # error
    with pytest.raises(PermissionError):
        make(10).cancel(NOW, authorized_by="RECEPCION")


def test_cancel_exactly_48h_free():               # límite
    assert make(48).cancel(NOW) == 0


def test_cancel_47h59_charges():                  # límite
    assert make(47.99).cancel(NOW) == 1500.0
