import pytest

from src.domain import CreditLimitExceeded, RoomAccount


def test_charge_1000_ok():                        # éxito
    a = RoomAccount()
    a.add_charge(1000, "recepcion-01")
    assert a.balance == 1000
    assert a.charges == [("recepcion-01", 1000)]


def test_charge_over_limit_rejected():            # error
    a = RoomAccount()
    with pytest.raises(CreditLimitExceeded):
        a.add_charge(3500, "recepcion-01")
    assert a.balance == 0


def test_charge_zero_or_negative_error():         # error
    with pytest.raises(ValueError):
        RoomAccount().add_charge(0, "recepcion-01")


def test_charge_exactly_3000_ok():                # límite
    a = RoomAccount()
    a.add_charge(3000, "recepcion-01")
    assert a.balance == 3000


def test_charge_3000_01_rejected():               # límite
    a = RoomAccount(balance=3000)
    with pytest.raises(CreditLimitExceeded):
        a.add_charge(0.01, "recepcion-01")


def test_admin_authorization_allows_excess():     # éxito
    a = RoomAccount(balance=2900)
    a.add_charge(500, "recepcion-01", admin_authorized=True)
    assert a.balance == 3400


def test_partial_payment_then_charge():           # éxito
    a = RoomAccount(balance=3000)
    a.partial_payment(1000)
    a.add_charge(500, "recepcion-01")
    assert a.balance == 2500
