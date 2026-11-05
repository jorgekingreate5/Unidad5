from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from src.domain import Reservation
from src.repository import SqlReservationRepository, make_engine

NOW = datetime(2026, 11, 1, 12, 0)


def sample():
    return Reservation(7, 1500.0, NOW + timedelta(days=5), NOW, "CONFIRMADA")


def test_reservation_commit():
    engine = make_engine()
    with Session(engine) as s:
        SqlReservationRepository(s).save(sample())
        s.commit()
        row = SqlReservationRepository(s).get(7)
        assert (row.id, row.night_rate, row.status) == (7, 1500.0, "CONFIRMADA")


def test_reservation_rollback():
    engine = make_engine()
    with Session(engine) as s:
        SqlReservationRepository(s).save(sample())
        s.rollback()
        assert SqlReservationRepository(s).get(7) is None
