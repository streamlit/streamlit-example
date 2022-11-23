import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import medfilt,wiener,detrend
from PIL import Image, ImageDraw
import sympy as sym
import cv2

st.title("#Proyecto #2 – INFO 1128")
st.write('**Pregunta 1:** Dada la siguiente figura obtenga los momentos invariantes de Hu (H1-H7) y la Tabla Resumen. Programe un script en Python que obtenga los Hu(i=1..7) de cada una de las vocales. Puede utilizar CV2.')
g1=Image.open("g1.png")
st.image(g1, caption='Grafico de la actividad')
img=Image.open("vocales.png")
a = img.crop((0, 0, 110, 222))
a.save("a.png")
e= img.crop((130, 0, 230, 222))
e.save("e.png")
i= img.crop((230, 0, 310, 222))
i.save("i.png")
o= img.crop((320, 0, 420, 222))
o.save("o.png")
u= img.crop((440, 0, 550, 222))
u.save("u.png")

list=["a.png","e.png","i.png","o.png","u.png"]

c=0
sol = []
while c!=5:
    # Read the input image
    img = cv2.imread(list[c])
    # Read image as grayscale image
    im = cv2.imread(list[c],cv2.IMREAD_GRAYSCALE)
    # Threshold image
    _,im = cv2.threshold(im, 128, 255, cv2.THRESH_BINARY)
        # Calculate Moments
    moments = cv2.moments(im)
    # Calculate Hu Moments
    huMoments = cv2.HuMoments(moments)
    sol.append(huMoments)
    c+=1
sol2 =np.array(sol)
st.text(sol2)
#for i in sol2:
    #st.table(i)
st.write('**Conclusiones:**')
st.write('**Pregunta 2:** Coloque cada una las siguientes imágenes en la posición señalada dentro de la plantilla de salida. Debe redimensionar y rotar las figuras. Programe un script en Python + Pygame + PIL.')
g2=Image.open("g2.png")
st.image(g2, caption='Grafico de la actividad')
base=Image.open("plantilla.png")
dibujo = ImageDraw.Draw(base)
sobre=Image.open("figuras.png")

#-----------IMAGEN 1---------------
fig = sobre.crop((4, 4, 221, 222))
figr=fig.resize((fig.height-100,fig.width-100))
region = figr.rotate(-10,expand=1)
rgba = region.convert("RGBA")
datas = rgba.getdata()
newData = []
for item in datas:
    if item[0] == 0 and item[1] == 0 and item[2] == 0:  # finding black colour by its RGB value
        # storing a transparent value when we find a black colour
        newData.append((255, 255, 255, 0))
    else:
        newData.append(item)  # other colours remain unchanged
  
rgba.putdata(newData)
base.paste(rgba,(5,15))
#-----------IMAGEN 2---------------
fig = sobre.crop((242, 4, 484, 207))
figr=fig.resize((fig.height-85,fig.width-120))
region = figr.rotate(10,expand=1)
rgba = region.convert("RGBA")
datas = rgba.getdata()
newData = []
for item in datas:
    if item[0] == 0 and item[1] == 0 and item[2] == 0:  # finding black colour by its RGB value
        # storing a transparent value when we find a black colour
        newData.append((255, 255, 255, 0))
    else:
        newData.append(item)  # other colours remain unchanged
  
rgba.putdata(newData)
base.paste(rgba,(200,20))
#-----------IMAGEN 3---------------

fig = sobre.crop((503, 23, 723, 198))
figr=fig.resize((fig.height-55,fig.width-105))
region = figr.rotate(-40,expand=1)
rgba = region.convert("RGBA")
datas = rgba.getdata()
newData = []
for item in datas:
    if item[0] == 0 and item[1] == 0 and item[2] == 0:  # finding black colour by its RGB value
        # storing a transparent value when we find a black colour
        newData.append((255, 255, 255, 0))
    else:
        newData.append(item)  # other colours remain unchanged
  
rgba.putdata(newData)
base.paste(rgba,(380,10))

#-----------IMAGEN 4---------------
fig = sobre.crop((733, 19, 980, 202))

figr=fig.resize((fig.height-70,fig.width-130))
region = figr.rotate(23,expand=1)
rgba = region.convert("RGBA")
datas = rgba.getdata()
newData = []
for item in datas:
    if item[0] == 0 and item[1] == 0 and item[2] == 0:  # finding black colour by its RGB value
        # storing a transparent value when we find a black colour
        newData.append((255, 255, 255, 0))
    else:
        newData.append(item)  # other colours remain unchanged
  
rgba.putdata(newData)
base.paste(rgba,(600,10))

base.save("plantillanew.png")
sol2 = Image.open('plantillanew.png')
st.image(sol2, caption='Solucion a la pregunta')

st.write('**Pregunta 3:** Aplique Least Square Polymonial mediante poly1d() y polyfit(). Utilice f1.npy y f2.npy para obtener el siguiente gráfico. Utilice x = np.arange(start=1,stop=50,step=1).')
g3 = Image.open('g3.png')
st.image(g3, caption='Grafico de la actividad')


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

