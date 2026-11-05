from datetime import UTC, datetime, timedelta

import pytest

from src.domain import Reservation

NOW = datetime(2026, 11, 1, 12, 0, tzinfo=UTC)


def pre(age_hours):
    return Reservation(1, 1500.0, NOW + timedelta(days=5), NOW - timedelta(hours=age_hours))


def test_confirm_at_23h_ok():                     # éxito
    r = pre(23)
    r.confirm_with_guarantee(NOW)
    assert r.status == "CONFIRMADA"


def test_confirm_after_30h_error():               # error
    r = pre(30)
    with pytest.raises(ValueError):
        r.confirm_with_guarantee(NOW)
    assert r.status == "EXPIRADA"


def test_expires_at_exactly_24h():                # límite (supuesto: 24 h cumplidas = expirada)
    assert pre(24).expire_if_needed(NOW) == "EXPIRADA"


def test_not_expired_at_23h59():                  # límite
    assert pre(23.98).expire_if_needed(NOW) == "PRE_RESERVA"
