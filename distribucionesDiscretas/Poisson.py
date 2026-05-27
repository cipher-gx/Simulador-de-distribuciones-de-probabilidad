import math
import re
import numpy as np

class Poisson:
    def __init__(self, l):
        self.l = l

    def esperanza(self):
        return self.l
    
    def varianza(self):
        return self.l
    
    def desviacion_estandar(self):
        return math.sqrt(self.l)
    
    def probabilidad_X(self, x):
        if self.l is None:
            raise ValueError("El parametro lambda no ha sido definido")
        if x < 0 or not isinstance(x, int):
            raise ValueError("x debe ser un entero no negativo")
        
        return ((self.l ** x) * (math.exp(-self.l))) / math.factorial(x)
    
    def probabilidad_x1_a_x2(self, x1, x2):
        prob = 0
        for i in range(x1, x2+1):
            prob += self.probabilidad_X(i)
        return prob
    
    def simular_x1_a_x2(self, x1, x2, iteraciones):
        simulaciones = np.random.poisson(self.l, size=iteraciones)
        filtro = (simulaciones >= x1) & (simulaciones <= x2)
        probabilidad_simulada = np.sum(filtro) / iteraciones
        return probabilidad_simulada, simulaciones 
    
    def evaluar_expresion(self, cadenaEntrada, iteraciones):
        reglas = [
            r"(?P<RANGO>\d+\s*<=\s*X\s*<=\s*\d+)",
            r"(?P<RANGO_INTERIOR>\d+\s*<\s*X\s*<\s*\d+)",
            r"(?P<MAYOR_IGUAL>X\s*>=\s*\d+)",
            r"(?P<MENOR_IGUAL>X\s*<=\s*\d+)",
            r"(?P<MAYOR>X\s*>\s*\d+)",
            r"(?P<MENOR>X\s*<\s*\d+)",
            r"(?P<IGUAL>X\s*=\s*\d+)",        
            r"(?P<PALABRA>[a-zA-Z]+)"
        ]
        
        patron = "|".join(reglas)
        automata = re.compile(patron, re.IGNORECASE)
        
        x1, x2 = None, None
        for match in automata.finditer(cadenaEntrada):
            tipo_regla = match.lastgroup
            texto_encontrado = match.group()
            
            
            if tipo_regla == "RANGO":
                numeros = [int(n) for n in re.findall(r"\d+", texto_encontrado)]
                x1, x2 = numeros[0], numeros[1]
            
            elif tipo_regla == "RANGO_INTERIOR":
                numeros = [int(n) for n in re.findall(r"\d+", texto_encontrado)]
                x1, x2 = numeros[0] + 1, numeros[1] - 1
                
            elif tipo_regla == "MAYOR_IGUAL":
                x = int(re.findall(r"\d+", texto_encontrado)[0])
                x1, x2 = x, float('inf')
                
            elif tipo_regla == "MENOR_IGUAL":
                x = int(re.findall(r"\d+", texto_encontrado)[0])
                x1, x2 = 0, x
                
            elif tipo_regla == "MAYOR":
                x = int(re.findall(r"\d+", texto_encontrado)[0])
                x1, x2 = x + 1, float('inf')
                
            elif tipo_regla == "MENOR":
                x = int(re.findall(r"\d+", texto_encontrado)[0])
                x1, x2 = 0, x - 1 

            elif tipo_regla == "IGUAL":
                x = int(re.findall(r"\d+", texto_encontrado)[0])
                x1, x2 = x, x
                
            elif tipo_regla == "PALABRA":
                continue

        
        if x1 is not None and x2 is not None:
            if x2 == float('inf'):
                teorica = 1 - self.probabilidad_x1_a_x2(0, x1-1)
                simulada_inversa, arreglo_datos = self.simular_x1_a_x2(0, x1-1, iteraciones)
                simulada = 1 - simulada_inversa
            else:
                teorica = self.probabilidad_x1_a_x2(x1, x2)
                simulada, arreglo_datos = self.simular_x1_a_x2(x1, x2, iteraciones)
                
            return teorica, simulada, arreglo_datos

        raise ValueError("No se detecto ninguna expresion matematica valida")
