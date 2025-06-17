# ... tus imports
import json
import os
import ttkbootstrap as ttkb
from ttkbootstrap.constants import *
from tkinter import messagebox, simpledialog

# ---------------------- Clases -----------------------

class Cuenta:
    def __init__(self, cedula, nombre, saldo):
        self.cedula = cedula
        self.nombre = nombre
        self.saldo = saldo

    def to_dict(self):
        return {
            "cedula": self.cedula,
            "nombre": self.nombre,
            "saldo": self.saldo
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
                    self.cuentas[cedula] = Cuenta(cedula, info["nombre"], info["saldo"])

    def guardar_cuentas(self):
        with open(self.archivo, "w") as f:
            data = {ced: cuenta.to_dict() for ced, cuenta in self.cuentas.items()}
            json.dump(data, f, indent=4)

    def crear_cuenta(self, cedula, nombre, saldo):
        if cedula not in self.cuentas:
            self.cuentas[cedula] = Cuenta(cedula, nombre, saldo)
            self.guardar_cuentas()
            return True
        return False

    def iniciar_sesion(self, cedula):
        return self.cuentas.get(cedula)

    def depositar(self, cuenta, monto):
        if monto > 0:
            cuenta.saldo += monto
            self.guardar_cuentas()
            return True
        return False

    def retirar(self, cuenta, monto):
        if 0 < monto <= cuenta.saldo:
            cuenta.saldo -= monto
            self.guardar_cuentas()
            return True
        return False

    def obtener_saldo(self, cuenta):
        return cuenta.saldo

    def eliminar_cuenta(self, cedula):
        if cedula in self.cuentas:
            del self.cuentas[cedula]
            self.guardar_cuentas()
            return True
        return False

# ---------------------- Ventana Banco -----------------------

class VentanaBanco(ttkb.Toplevel):
    def __init__(self, master, controlador, cuenta):
        super().__init__(master)
        self.title("Cuenta Bancaria")
        self.geometry("600x420")
        self.controlador = controlador
        self.cuenta = cuenta

        ttkb.Label(self, text=f"Bienvenido, {cuenta.nombre}", font=("Arial", 16)).pack(pady=10)
        ttkb.Label(self, text=f"Cédula: {cuenta.cedula}", font=("Arial", 12)).pack(pady=5)

        self.label_saldo = ttkb.Label(self, text=f"Saldo: ${cuenta.saldo:.2f}", font=("Arial", 14))
        self.label_saldo.pack(pady=10)

        self.entry_monto = ttkb.Entry(self, font=("Arial", 12))
        self.entry_monto.pack(pady=10)

        ttkb.Button(self, text="Depositar", bootstyle="success", command=self.depositar).pack(pady=5)
        ttkb.Button(self, text="Retirar", bootstyle="warning", command=self.retirar).pack(pady=5)
        ttkb.Button(self, text="Eliminar cuenta", bootstyle="danger-outline", command=self.eliminar_cuenta).pack(pady=5)
        ttkb.Button(self, text="Salir", bootstyle="secondary", command=self.destroy).pack(pady=10)

    def actualizar_saldo(self):
        self.label_saldo.config(text=f"Saldo: ${self.cuenta.saldo:.2f}")

    def obtener_monto(self):
        try:
            return float(self.entry_monto.get())
        except ValueError:
            messagebox.showerror("Error", "Monto inválido.")
            return None

    def depositar(self):
        monto = self.obtener_monto()
        if monto and self.controlador.depositar(self.cuenta, monto):
            self.actualizar_saldo()

    def retirar(self):
        monto = self.obtener_monto()
        if monto and self.controlador.retirar(self.cuenta, monto):
            self.actualizar_saldo()
        else:
            messagebox.showerror("Error", "Fondos insuficientes o monto inválido.")

    def eliminar_cuenta(self):
        confirm = messagebox.askyesno("Eliminar cuenta", "¿Estás seguro de eliminar tu cuenta? Esta acción no se puede deshacer.")
        if confirm:
            if self.controlador.eliminar_cuenta(self.cuenta.cedula):
                messagebox.showinfo("Cuenta eliminada", "Tu cuenta ha sido eliminada correctamente.")
                self.destroy()
                self.master.deiconify()
            else:
                messagebox.showerror("Error", "No se pudo eliminar la cuenta.")

# ---------------------- Ventana Inicio -----------------------

class VentanaInicio(ttkb.Window):
    def __init__(self):
        super().__init__(title="Inicio de Sesión", themename="superhero")
        self.geometry("400x300")
        self.controlador = ControladorBanco()

        ttkb.Label(self, text="Ingrese su número de cédula:", font=("Arial", 12)).pack(pady=10)
        self.entry_cedula = ttkb.Entry(self)
        self.entry_cedula.pack(pady=5)

        ttkb.Button(self, text="Iniciar Sesión", bootstyle="primary", command=self.iniciar_sesion).pack(pady=10)

    def iniciar_sesion(self):
        cedula = self.entry_cedula.get()
        if not cedula:
            messagebox.showerror("Error", "Ingrese un número de cédula.")
            return

        cuenta = self.controlador.iniciar_sesion(cedula)
        if cuenta:
            self.abrir_ventana_banco(cuenta)
        else:
            crear = messagebox.askyesno("No encontrado", "¿Desea crear una cuenta nueva?")
            if crear:
                self.registrar_cuenta(cedula)

    def registrar_cuenta(self, cedula):
        nombre = simpledialog.askstring("Nombre", "Ingrese su nombre:")
        saldo = simpledialog.askfloat("Saldo inicial", "Ingrese el saldo inicial:")
        if nombre and saldo is not None:
            if self.controlador.crear_cuenta(cedula, nombre, saldo):
                cuenta = self.controlador.iniciar_sesion(cedula)
                self.abrir_ventana_banco(cuenta)
            else:
                messagebox.showerror("Error", "La cuenta ya existe.")
        else:
            messagebox.showwarning("Cancelado", "Registro incompleto.")

    def abrir_ventana_banco(self, cuenta):
        self.withdraw()
        ventana = VentanaBanco(self, self.controlador, cuenta)
        ventana.protocol("WM_DELETE_WINDOW", self.on_close_main)

    def on_close_main(self):
        self.deiconify()
        for child in self.winfo_children():
            if isinstance(child, VentanaBanco):
                child.destroy()

# ---------------------- MAIN -----------------------

if __name__ == "__main__":
    app = VentanaInicio()
    app.mainloop()
