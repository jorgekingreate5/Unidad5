# Adaptación U5 – Pruebas de reglas del PIA Hotel Costa Azul

Equipo: Jorge Luis Molina García (2147723), Jonathan Alexander Reyes Garcia (2146387), Leonardo Davila Gongora (2145945).
Reglas tomadas del BRD aprobado del Hotel Costa Azul (§6 Restricciones): no se inventaron reglas nuevas.

| Regla | Dominio |
|---|---|
| 1. Cancelación sin costo con ≥ 48 h; después, cargo de 1 noche; excepción solo por Jefe de Reservaciones o Administración | `Reservation.cancel` |
| 2. Tope de consumos de $3,000 MXN por habitación; superarlo requiere pago parcial o autorización de Administración | `RoomAccount.add_charge` |
| 3. La pre-reserva expira a las 24 h si no hay garantía | `Reservation.expire_if_needed` |

Instalación y comandos: igual que el laboratorio (`pip install -r requirements.txt`, `python -m pytest -v --cov=src --cov-report=html --cov-fail-under=80`, `python -m ruff check src tests`).

Arquitectura: `domain.py` (reglas puras) ← `application.py` (`ReservationService`, valida la tarjeta con un validador inyectable y simulado con Mock) ← `repository.py` (SQLAlchemy, SQLite en memoria).
Matriz: `datos/matriz_pruebas_pia.csv` (22 casos).
