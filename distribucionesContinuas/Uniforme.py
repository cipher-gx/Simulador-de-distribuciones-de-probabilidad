import re
import numpy as np
from scipy.integrate import quad

class Uniforme:
    def __init__(self, limiteInferior, limiteSuperior):
        self.limiteInferior = limiteInferior
        self.limiteSuperior = limiteSuperior

    def distribucion_uniforme(self, x):
        if self.limiteInferior <= x <= self.limiteSuperior:
            return 1 / (self.limiteSuperior - self.limiteInferior)
        else:
            return 0

    def Esperanza(self):
        return (self.limiteInferior + self.limiteSuperior) / 2

    def Varianza(self):
        return (self.limiteSuperior - self.limiteInferior) ** 2 / 12

    def Desviacion_Estandar(self):
        return np.sqrt(self.Varianza())

    def probabilidad_X1_a_X2(self, x1, x2):
        resultado, error = quad(self.distribucion_uniforme, x1, x2)
        return resultado

    def simular_probabilidad(self, x1, x2, iteraciones):
        datos_simulados = np.random.uniform(self.limiteInferior, self.limiteSuperior, iteraciones)
        casos_favorables = np.sum((datos_simulados > x1) & (datos_simulados < x2))
        probabilidad_simulada = casos_favorables / iteraciones
        return probabilidad_simulada, datos_simulados

    def evaluar_expresion(self, cadenaEntrada, iteraciones):
        # 1. Regresamos el soporte para números negativos (-?)
        reglas = [
            r"(?P<RANGO_INTERIOR>-?\d+(?:\.\d+)?\s*(?:<|<=)\s*X\s*(?:<|<=)\s*-?\d+(?:\.\d+)?)",
            r"(?P<MAYOR>X\s*(?:>|>=)\s*-?\d+(?:\.\d+)?)",
            r"(?P<MENOR>X\s*(?:<|<=)\s*-?\d+(?:\.\d+)?)",
            r"(?P<IGUAL>X\s*=\s*-?\d+(?:\.\d+)?)",
            r"(?P<PALABRA>[a-zA-Z]+)"
        ]

        patron = "|".join(reglas)
        automata = re.compile(patron, re.IGNORECASE)

        for match in automata.finditer(cadenaEntrada):
            tipo_regla = match.lastgroup
            texto_encontrado = match.group()
            x1, x2 = None, None

            if tipo_regla == "RANGO_INTERIOR":
                numeros = [float(n) for n in re.findall(r"-?\d+(?:\.\d+)?", texto_encontrado)]
                x1, x2 = numeros[0], numeros[1]

            elif tipo_regla == "MAYOR":
                x = float(re.findall(r"-?\d+(?:\.\d+)?", texto_encontrado)[0])
                # 2. El techo ahora es el límite superior de la distribución
                x1, x2 = x, self.limiteSuperior

            elif tipo_regla == "MENOR":
                x = float(re.findall(r"-?\d+(?:\.\d+)?", texto_encontrado)[0])
                # 2. El piso ahora es el límite inferior de la distribución
                x1, x2 = self.limiteInferior, x

            elif tipo_regla == "IGUAL":
                return 0.0, 0.0, np.array([])

            elif tipo_regla == "PALABRA":
                continue

            if x1 is not None and x2 is not None:
                # 3. Blindaje: Recortar si el usuario pide cosas fuera del rectángulo
                if x1 < self.limiteInferior:
                    x1 = self.limiteInferior
                if x2 > self.limiteSuperior:
                    x2 = self.limiteSuperior
                
                # Si los límites se cruzan (ej. piden < 2 pero la caja empieza en 5)
                if x1 >= x2:
                    return 0.0, 0.0, np.array([])

                teorica = self.probabilidad_X1_a_X2(x1, x2)
                simulada, arreglo_datos = self.simular_probabilidad(x1, x2, iteraciones)

                return teorica, simulada, arreglo_datos

        raise ValueError("No se detectó ninguna expresión matemática válida.")


# ==========================================
# BLOQUE DE PRUEBAS
# ==========================================
if __name__ == "__main__":
    # Creamos una distribución Uniforme que va de -5 a 10
    mi_simulador_uni = Uniforme(limiteInferior=-5, limiteSuperior=10)

    print("--- PARÁMETROS BASE (UNIFORME) ---")
    print(f"Límites: [{mi_simulador_uni.limiteInferior}, {mi_simulador_uni.limiteSuperior}]")
    print(f"Esperanza: {mi_simulador_uni.Esperanza()}")
    print("-" * 45)

    pruebas = [
        "-2 < X < 4",        # Rango estándar que incluye negativos
        "X < 0",             # Menor que (el límite inferior automático será -5)
        "X > 15",            # Mayor que el máximo (el blindaje detectará que es 0%)
        "X = 5",             # Valor exacto
    ]

    for expresion in pruebas:
        try:
            teorica, simulada, datos = mi_simulador_uni.evaluar_expresion(expresion, 100000)
            print(f"Expresión: '{expresion}'")
            print(f"  -> Prob. Teórica: {teorica:.5f} | Prob. Simulada: {simulada:.5f}")
            print("-" * 45)
        except Exception as e:
            print(f"Expresión: '{expresion}' \t-> Error: {e}")