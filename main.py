from distribucionesDiscretas.Binomial import Binomial
from distribucionesDiscretas.Hipergeometrica import Hipergeometrica
from distribucionesDiscretas.Poisson import Poisson
from distribucionesDiscretas.Geometrica import Geometrica
from distribucionesDiscretas.Bernoulli import Bernoulli
from distribucionesContinuas.Normal import Normal

n = 9
p = 0.8
binomial = Binomial(n, p)

print("Binomial:")
print(f"Probabilidad de obtener exactamente 8 éxitos: {binomial.probabilidad_X(8):.6f}")


