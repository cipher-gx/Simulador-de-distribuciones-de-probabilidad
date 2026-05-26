import re
import numpy as np
from scipy.integrate import quad

class Normal:
    def __init__(self, media, desviacion):
        self.media = media
        self.desviacion = desviacion

    def distribucion_normal(self, x):
        return (np.exp((-1/2)*((x-self.media)/self.desviacion)**2)/(np.sqrt(2*np.pi)*self.desviacion))

    def Esperanza(self):
        return self.media

    def Varianza(self):
        return self.desviacion ** 2

    def Desviacion_Estandar(self):
        return self.desviacion

    def probabilidad_X1_a_X2(self, x1, x2):
        resultado, error = quad(self.distribucion_normal, x1, x2)
        return resultado
    
    def simular_probabilidad(self, x1, x2, iteraciones):
        datos_simulados = np.random.normal(self.media, self.desviacion, iteraciones)
        casos_favorables = np.sum((datos_simulados > x1) & (datos_simulados < x2))
        probabilidad_simulada = casos_favorables / iteraciones
        
        return probabilidad_simulada, datos_simulados

    def evaluar_expresion(self, cadenaEntrada, iteraciones):
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
                x1, x2 = x, np.inf
            
            elif tipo_regla == "MENOR":
                x = float(re.findall(r"-?\d+(?:\.\d+)?", texto_encontrado)[0])
                x1, x2 = -np.inf, x
                
            elif tipo_regla == "IGUAL":
                return 0.0, 0.0, np.array([]) 
            
            elif tipo_regla == "PALABRA":
                continue

            if x1 is not None and x2 is not None:
                teorica = self.probabilidad_X1_a_X2(x1, x2)
                simulada, arreglo_datos = self.simular_probabilidad(x1, x2, iteraciones)
                return teorica, simulada, arreglo_datos

        raise ValueError("No se detectó ninguna expresión matemática válida.")


if __name__ == "__main__":
    mi_simulador = Normal(media=8, desviacion=1.5)

    print("--- PARÁMETROS BASE ---")
    print(f"Esperanza (Media): {mi_simulador.Esperanza()}")
    print(f"Varianza: {mi_simulador.Varianza()}")
    print("-" * 40)

    pruebas = [
        "7 < X < 9",         
        "X < 8",             
        "X > 9.5",           
        "X = 8.5",           
    ]

    print("\n--- CALCULANDO Y SIMULANDO PROBABILIDADES ---")
    for expresion in pruebas:
        try:
            teorica, simulada, datos = mi_simulador.evaluar_expresion(expresion, iteraciones=10000)
            
            print(f"Expresión: '{expresion}'")
            print(f"  -> Prob. Teórica (Integral): {teorica:.5f}")
            print(f"  -> Prob. Simulada (Empírica): {simulada:.5f}")
            print(f"  -> Datos generados para la gráfica: {len(datos)} números")
            print("-" * 40)
            
        except Exception as e:
            print(f"Expresión: '{expresion}' \t-> Error: {e}")