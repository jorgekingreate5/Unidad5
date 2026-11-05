from src.domain import Reservation


class GuaranteeRejected(Exception):
    pass


class ReservationService:
    """Coordina; las reglas viven en el dominio. El validador de tarjeta es simulado."""

    def __init__(self, card_validator):
        self.card_validator = card_validator

    def guarantee(self, reservation: Reservation, card_token, now):
        # Se valida la tarjeta ANTES de confirmar (evita el riesgo detectado en E5).
        if not self.card_validator.is_valid(card_token):
            raise GuaranteeRejected("card rejected")
        reservation.confirm_with_guarantee(now)
        return reservation.status
