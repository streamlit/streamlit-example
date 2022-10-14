import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import medfilt,wiener,detrend
from PIL import Image, ImageDraw
import pandas as pd

st.title("#Proyecto #2 – INFO 1128")
st.write('**Pregunta 1:** Dada la siguiente figura obtenga los momentos invariantes de Hu (H1-H7) y la Tabla Resumen. Programe un script en Python que obtenga los Hu(i=1..7) de cada una de las vocales. Puede utilizar CV2. ¿Qué conclusión obtiene al analizar la Tabla Resumen? Explique claramente y con detalle.')
g1=Image.open("g1.png")
st.image(g1, caption='Grafico de la actividad')
st.write('**Solucion:** el problema nos solicita obtener los momentos de hu de una imagen que contiene distintos objetos o letras, con el cual se debe aplicar un logaritmo mostrar sus respectivos resultados')
st.write('Primeramente, se debe importar las librerías correspondientes, en este caso se trabajará con cv2 para el manejo de imagenes y numpy para los manejos matemáticos; en segundo lugar, se debe convertir la imagen a escala de grises con cv2 para que pueda ser manejable por el programa; se debe obtener la letra de la serie de imagen, por lo cual se deberá generar un rango de pixeles donde se encuentra la figura, luego, calcular los momentos normales y en consiguiente calcular los momentos de hu con cv2, aplicándole un valor absoluto para que no ocurra errores al calcular el logaritmo de este, donde se aplica con numpy y por ultimo para mostrar los datos correctos al anterior resultado se le aplica el valor absoluto y se muestran cada momento. Obteniendose la siguiente tabla:')
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
st.write('**Conclusiones:** Al analizar los momentos de hu de las diferentes imágenes podemos concluir que sus valores son casi similares, ya que las dimensiones son similares y como los momentos indican que podemos reconocer las letras en diferentes posiciones (traslaciones), orientaciones (rotaciones) , ya que se mantienen dando los mismos resultados, pero estos cambian dependiendo del área en el que estén, si el rango de la imagen varia se obtienen resultados distintos, de lo contrario con sus mismas dimensiones estos deberían dar los mismos resultados independiente de la posición ')
st.write('**Pregunta 2:** Coloque cada una las siguientes imágenes en la posición señalada dentro de la plantilla de salida. Debe redimensionar y rotar las figuras. Programe un script en Python + Pygame + PIL.')
g2=Image.open("g2.png")
st.image(g2, caption='Grafico de la actividad')

st.write('**Solucion:** el problema nos indica que con respecto a la imagen proporcionada la cual es un conjunto de imágenes consecutivas, tener que manipularlas de tal forma que debe quedar igual a la plantilla facilitada, utilizando las librerías Python, pygame y pillow.')
st.write('Primeramente, se debe importar las librerías correspondientes, en este caso se trabajará con pillow para el manejo de imágenes; en segundo lugar, se debe definir la base con la que trabajaremos y las figuras que insertaremos en esta, por lo cual la plantilla se utilizo de base con ImageDraw.Draw, por consiguiente se realizó un recorte sobre el perímetro de las imágenes crop, luego redimensionarlas con resize, posteriormente rotarlas en grados con rotate, y expandirlas para que no se recortara la imagen, este nos resulta en su imagen rotada pero con un fondo negro, por lo cual se manipulo y se convirtió en un fondo transparente manipulando los valores rgb, luego reemplazando, para finalmente ubicarlas sobre la plantilla con paste e indicando los pixeles en x e y. Obteniendose la siguiente imagen')

sol2 = Image.open('plantillanew.png')
st.image(sol2, caption='Solucion a la pregunta')

st.write('**Pregunta 3:** Aplique Least Square Polymonial mediante poly1d() y polyfit(). Utilice f1.npy y f2.npy para obtener el siguiente gráfico. Utilice x = np.arange(start=1,stop=50,step=1).')
g3 = Image.open('g3.png')
st.image(g3, caption='Grafico de la actividad')
st.write('**Solucion:** el problema nos indica que debemos graficar los datos dados en unos archivos aplicando Least Square Polymonial tal que el grafico quede similar al proporcionado, con líneas que cruzan los puntos.')
st.write('primeramente, se debe importar las librerías correspondientes, en este caso se trabajará con pyplot para las graficas y numpy para las lecturas y manejos matematicos. Obteniendose la siguiente grafica')
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
st.write('**Observacion:** El filtro Wiener lo que busca es reducir el ruido de la imagen, y se basa en que este es un proceso aleatorio independiente de la posicion este posee un filtro de peso bajo, lo cual consiste en que realiza cortes de frecuencias bajos en zonas con poco detalle, a comparacion de zonas con altos niveles de detalle. este se realiza de tal forma que la salida de cada posicion, es la suma media de local de una ventana de filtro con un termino de contraste local de tal forma que este ultimo sea mayor en zonas de altos detalles.')
st.write('El filtro de median lo que hace es reemplazar el valor de cada una de las posiciones de la funcion, y reemplazarlo con la media de las posiciones adyacentes. Para esto se define el tamaño de la ventana de filtro (kernel) en donde operara la funcion, a mientras mayor sea el rango, la señal tiende a simplificarse.')
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
st.write('**Observacion:** Mientras mas grande es la ventana de filtro, la señal tiende mas a ser una linea recta, esto debido a que la ventana cubre casi la totalidad de la onda y el calculo se simplifica a la media de esta misma')

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

st.write('**Solucion:** Para resolver esta pregunta deberemos aplicar el metodo de interpolacion de chevyshev, conociendo los puntos por los que pasa la funcion, utilizaremos la libreria numpy.polynomial.chebyshev') 
st.write('**Observacion:** Chevishev no invento un metodo de interpolacion, si no bautizo a un conjunto de polinomios que cumplen la caracteristica de que en el intervalo [-1,1] su rango de valores esta en el rango de [-1,1], sin embargo, lo que haremos sera forzar la creacion de un polinomio de este tipo con los puntos conocidos, mediante la funcion numpy.polynomial.chebyshev') 

st.write('**Intervalo a graficar:**')
Imin = st.slider("valor minimo", -25, 25, 1,1)
Imax = st.slider("valor maximo", -25, 25, 10,1)
fig = plt.figure(figsize=(10,4))
ax = plt.axes()
#puntos
data = np.load("cheby.npy")
x=data[0]
y=data[1]

Vander=np.polynomial.chebyshev.chebvander(x,len(x)-1)
M=np.linalg.solve(Vander,y)
pol= np.polynomial.Chebyshev(M)
print(pol)
x = np.linspace(Imin,Imax,100)
y = pol(x)
plt.plot(x,y,label='Interpolacion Chebyshev',color='b')
plt.plot(data[0],data[1],'o', label='Puntos',color='r')
plt.xlabel('F(x)')
plt.ylabel('T(s)')
plt.grid()
plt.xticks([1,2,3,4,5,6,7,8,9,10])
plt.legend()
plt.show()

st.pyplot(fig)
plt.close()
st.write('**Polinomio obtenido:**',pol)
st.write('**Conclusiones:** a partir de lo obtenido podemos decir que la interpolacion se trata de encontrar una funcion la cual cumpla que pase por cada uno de los puntos conocidos, en donde esperamos predecir los valores que no conocemos, sin embargo se puede obtener una aproximacion conociendo los valores del entorno. Ademas los aportes de chebyshev ayudan considerablemente a reducir la cota superior, simplificando considerablemente los calculos realizados')
