import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import ttk
from controlador import ControladorBanco

class VistaBanco:
    def __init__(self, root, controlador):
        self.controlador = controlador
        self.root = root
        self.root.geometry("600x400")
        self.root.title("Sistema Bancario")
        
        # Estilo
        style = ttk.Style()
        style.configure("TLabel", font=("Arial", 14))
        style.configure("TButton", font=("Arial", 12), padding=10)
        style.configure("TEntry", font=("Arial", 12), padding=5)
        
        self.frame = ttk.Frame(root, padding="20")
        self.frame.pack(fill=tk.BOTH, expand=True)
        
        self.label_usuario = ttk.Label(self.frame, text=f"Usuario: {controlador.obtener_usuario()}")
        self.label_usuario.pack(pady=10)
        
        self.label_saldo = ttk.Label(self.frame, text=f"Saldo: ${controlador.obtener_saldo():.2f}")
        self.label_saldo.pack(pady=10)
        
        self.entry_cantidad = ttk.Entry(self.frame)
        self.entry_cantidad.pack(pady=10)
        
        self.btn_depositar = ttk.Button(self.frame, text="Depositar", command=self.depositar)
        self.btn_depositar.pack(pady=5)
        
        self.btn_retirar = ttk.Button(self.frame, text="Retirar", command=self.retirar)
        self.btn_retirar.pack(pady=5)
        
        self.btn_salir = ttk.Button(self.frame, text="Salir", command=self.root.quit)
        self.btn_salir.pack(pady=5)
        
    def depositar(self):
        cantidad = self.obtener_cantidad()
        if cantidad is not None:
            if self.controlador.depositar(cantidad):
                self.actualizar_saldo()
            else:
                messagebox.showerror("Error", "Ingrese un monto válido para depositar.")
    
    def retirar(self):
        cantidad = self.obtener_cantidad()
        if cantidad is not None:
            if self.controlador.retirar(cantidad):
                self.actualizar_saldo()
            else:
                messagebox.showerror("Error", "Fondos insuficientes o cantidad inválida.")
    
    def obtener_cantidad(self):
        try:
            return float(self.entry_cantidad.get())
        except ValueError:
            messagebox.showerror("Error", "Ingrese una cantidad válida.")
            return None
    
    def actualizar_saldo(self):
        self.label_saldo.config(text=f"Saldo: ${self.controlador.obtener_saldo():.2f}")

if __name__ == "__main__":
    root = tk.Tk()
    usuario = simpledialog.askstring("Usuario", "Ingrese el nombre del usuario:")
    saldo_inicial = simpledialog.askfloat("Saldo Inicial", "Ingrese el saldo inicial del usuario:")
    controlador = ControladorBanco(usuario, saldo_inicial)
    vista = VistaBanco(root, controlador)
    root.mainloop()