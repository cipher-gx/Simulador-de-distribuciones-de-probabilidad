import re
import numpy as np
from scipy.integrate import quad

class Exponencial:
    def __init__(self, alfa):
        self.alfa = alfa

    def distribucion_exponencial(self, x):
        return self.alfa * np.exp(-self.alfa * x)

    def Esperanza(self):
        return 1 / self.alfa

    def Varianza(self):
        return 1 / (self.alfa ** 2)

    def Desviacion_Estandar(self):
        return 1 / self.alfa

    def probabilidad_X1_a_X2(self, x1, x2):
        resultado, error = quad(self.distribucion_exponencial, x1, x2)
        return resultado
    
    def simular_probabilidad(self, x1, x2, iteraciones):
        datos_simulados = np.random.exponential(1/self.alfa, iteraciones)
        casos_favorables = np.sum((datos_simulados > x1) & (datos_simulados < x2))
        probabilidad_simulada = casos_favorables / iteraciones
        
        return probabilidad_simulada, datos_simulados

    def evaluar_expresion(self, cadenaEntrada, iteraciones):
        reglas = [
            r"(?P<RANGO_INTERIOR>\d+(?:\.\d+)?\s*(?:<|<=)\s*X\s*(?:<|<=)\s*\d+(?:\.\d+)?)",
            r"(?P<MAYOR>X\s*(?:>|>=)\s*\d+(?:\.\d+)?)",
            r"(?P<MENOR>X\s*(?:<|<=)\s*\d+(?:\.\d+)?)",
            r"(?P<IGUAL>X\s*=\s*\d+(?:\.\d+)?)", 
            r"(?P<PALABRA>[a-zA-Z]+)"
        ]

        patron = "|".join(reglas)
        automata = re.compile(patron, re.IGNORECASE)

        for match in automata.finditer(cadenaEntrada):
            tipo_regla = match.lastgroup
            texto_encontrado = match.group()
            x1, x2 = None, None 
        
            if tipo_regla == "RANGO_INTERIOR":
                numeros = [float(n) for n in re.findall(r"\d+(?:\.\d+)?", texto_encontrado)]
                x1, x2 = numeros[0], numeros[1]
            
            elif tipo_regla == "MAYOR":
                x = float(re.findall(r"\d+(?:\.\d+)?", texto_encontrado)[0])
                x1, x2 = x, np.inf
            
            elif tipo_regla == "MENOR":
                x = float(re.findall(r"\d+(?:\.\d+)?", texto_encontrado)[0])
                x1, x2 = 0, x
                
            elif tipo_regla == "IGUAL":
                return 0.0, 0.0, np.array([]) 
            
            elif tipo_regla == "PALABRA":
                continue

            if x1 is not None and x2 is not None:
                teorica = self.probabilidad_X1_a_X2(x1, x2)
                simulada, arreglo_datos = self.simular_probabilidad(x1, x2, iteraciones)
                
                return teorica, simulada, arreglo_datos

        raise ValueError("No se detectó ninguna expresión matemática válida.")