import sys
import numpy as np
import scipy.stats as stats
from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import Qt  
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from distribucionesContinuas.Normal import Normal
from distribucionesContinuas.Exponencial import Exponencial
from distribucionesContinuas.Uniforme import Uniforme

from distribucionesDiscretas.Bernoulli import Bernoulli
from distribucionesDiscretas.Binomial import Binomial
from distribucionesDiscretas.Geometrica import Geometrica
from distribucionesDiscretas.Hipergeometrica import Hipergeometrica
from distribucionesDiscretas.Poisson import Poisson


class Lienzo(FigureCanvas):
    def __init__(self, parent=None):
        self.fig = Figure(figsize=(6, 4.5), dpi=100)
        self.ax = self.fig.add_subplot(111)
        super().__init__(self.fig)
        
        self.fig.patch.set_facecolor('#0d1117') 
        self.ax.set_facecolor('#161b22')         
        self.ax.tick_params(colors='#8b949e', labelsize=10)      
        self.ax.xaxis.label.set_color('#8b949e')
        self.ax.yaxis.label.set_color('#8b949e')
        self.ax.title.set_color('#c9d1d9')
        self.ax.spines['bottom'].set_color('#30363d')
        self.ax.spines['top'].set_color('none')
        self.ax.spines['right'].set_color('none')
        self.ax.spines['left'].set_color('#30363d')

    def actualizar_grafica(self, datos, es_discreta, indice=None, params=None, titulo="Distribución"):
        self.ax.clear()
        if datos is None or len(datos) == 0:
            self.draw()
            return

        if es_discreta:
            valores, frecuencias = np.unique(datos, return_counts=True)
            probabilidades = frecuencias / len(datos)
            self.ax.bar(valores, probabilidades, color='#58a6ff', alpha=0.8, width=0.4, edgecolor='#0d1117', zorder=3, label="Simulado")
            self.ax.set_ylabel("Probabilidad Empírica")
            self.ax.set_xticks(valores)
        else:
            self.ax.hist(datos, bins=50, density=True, color='#238636', alpha=0.7, edgecolor='#0d1117', zorder=3, label="Simulado")
            self.ax.set_ylabel("Densidad de Probabilidad")

        if params is not None:
            if es_discreta:
                x_teo = np.arange(int(min(datos)), int(max(datos)) + 1)
                y_teo = np.zeros_like(x_teo, dtype=float)
                
                if indice == 3:   # Bernoulli
                    y_teo = stats.bernoulli.pmf(x_teo, params['p'])
                elif indice == 4: # Binomial
                    y_teo = stats.binom.pmf(x_teo, params['n'], params['p'])
                elif indice == 5: # Geométrica
                    y_teo = stats.geom.pmf(x_teo, params['p'])
                elif indice == 6: # Hipergeométrica
                    y_teo = stats.hypergeom.pmf(x_teo, params['N'], params['K'], params['n_m'])
                elif indice == 7: # Poisson
                    y_teo = stats.poisson.pmf(x_teo, params['lam'])
                
                self.ax.plot(x_teo, y_teo, color='#ff7b72', marker='o', linestyle='dashed', linewidth=2, markersize=6, label="Teórico", zorder=4)
                
            else:
                x_teo = np.linspace(min(datos), max(datos), 200)
                y_teo = np.zeros_like(x_teo, dtype=float)
                
                if indice == 0:   # Normal
                    y_teo = stats.norm.pdf(x_teo, loc=params['mu'], scale=params['sigma'])
                elif indice == 1: # Exponencial
                    y_teo = stats.expon.pdf(x_teo, scale=1/params['lam'])
                elif indice == 2: # Uniforme
                    y_teo = stats.uniform.pdf(x_teo, loc=params['a'], scale=params['b'] - params['a'])
                
                self.ax.plot(x_teo, y_teo, color='#ff7b72', linewidth=2.5, label="Teórico", zorder=4)

            self.ax.legend(facecolor='#161b22', edgecolor='#30363d', labelcolor='#c9d1d9')

        self.ax.set_title(titulo, fontsize=12, fontweight='bold')
        self.ax.set_xlabel("Variable Aleatoria (X)")
        self.ax.grid(True, color='#30363d', linestyle='--', alpha=0.5, zorder=0)
        self.fig.tight_layout()
        self.draw()


