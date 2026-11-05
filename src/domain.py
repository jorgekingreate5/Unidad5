"""Reglas del BRD de Hotel Costa Azul (MXN). Sin dependencias externas."""
from dataclasses import dataclass, field
from datetime import datetime, timedelta

FREE_CANCEL_HOURS = 48          # BRD §6: cancelación sin costo con >= 48 h
PRE_RESERVATION_HOURS = 24      # BRD §6: pre-reserva expira a las 24 h sin garantía
CREDIT_LIMIT = 3000.0           # BRD §6: tope de consumos por habitación
AUTHORIZERS = {"JEFE_RESERVACIONES", "ADMINISTRACION"}


class CreditLimitExceeded(Exception):
    pass


@dataclass
class Reservation:
    id: int
    night_rate: float
    arrival: datetime
    created_at: datetime
    status: str = "PRE_RESERVA"   # PRE_RESERVA, CONFIRMADA, CANCELADA, EXPIRADA

    def expire_if_needed(self, now):
        """Regla 3: la pre-reserva sin garantía se libera a las 24 h."""
        if self.status == "PRE_RESERVA" and now - self.created_at >= timedelta(hours=PRE_RESERVATION_HOURS):
            self.status = "EXPIRADA"
        return self.status

    def confirm_with_guarantee(self, now):
        if self.expire_if_needed(now) != "PRE_RESERVA":
            raise ValueError("only a valid pre-reservation can be confirmed")
        self.status = "CONFIRMADA"

    def cancel(self, now, authorized_by=None):
        """Regla 1: devuelve el cargo (0 o 1 noche)."""
        if self.status not in ("PRE_RESERVA", "CONFIRMADA"):
            raise ValueError("reservation cannot be cancelled")
        if authorized_by is not None and authorized_by not in AUTHORIZERS:
            raise PermissionError("only Jefe de Reservaciones or Administración can authorize")
        charge = 0.0
        if self.arrival - now < timedelta(hours=FREE_CANCEL_HOURS) and authorized_by is None:
            charge = self.night_rate
        self.status = "CANCELADA"
        return charge


@dataclass
class RoomAccount:
    """Regla 2: consumos de una habitación con tope de crédito."""
    balance: float = 0.0
    charges: list = field(default_factory=list)

    def add_charge(self, amount, employee, admin_authorized=False):
        if amount <= 0:
            raise ValueError("amount must be positive")
        if self.balance + amount > CREDIT_LIMIT and not admin_authorized:
            raise CreditLimitExceeded("credit limit exceeded")
        self.balance += amount
        self.charges.append((employee, amount))

    def partial_payment(self, amount):
        if amount <= 0 or amount > self.balance:
            raise ValueError("invalid payment")
        self.balance -= amount
