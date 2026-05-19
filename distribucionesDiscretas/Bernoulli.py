import math
import re
import numpy as np

class Bernoulli:
    def __init__(self, p):
        self.p = p
    
    def esperanza(self):
        return self.p

    def varianza(self):
        return self.p * (1 - self.p)
        
    def desviacion_estandar(self):
        return math.sqrt(self.varianza())
    
    def probabilidad_X(self, x):
        if x < 0 or x > 1:
            return 0
        else:
            return (self.p ** x) * ((1 - self.p) ** (1 - x))

    def probabilidad_x1_a_x2(self, x1, x2):
        probabilidad = 0
        for x in range(x1, x2 + 1):
            probabilidad += self.probabilidad_X(x)
        return probabilidad

    def simular_x1_a_x2(self, x1, x2, tamaño_muestra):
        juegos = np.random.binomial(n=1, p=self.p, size=tamaño_muestra)
        filtro = (juegos >= x1) & (juegos <= x2)
        return np.sum(filtro) / tamaño_muestra
        
    def evaluar_expresion(self, cadenaEntrada):
        reglas = [
            r"(?P<RANGO>\d+\s*<=\s*X\s*<=\s*\d+)",
            r"(?P<RANGO_INTERIOR>\d+\s*<\s*X\s*<\s*\d+)",
            r"(?P<MAYOR_IGUAL>X\s*>=\s*\d+)",
            r"(?P<MENOR_IGUAL>X\s*<=\s*\d+)",
            r"(?P<MAYOR>X\s*>\s*\d+)",
            r"(?P<MENOR>X\s*<\s*\d+)",
            r"(?P<PALABRA>[a-zA-Z]+)"
        ]
        
        patron = "|".join(reglas)
        automata = re.compile(patron, re.IGNORECASE)
        
        x1, x2 = None, None
        n_fijo = 1
        
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
                x1, x2 = x, n_fijo
                
            elif tipo_regla == "MENOR_IGUAL":
                x = int(re.findall(r"\d+", texto_encontrado)[0])
                x1, x2 = 0, x
                
            elif tipo_regla == "MAYOR":
                x = int(re.findall(r"\d+", texto_encontrado)[0])
                x1, x2 = x + 1, n_fijo 
                
            elif tipo_regla == "MENOR":
                x = int(re.findall(r"\d+", texto_encontrado)[0])
                x1, x2 = 0, x - 1 
                
            elif tipo_regla == "PALABRA":
                continue

        if x1 is not None and x2 is not None:
            teorica = self.probabilidad_x1_a_x2(x1, x2)
            simulada = self.simular_x1_a_x2(x1, x2, 10000)
            return teorica, simulada

        raise ValueError("No se detecto ninguna expresion matematica valida")
    

        