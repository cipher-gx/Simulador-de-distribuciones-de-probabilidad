import sys
import numpy as np
from PyQt6 import QtWidgets, uic
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

    def actualizar_grafica(self, datos, es_discreta, titulo="Distribución"):
        self.ax.clear()
        if datos is None or len(datos) == 0:
            self.draw()
            return

        if es_discreta:
            valores, frecuencias = np.unique(datos, return_counts=True)
            probabilidades = frecuencias / len(datos)
            self.ax.bar(valores, probabilidades, color='#58a6ff', alpha=0.8, width=0.4, edgecolor='#0d1117', zorder=3)
            self.ax.set_ylabel("Probabilidad Empírica")
            self.ax.set_xticks(valores)
        else:
            self.ax.hist(datos, bins=50, density=True, color='#238636', alpha=0.7, edgecolor='#0d1117', zorder=3)
            self.ax.set_ylabel("Densidad de Probabilidad")

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
        
        self.combo_distribuciones.currentIndexChanged.connect(self.cambiar_formulario)
        self.boton_calcular.clicked.connect(self.ejecutar_calculo)
        self.boton_exportar.clicked.connect(self.exportar_imagen)
        
        self.statusBar().showMessage("Motores matemáticos unificados enlazados correctamente.", 5000)

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

        try:
            if indice == 0:    # Normal
                instancia = Normal(self.spin_media.value(), self.spin_desviacion.value())
                es_discreta = False
                
            elif indice == 1:  # Exponencial
                instancia = Exponencial(self.spin_lambda.value())
                es_discreta = False
                
            elif indice == 2:  # Uniforme
                instancia = Uniforme(self.spin_a.value(), self.spin_b.value())
                es_discreta = False
                
            elif indice == 3:  # Bernoulli
                instancia = Bernoulli(self.spin_p_ber.value())
                es_discreta = True
                
            elif indice == 4:  # Binomial
                instancia = Binomial(self.spin_n_bin.value(), self.spin_p_bin.value())
                es_discreta = True
                
            elif indice == 5:  # Geométrica
                instancia = Geometrica(self.spin_p_geo.value())
                es_discreta = True
                
            elif indice == 6:  # Hipergeométrica 
                instancia = Hipergeometrica(
                    n=self.spin_n_muestra.value(), 
                    k=self.spin_K_exitos.value(), 
                    N=self.spin_N_pob.value()
                )
                es_discreta = True
                
            elif indice == 7:  # Poisson
                instancia = Poisson(self.spin_lam_poi.value())
                es_discreta = True


            teorica, simulada, datos_simulados = instancia.evaluar_expresion(texto_expresion, iteraciones_ui)

            self.label_teorica.setText(f"Teórica: {teorica * 100:.4f} %")
            self.label_simulada.setText(f"Simulada: {simulada * 100:.4f} %")
            
            self.lienzo.actualizar_grafica(datos_simulados, es_discreta, titulo=f"Simulación Monte Carlo - {nombre_dist}")
            self.statusBar().showMessage(f"Cálculo exitoso para {nombre_dist}.", 3000)

        except Exception as e:
            self.label_teorica.setText("Teórica: -- %")
            self.label_simulada.setText("Simulada: -- %")
            self.lienzo.ax.clear()
            self.lienzo.draw()
            self.statusBar().showMessage(f"Error en la expresión: {str(e)}", 6000)

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