class MiSimulador(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("interfaz.ui", self)
        
        self.lienzo = Lienzo(self)
        self.layout_grafica.addWidget(self.lienzo)
        
        self.tabla_resultados.setRowCount(4)
        self.tabla_resultados.setHorizontalHeaderLabels(["Teórico", "Simulado", "Diferencia"])
        self.tabla_resultados.setVerticalHeaderLabels(["Probabilidad", "Media", "Varianza", "Desviación"])
        self.tabla_resultados.setMinimumHeight(185)
        self.tabla_resultados.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.tabla_resultados.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.tabla_resultados.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.tabla_resultados.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        self.combo_distribuciones.currentIndexChanged.connect(self.cambiar_formulario)
        self.boton_calcular.clicked.connect(self.ejecutar_calculo)
        self.boton_exportar.clicked.connect(self.exportar_imagen)

    def cambiar_formulario(self, indice):
        self.paginas_variables.setCurrentIndex(indice)

    def ejecutar_calculo(self):
        indice = self.combo_distribuciones.currentIndex()
        texto_expresion = self.input_expresion.text().strip()
        iteraciones_ui = self.spin_iteraciones.value()
        
        if not texto_expresion:
            self.statusBar().showMessage("Error: Ingresa una expresión válida (ej. 2 < X < 5)", 4000)
            return

        nombre_dist = self.combo_distribuciones.currentText()
        instancia = None
        es_discreta = False
        params = {}

        try:
            if indice == 0:
                instancia = Normal(self.spin_media.value(), self.spin_desviacion.value())
                params = {'mu': self.spin_media.value(), 'sigma': self.spin_desviacion.value()}
                es_discreta = False
            elif indice == 1:
                instancia = Exponencial(self.spin_lambda.value())
                params = {'lam': self.spin_lambda.value()}
                es_discreta = False
            elif indice == 2:
                instancia = Uniforme(self.spin_a.value(), self.spin_b.value())
                params = {'a': self.spin_a.value(), 'b': self.spin_b.value()}
                es_discreta = False
            elif indice == 3:
                instancia = Bernoulli(self.spin_p_ber.value())
                params = {'p': self.spin_p_ber.value()}
                es_discreta = True
            elif indice == 4:
                instancia = Binomial(self.spin_n_bin.value(), self.spin_p_bin.value())
                params = {'n': self.spin_n_bin.value(), 'p': self.spin_p_bin.value()}
                es_discreta = True
            elif indice == 5:
                instancia = Geometrica(self.spin_p_geo.value())
                params = {'p': self.spin_p_geo.value()}
                es_discreta = True
            elif indice == 6:
                instancia = Hipergeometrica(n=self.spin_n_muestra.value(), k=self.spin_K_exitos.value(), N=self.spin_N_pob.value())
                params = {'n_m': self.spin_n_muestra.value(), 'K': self.spin_K_exitos.value(), 'N': self.spin_N_pob.value()}
                es_discreta = True
            elif indice == 7:
                instancia = Poisson(self.spin_lam_poi.value())
                params = {'lam': self.spin_lam_poi.value()}
                es_discreta = True

            teorica, simulada, datos_simulados = instancia.evaluar_expresion(texto_expresion, iteraciones_ui)

            teo_media = instancia.esperanza() if hasattr(instancia, 'esperanza') else instancia.Esperanza()
            teo_var = instancia.varianza() if hasattr(instancia, 'varianza') else instancia.Varianza()
            teo_std = instancia.desviacion_estandar() if hasattr(instancia, 'desviacion_estandar') else instancia.Desviacion_Estandar()

            sim_media = np.mean(datos_simulados) if len(datos_simulados) > 0 else 0
            sim_var = np.var(datos_simulados) if len(datos_simulados) > 0 else 0
            sim_std = np.std(datos_simulados) if len(datos_simulados) > 0 else 0

            self.tabla_resultados.setItem(0, 0, QtWidgets.QTableWidgetItem(f"{teorica * 100:.4f} %"))
            self.tabla_resultados.setItem(0, 1, QtWidgets.QTableWidgetItem(f"{simulada * 100:.4f} %"))
            self.tabla_resultados.setItem(0, 2, QtWidgets.QTableWidgetItem(f"{abs(teorica - simulada) * 100:.4f} %"))
            
            self.tabla_resultados.setItem(1, 0, QtWidgets.QTableWidgetItem(f"{teo_media:.4f}"))
            self.tabla_resultados.setItem(1, 1, QtWidgets.QTableWidgetItem(f"{sim_media:.4f}"))
            self.tabla_resultados.setItem(1, 2, QtWidgets.QTableWidgetItem(f"{abs(teo_media - sim_media):.4f}"))
            
            self.tabla_resultados.setItem(2, 0, QtWidgets.QTableWidgetItem(f"{teo_var:.4f}"))
            self.tabla_resultados.setItem(2, 1, QtWidgets.QTableWidgetItem(f"{sim_var:.4f}"))
            self.tabla_resultados.setItem(2, 2, QtWidgets.QTableWidgetItem(f"{abs(teo_var - sim_var):.4f}"))
            
            self.tabla_resultados.setItem(3, 0, QtWidgets.QTableWidgetItem(f"{teo_std:.4f}"))
            self.tabla_resultados.setItem(3, 1, QtWidgets.QTableWidgetItem(f"{sim_std:.4f}"))
            self.tabla_resultados.setItem(3, 2, QtWidgets.QTableWidgetItem(f"{abs(teo_std - sim_std):.4f}"))
            
            self.lienzo.actualizar_grafica(datos_simulados, es_discreta, indice, params, titulo=f"Simulación Estocástica - {nombre_dist}")
            self.statusBar().showMessage(f"Cálculo exitoso para {nombre_dist}.", 3000)

        except Exception as e:
            self.tabla_resultados.clearContents()
            self.lienzo.ax.clear()
            self.lienzo.draw()
            self.statusBar().showMessage(f"Error en la expresión o parámetros: {str(e)}", 6000)

    def exportar_imagen(self):
        ruta_archivo, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, 
            "Exportar Análisis Gráfico", 
            "", 
            "Documento PDF (*.pdf);;Gráficos Vectoriales SVG (*.svg);;Imágenes PNG (*.png)"
        )
        
        if ruta_archivo:
            self.lienzo.fig.savefig(
                ruta_archivo, 
                facecolor=self.lienzo.fig.get_facecolor(), 
                edgecolor='none', 
                dpi=300, 
                bbox_inches="tight"
            )
            self.statusBar().showMessage(f"Gráfica exportada exitosamente: {ruta_archivo}", 4000)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ventana = MiSimulador()
    ventana.show()
    sys.exit(app.exec())