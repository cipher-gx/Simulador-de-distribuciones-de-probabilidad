import math
import re
import numpy as np

class Hipergeometrica:
    def __init__(self, n, k, N):
        self.n = n
        self.k = k
        self.N = N

    def esperanza(self):
        return self.n * (self.k / self.N)
    
    def varianza(self):
        return self.n * (self.k / self.N) * (1 - (self.k / self.N)) * ((self.N - self.n) / (self.N - 1))
    
    def desviacion_estandar(self):
        return math.sqrt(self.varianza())
    
    def probabilidad_X(self, x):
        if x < 0 or x > self.n:
            return 0
        else:
            return (math.comb(self.k, x) * math.comb(self.N - self.k, self.n - x)) / math.comb(self.N, self.n)
        
    def probabilidad_x1_a_x2(self, x1, x2):
        prob = 0
        for i in range(x1, x2+1):
            prob += self.probabilidad_X(i)
        return prob
    
    def simular_x1_a_x2(self, x1, x2, iteraciones):
        simulaciones = np.random.hypergeometric(self.k, self.N - self.k, self.n, size=iteraciones)
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
        
        for match in automata.finditer(cadenaEntrada):
            tipo_regla = match.lastgroup
            texto_encontrado = match.group()
            x1, x2 = None, None
            
            if tipo_regla == "RANGO":
                numeros = [int(n) for n in re.findall(r"\d+", texto_encontrado)]
                x1, x2 = numeros[0], numeros[1]
            
            elif tipo_regla == "RANGO_INTERIOR":
                numeros = [int(n) for n in re.findall(r"\d+", texto_encontrado)]
                x1, x2 = numeros[0] + 1, numeros[1] - 1

            elif tipo_regla == "MAYOR_IGUAL":
                x = int(re.findall(r"\d+", texto_encontrado)[0])
                x1, x2 = x, self.n
                
            elif tipo_regla == "MENOR_IGUAL":
                x = int(re.findall(r"\d+", texto_encontrado)[0])
                x1, x2 = 0, x
                
            elif tipo_regla == "MAYOR":
                x = int(re.findall(r"\d+", texto_encontrado)[0])
                x1, x2 = x + 1, self.n
                
            elif tipo_regla == "MENOR":
                x = int(re.findall(r"\d+", texto_encontrado)[0])
                x1, x2 = 0, x - 1

            elif tipo_regla == "IGUAL":
                x = int(re.findall(r"\d+", texto_encontrado)[0])
                x1, x2 = x, x
                
            elif tipo_regla == "PALABRA":
                continue

        if x1 is not None and x2 is not None:
            teorica = self.probabilidad_x1_a_x2(x1, x2)
            simulada, arreglo_datos = self.simular_x1_a_x2(x1, x2, iteraciones)
            return teorica, simulada, arreglo_datos

        raise ValueError("No se detecto ninguna expresion matematica valida")
    