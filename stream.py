import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import medfilt,wiener,detrend
from PIL import Image, ImageDraw
import sympy as sym
import pandas as pd

st.title("#Proyecto #2 – INFO 1128")
st.write('**Pregunta 1:** Dada la siguiente figura obtenga los momentos invariantes de Hu (H1-H7) y la Tabla Resumen. Programe un script en Python que obtenga los Hu(i=1..7) de cada una de las vocales. Puede utilizar CV2.')
g1=Image.open("g1.png")
st.image(g1, caption='Grafico de la actividad')
resultados = np.array(([-2.76677952,-6.92286543,-10.26341753,-9.63246675,-19.58147865,-13.20587622,-20.7346789],
                    [-2.86997055,-6.62912557,-11.27096333,-11.21889071,-22.48086458,-15.08023758,-23.02484045],
                    [-2.91051886,-6.81194856,-10.3543975,-9.92918996,-20.22375921,-13.81596346,-20.21926147],
                    [-2.79289785,-8.09250288,-10.3108734,-9.43646346,-19.39956437,-13.48668572,-19.5459451],
                    [-2.77848784,-6.63761266,-10.90001363,-10.42824618,-21.86198961,-13.9458709,-21.09874225]
), dtype=np.float32)

df = pd.DataFrame(
   resultados,
   
   columns=('Log(H%d)' % (i+1) for i in range(7)))
df.index = ['A', 'E', 'I', 'O', 'U']

st.table(df)
st.write('**Conclusiones:**')
st.write('**Pregunta 2:** Coloque cada una las siguientes imágenes en la posición señalada dentro de la plantilla de salida. Debe redimensionar y rotar las figuras. Programe un script en Python + Pygame + PIL.')
g2=Image.open("g2.png")
st.image(g2, caption='Grafico de la actividad')

sol2 = Image.open('plantillanew.png')
st.image(sol2, caption='Solucion a la pregunta')

st.write('**Pregunta 3:** Aplique Least Square Polymonial mediante poly1d() y polyfit(). Utilice f1.npy y f2.npy para obtener el siguiente gráfico. Utilice x = np.arange(start=1,stop=50,step=1).')
g3 = Image.open('g3.png')
st.image(g3, caption='Grafico de la actividad')
data1 = np.load('f1.npy')
data2 = np.load('f2.npy')
fig = plt.figure(figsize=(10,4))
ax = plt.axes()

x = np.arange(start=1,stop=50,step=1)

y1=np.poly1d(data1)
fit1 = np.polyfit(x, y1, 1)
p1 = np.poly1d(fit1)
plt.plot(x, y1, '.',x,p1(x),color='black')
plt.plot(x,y1,'o', label='F1(x,deg=1)',color='blue')
y2=np.poly1d(data2)
fit2 = np.polyfit(x, y2, 2)
p2 = np.poly1d(fit2)
plt.plot(x, y2, '.', x, p2(x),color='black')
plt.plot(x,y2,'o', label='F2(x,deg=2)',color='orange')
plt.xlabel('T(s)')
plt.ylabel('F(x)')
plt.grid()
plt.title('Least Square Polymonial')
plt.legend()
st.pyplot(fig)
plt.close()

st.write('**Pregunta 4:** Dada la señal signal.npy aplique los filtros Median y Wiener para obtener el siguiente gráfico. Investigue sobre el módulos scipy.signal.')
g4 = Image.open('g4.png')
st.image(g4, caption='Grafico de la actividad')

st.write('**Solucion:** Se nos solicita aplicar los filtros Median y Wiener, para el cual los valores de la ventana de filtro fueron los predeterminados (3), tambien podemos editar los valores del filtro para visualizar como seria la señal con un valor distinto')

data = np.load('signal.npy')
Mkernel = st.slider("Filtro Median: Tamaño de la ventana de filtro", 1, 201, 3,2)
Wkernel = st.slider("Filtro Wiener: Tamaño de la ventana de filtro", 1, 101, 3,2)
w = wiener(data,Mkernel)
m = medfilt(data,Wkernel)

fig = plt.figure(figsize=(10,4))
ax = plt.axes()
plt.plot(data, label = 'Señal original')
plt.plot(m, label = 'filtro Median')
plt.plot(w, label = 'filtro Wiener')
plt.xlabel('T(s)')
plt.ylabel('señal')
plt.title('filtro de señales')
plt.legend()
plt.grid()
st.pyplot(fig)
plt.close()


st.write('**Pregunta 5:** Separe la tendencia de la señal. Obtenga un gráfico similar. Complete el código.')
g5 = Image.open('g5.png')
st.image(g5, caption='Grafico de la actividad')

t = np.linspace(0,5,100)
x = t + np.random.normal(size=100)

st.write('**Solucion:** En el script presentado se nos presenta una serie con una tendencia t, por lo que debemos es hallar la serie sin tendencia, lo cual lo hemos calculado con ayuda de la funcion signal.detrend()')
st.write('**Observacion:** en el script presentado se obtienen valores aleatorios en el intervalo (0,5), por lo que variara cada vez que se ejecute el programa')
NoT = detrend(x)

#ajuste = st.slider("ajuste", 0, 100, 0,1)
#NoT = detrend(x, bp=ajuste)

fig = plt.figure(figsize=(10,4))
ax = plt.axes()
plt.plot(t,x, label = 'serie con tendencia')
plt.plot(t,NoT, label = 'serie sin tendencia')
plt.legend()
st.pyplot(fig)
plt.close()

st.write('**Pregunta 6:** Obtenga la Interpolación de Chebyshev desde cheby.npy. ¿Qué conclusiones obtiene? ¿Escriba el polinomio con sus coeficientes.')
g6 = Image.open('g6.png')
st.image(g6, caption='Grafico de la actividad')

st.write('**Solucion:** Para resolver esta pregunta deberemos aplicar el metodo de interpolacion de chevyshev, conociendo los puntos por los que pasa la funcion')
st.write('**Observacion:** Chevishev no invento un metodo de interpolacion, si no bautizo a un conjunto de polinomios que cumplen la caracteristica de que en el intervalo [-1,1] su rango de valores esta en el rango de [-1,1], sin embargo el presente polinomio no cumple dicha caracteristica. Este conjunto tiene la peculariedad de que mediante el **metodo de interpolacion de Lagrange** se reduce significativamente la cota superior') 

st.write('**Intervalo a graficar:**')
Imin = st.slider("valor minimo", -25, 25, 1,1)
Imax = st.slider("valor maximo", -25, 25, 10,1)
#puntos
data = np.load('cheby.npy')
fig = plt.figure(figsize=(10,4))
ax = plt.axes()
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
a = np.min(Imin) #intervalo [a,b]
b = np.max(Imax)
px = np.linspace(a,b,100)
py = fx(px)
plt.plot(px,py,label='Interpolacion Chebyshev',color='b')
plt.grid()
plt.xticks([1,2,3,4,5,6,7,8,9,10])
plt.legend()

st.pyplot(fig)
plt.close()
st.write('**Polinomio obtenido:**',pol)
st.write('**Conclusiones:** a partir de lo obtenido podemos decir que la interpolacion se trata de encontrar una funcion la cual cumpla que pase por cada uno de los puntos conocidos, en donde esperamos predecir los valores que no conocemos, sin embargo se puede obtener una aproximacion conociendo los valores del entorno')
