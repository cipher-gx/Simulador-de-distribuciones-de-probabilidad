import math
import re

class Binomial:
    def __init__(self, n, p):
        self.n = n
        self.p = p
    
    def esperanza(self):
        return self.n * self.p

    def varianza(self):
        return self.n * self.p * (1 - self.p)
    
    def desviacion_estandar(self):
        return math.sqrt(self.varianza())
    
    def probabilidad_X(self, x):
        return (math.comb(self.n, x)) * (self.p ** x) * ((1 - self.p) ** (self.n - x))
    
    def probabilidad_x1_a_x2(self, x1, x2):
        prob = 0
        for i in range(x1, x2+1):
            prob += self.probabilidad_X(i)
        return prob
        
    def evaluar_expresion(self, cadenaEntrada):
        reglas = [
            r"(?P<RANGO>\d+\s*<=\s*X\s*<=\s*\d+)",
            r"(?P<MAYOR_IGUAL>X\s*>=\s*\d+)",
            r"(?P<MENOR_IGUAL>X\s*<=\s*\d+)",
            r"(?P<MAYOR>X\s*>\s*\d+)",
            r"(?P<MENOR>X\s*<\s*\d+)",
            r"(?P<PALABRA>[a-zA-Z]+)"
        ]
        
        patron = "|".join(reglas)
        automata = re.compile(patron, re.IGNORECASE)
        
        for match in automata.finditer(cadenaEntrada):
            tipo_regla = match.lastgroup
            texto_encontrado = match.group()
            
            if tipo_regla == "RANGO":
                numeros = [int(n) for n in re.findall(r"\d+", texto_encontrado)]
                return self.probabilidad_x1_a_x2(numeros[0], numeros[1])
                
            elif tipo_regla == "MAYOR_IGUAL":
                x = int(re.findall(r"\d+", texto_encontrado)[0])
                return self.probabilidad_x1_a_x2(x, self.n)
                
            elif tipo_regla == "MENOR_IGUAL":
                x = int(re.findall(r"\d+", texto_encontrado)[0])
                return self.probabilidad_x1_a_x2(0, x)
                
            elif tipo_regla == "MAYOR":
                x = int(re.findall(r"\d+", texto_encontrado)[0])
                return self.probabilidad_x1_a_x2(x + 1, self.n) 
                
            elif tipo_regla == "MENOR":
                x = int(re.findall(r"\d+", texto_encontrado)[0])
                return self.probabilidad_x1_a_x2(0, x - 1) 
                
            elif tipo_regla == "PALABRA":
                continue

        raise ValueError("No se detecto ninguna expresion matematica valida")
