from sqlalchemy import Column, DateTime, Float, Integer, String, create_engine
from sqlalchemy.orm import DeclarativeBase, Session


class Base(DeclarativeBase):
    pass


class ReservationRow(Base):
    __tablename__ = "reservations"
    id = Column(Integer, primary_key=True)
    night_rate = Column(Float, nullable=False)
    arrival = Column(DateTime, nullable=False)
    created_at = Column(DateTime, nullable=False)
    status = Column(String, nullable=False)


class SqlReservationRepository:
    def __init__(self, session: Session):
        self.session = session

    def save(self, r):
        self.session.add(ReservationRow(id=r.id, night_rate=r.night_rate, arrival=r.arrival,
                                        created_at=r.created_at, status=r.status))

    def get(self, reservation_id):
        return self.session.get(ReservationRow, reservation_id)


def make_engine(url="sqlite+pysqlite:///:memory:"):
    engine = create_engine(url)
    Base.metadata.create_all(engine)
    return engine


__all__ = ["ReservationRow", "SqlReservationRepository", "make_engine"]
