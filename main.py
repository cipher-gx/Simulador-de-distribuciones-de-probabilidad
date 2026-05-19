from distribucionesDiscretas.Binomial import Binomial
from distribucionesDiscretas.Hipergeometrica import Hipergeometrica
from distribucionesDiscretas.Poisson import Poisson
from distribucionesDiscretas.Geometrica import Geometrica
from distribucionesDiscretas.Bernoulli import Bernoulli

n = 10
p = 0.5
binomial = Binomial(n, p)

print("Esperanza:", binomial.esperanza())
print("Varianza:", binomial.varianza())
print("P(X=3):", binomial.probabilidad_X(3))
print("P(2 < X < 5):", binomial.probabilidad_x1_a_x2(3, 4))
print("Evaluar expresión '2 <= X <= 5':", binomial.evaluar_expresion("Holaa evalua 2 < X < 5"))


hypergeometrica = Hipergeometrica(n=10, k=5, N=20)
print("Esperanza:", hypergeometrica.esperanza())
print("Varianza:", hypergeometrica.varianza())
print("P(X=3):", hypergeometrica.probabilidad_X(3))
print("P(2 < X < 5):", hypergeometrica.probabilidad_x1_a_x2(3, 4))
print("Evaluar expresión '2 < X < 5':", hypergeometrica.evaluar_expresion("Holaa evalua 2 < X < 5"))

poisson = Poisson(l=3)
print("Esperanza:", poisson.esperanza())
print("Varianza:", poisson.varianza())
print("P(X=3):", poisson.probabilidad_X(3))
print("P(2 < X < 5):", poisson.probabilidad_x1_a_x2(3, 4))
print("Evaluar expresión '2 < X < 5':", poisson.evaluar_expresion("Holaa evalua 2 < X < 5"))

geometrica = Geometrica(p=0.5)
print("Esperanza:", geometrica.esperanza())
print("Varianza:", geometrica.varianza())
print("P(X=3):", geometrica.probabilidad_X(3))
print("P(2 < X < 5):", geometrica.probabilidad_x1_a_x2(3, 4))
print("Evaluar expresión '2 < X < 5':", geometrica.evaluar_expresion("Holaa evalua 2 < X < 5"))

bernoulli = Bernoulli(p=0.5)
print("Esperanza:", bernoulli.esperanza())
print("Varianza:", bernoulli.varianza())
print("P(X=1):", bernoulli.probabilidad_X(1))
print("P(X=0):", bernoulli.probabilidad_X(0))
print("Evaluar expresión 'X  1':", bernoulli.evaluar_expresion("Holaa evalua X < 1"))


