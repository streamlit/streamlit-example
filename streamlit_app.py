import numpy as np
import matplotlib.pyplot as plt
import sympy as sym
import streamlit as st

st.title("Ejercicio numero 6")
st.text("Obtenga la Interpolación de Chebyshev desde cheby.npy. ¿Qué conclusiones obtiene? ¿Escriba el polinomio con sus coeficientes.")
st.text("cheby.npy = [[ 1  2  3  4  5  6  7  8  9 10][ 1  3  5  4  7  6 12 10 13 12]]")

#puntos
data = np.load('cheby.npy')
#data = [[0,0.2,0.3,0.4],[1,1.6,1.7,2.0]]
plt.plot(data[0],data[1],'o', label='Puntos',color='r')
plt.xlabel('F(x)')
plt.ylabel('T(s)')

#matriz de vandermounde
n = len(data[0])
D = np.zeros((n,n),dtype=float)

for i in range(n):
    for j in range(n):
        exp = n - 1 -j
        D[i,j]= data[0][i]**exp

#resolver la matriz
var = np.linalg.solve(D,data[1])
x = sym.Symbol('x')
pol = 0
for i in range(0,n,1):
    exp = (n-1)-i   # Derecha a izquierda
    t = var[i]*(x**exp)
    pol = pol + t

sym.pprint(pol)
#graficar el polinomio
fx = sym.lambdify(x,pol)
a = np.min(data[0]) #intervalo [a,b]
b = np.max(data[0])
px = np.linspace(a,b,100)
py = fx(px)
plt.plot(px,py,label='Interpolacion Chebyshev',color='b')
plt.grid()
plt.xticks([1,2,3,4,5,6,7,8,9,10])
plt.legend()

st.pyplot()
