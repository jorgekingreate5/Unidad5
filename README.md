# Unidad 5 CLN – Integración, Pruebas y Calidad (Laboratorio guiado)

Equipo: Jorge Luis Molina García (2147723), Jonathan Alexander Reyes Garcia (2146387), Leonardo Davila Gongora (2145945) – ITS, FIME UANL.
Profesor: Miguel Ángel Gómez Marroquín. Proyecto base: ejemplo de pedidos entregado por el profesor.

## Instalación
Windows PowerShell:
```
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```
macOS / Linux:
```
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Comandos
```
python -m pytest -v                                   # todas las pruebas (E1)
python -m pytest tests/test_order.py -v               # dominio (E2, E3)
python -m pytest tests/test_repository.py -v          # persistencia (E4)
python -m pytest tests/test_service.py -v             # mocks (E5)
python -m pytest tests/test_security.py -v            # autorización (E6)
python -m ruff check src tests
python -m pytest -v --cov=src --cov-report=term-missing --cov-report=html --cov-fail-under=80   # E7
```
El reporte HTML queda en `htmlcov/index.html`.

### Reproducir la fase RED (E3)
1. Copiar `../tdd/domain_1_original_RED.py` sobre `src/domain.py` (versión original, sin la regla).
2. `python -m pytest tests/test_order.py::test_cannot_confirm_twice -v` → FAIL (esperado).
3. Copiar `../tdd/domain_2_GREEN.py` → PASS. Después `../tdd/domain_3_REFACTOR.py` (versión final del proyecto) y ejecutar toda la suite.

## Arquitectura
| Archivo | Responsabilidad |
|---|---|
| `src/domain.py` | Reglas de pedidos: descuento VIP 15 %, total > 0, deuda, no confirmar dos veces |
| `src/application.py` | `OrderService.checkout`: confirma el pedido y cobra con una pasarela (inyectada) |
| `src/repository.py` | Persistencia SQLAlchemy 2.x (SQLite en memoria en las pruebas) |
| `src/security.py` | `can_cancel`: SHIPPED nunca; administrador sí; propietario solo antes de 24 h |
| `tests/` | Unitarias (dominio, seguridad), integración (repositorio), mocks (servicio) y parametrizadas con CSV |
| `datos/` | CSV y SQLite didácticos del profesor + `matriz_pruebas.csv` del equipo |
| `.github/workflows/ci.yml` | CI Business Logic: Ruff, pytest con cobertura ≥ 80 %, compileall |

Capas: dominio (sin dependencias) ← servicio de aplicación (usa una pasarela inyectable) ← repositorio (SQLAlchemy). Las pruebas del dominio no usan base de datos ni red.

## Notas
- Los datos son ficticios; no hay credenciales ni `.venv` en la entrega.
- Riesgo conocido (E5): `checkout` confirma el pedido antes de saber si el pago fue aceptado.
