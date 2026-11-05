"""Pruebas parametrizadas con los CSV del profesor (LEEME punto 7)."""
import csv
from pathlib import Path

import pytest

from src.domain import CustomerHasDebt, Order

DATOS = Path(__file__).resolve().parent.parent / "datos"


def _leer(nombre):
    with open(DATOS / nombre, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


PEDIDOS = {int(r["pedido_id"]): r for r in _leer("pedidos_prueba.csv")}
CASOS = [c for c in _leer("casos_de_prueba.csv") if c["accion"] == "confirmar"]


@pytest.mark.parametrize("caso", CASOS, ids=[c["caso_id"] for c in CASOS])
def test_confirmar_segun_csv(caso):
    p = PEDIDOS[int(caso["pedido_id"])]
    order = Order(float(p["total"]), vip=p["es_vip"] == "1", status=p["estado_inicial"])
    deuda = float(p["deuda_cliente"])
    esperado = caso["resultado_esperado"]

    if esperado == "CustomerHasDebt":
        with pytest.raises(CustomerHasDebt):
            order.confirm(customer_debt=deuda)
    elif esperado == "ValueError":
        with pytest.raises(ValueError):
            order.confirm(customer_debt=deuda)
    elif caso["caso_id"] == "CP08":
        # Caso TDD: el CSV describe el comportamiento ANTERIOR; tras el ciclo RED-GREEN
        # la regla correcta es rechazar la segunda confirmación.
        with pytest.raises(ValueError, match="already confirmed"):
            order.confirm(customer_debt=deuda)
    else:
        cobro = float(esperado.split("cobro")[1])
        assert order.confirm(customer_debt=deuda) == pytest.approx(cobro)
        assert order.status == "CONFIRMED"
