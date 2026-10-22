from enum import Enum


class TipoMovimientoEnum(int, Enum):
  PAGO_O_ABONO = 1
  CREACION_FACTURA = 2
  # Aquí podrás agregar los futuros tipos para puntos:
  # ACUMULACION_PUNTOS = 3
  # CANJE_PUNTOS = 4