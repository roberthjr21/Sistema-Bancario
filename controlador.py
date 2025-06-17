import json
import os
from datetime import datetime

class Cuenta:
    def __init__(self, cedula, nombre, saldo, movimientos=None):
        self.cedula = cedula
        self.nombre = nombre
        self.saldo = saldo
        self.movimientos = movimientos if movimientos else []

    def to_dict(self):
        return {
            "cedula": self.cedula,
            "nombre": self.nombre,
            "saldo": self.saldo,
            "movimientos": self.movimientos
        }

class ControladorBanco:
    def __init__(self, archivo="cuentas.json"):
        self.archivo = archivo
        self.cuentas = {}
        self.cargar_cuentas()

    def cargar_cuentas(self):
        if os.path.exists(self.archivo):
            with open(self.archivo, "r") as f:
                data = json.load(f)
                for cedula, info in data.items():
                    self.cuentas[cedula] = Cuenta(
                        cedula,
                        info["nombre"],
                        info["saldo"],
                        info.get("movimientos", [])
                    )

    def guardar_cuentas(self):
        with open(self.archivo, "w") as f:
            data = {ced: cuenta.to_dict() for ced, cuenta in self.cuentas.items()}
            json.dump(data, f, indent=4)

    def crear_cuenta(self, cedula, nombre, saldo):
        if cedula not in self.cuentas:
            cuenta = Cuenta(cedula, nombre, saldo)
            cuenta.movimientos.append(self._registro("Depósito inicial", saldo))
            self.cuentas[cedula] = cuenta
            self.guardar_cuentas()
            return True
        return False

    def iniciar_sesion(self, cedula):
        return self.cuentas.get(cedula)

    def depositar(self, cuenta, monto):
        if monto > 0:
            cuenta.saldo += monto
            cuenta.movimientos.append(self._registro("Depósito", monto))
            self.guardar_cuentas()
            return True
        return False

    def retirar(self, cuenta, monto):
        if 0 < monto <= cuenta.saldo:
            cuenta.saldo -= monto
            cuenta.movimientos.append(self._registro("Retiro", monto))
            self.guardar_cuentas()
            return True
        return False

    def obtener_saldo(self, cuenta):
        return cuenta.saldo

    def obtener_movimientos(self, cuenta):
        return cuenta.movimientos

    def _registro(self, tipo, monto):
        return {
            "tipo": tipo,
            "monto": monto,
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M")
        }
