from modelo import CuentaBancaria

class ControladorBanco:
    def __init__(self, usuario, saldo_inicial):
        self.modelo = CuentaBancaria(usuario, saldo_inicial)
    
    def depositar(self, cantidad):
        return self.modelo.depositar(cantidad)
    
    def retirar(self, cantidad):
        return self.modelo.retirar(cantidad)
    
    def obtener_saldo(self):
        return self.modelo.consultar_saldo()
    
    def obtener_usuario(self):
        return self.modelo.usuario