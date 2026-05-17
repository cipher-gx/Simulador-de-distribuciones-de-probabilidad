from distribucionesDiscretas.Binomial import Binomial

n = 10
p = 0.5
binomial = Binomial(n, p)

print("Esperanza:", binomial.esperanza())
print("Varianza:", binomial.varianza())
print("P(X=3):", binomial.probabilidad_X(3))
print("P(2 <= X <= 5):", binomial.probabilidad_x1_a_x2(2, 5))