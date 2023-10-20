import streamlit as st
import numpy as np
from scipy.integrate import quad 
from PIL import Image
from fractions import Fraction
import matplotlib.pyplot as plt

fig, ax = plt.subplots()

image = Image.open('HW2.png')
st.subheader('General Load Distributer', divider='rainbow')
st.image(image)

la = st.number_input('Type $$l_a$$ below', value=None, placeholder="la", label_visibility='visible')
lb = st.number_input('Type $$l_b$$ below', value=None, placeholder="lb", label_visibility='visible')
l = st.number_input('Type $$l$$ below', value=None, placeholder="l", label_visibility='visible')
a = st.number_input('Type $$a$$ below', value=None, placeholder="a", label_visibility='visible')
b = st.number_input('Type $$b$$ below', value=None, placeholder="b", label_visibility='visible')
f = st.number_input('Type $$f$$ below', value=None, placeholder="f", label_visibility='visible')
if(la == None): la = 0
if(lb == None): lb = 0
if(l == None): l = 0
if(a == None): a = 0
if(b == None): b = 0
if(f == None): f = 0

st.write(la,lb,l,a,b,f)
if st.button('Calculate'):
    #Declare variables
    x1 = la
    x2 = la + l
    x3 = la + l/2
    c = (a+b)/2 + f

    #Augmented matrix
    st.latex(r'''\left[\begin{array}{ccc|c}  
    ''' + str(x3**2) + r''' & ''' + str(x3) + r''' & 1 & ''' + str(c) + r'''\\  
    ''' + str(x2**2) + r''' & ''' + str(x2) + r''' & 1 & ''' + str(b) + r'''\\
    ''' + str(x1**2) + r''' & ''' + str(x1) + r''' & 1 & ''' + str(a) + r'''
    \end{array}\right]''')

    #Solve for F(x)
    m1 = np.array([[x3**2,x3,1],[x2**2,x2,1],[x1**2,x1,1]])
    m2 = np.array([c,b,a])
    try:
        m3 = np.linalg.solve(m1, m2)
        
        t = np.linspace(la,la+l,100)
        ax.plot(t, m3[0]*t**2 + m3[1]*t + m3[2], color='black')
        ax.plot([la,la],[0,a], color = 'black')
        ax.plot([la+l,la+l],[0,b], color = 'black')
        ax.plot([la,la+l],[0,0], color = 'black')
        ax.fill_between(t, m3[0]*t**2 + m3[1]*t + m3[2], 0*t, alpha = 0.5, color = 'orange')
        plt.xlabel("Length (m)")
        plt.ylabel("Load Value (kN)")
        st.pyplot(fig)

        #Show F(x) equation
        st.latex(r'''F(x) = ''' + str(m3[0]) + r'''x^2 + ''' + str(m3[1]) + r'''x + ''' + str(m3[2]) + r'''''')
        
        #Integrate F(x) to find resultant
        def f(x): return m3[0]*x**2 + m3[1]*x + m3[2]
        I = quad(f, la, l+la)[0]
        
        #Show resultant
        st.latex(r'''F_{resultant} = \int_{''' + str(la) + r'''}^{''' + str(la+l) + r'''}F(x)dx = ''' + str(np.round(-1*I,decimals=2)) + r'''\; kN''')
        
        #Integrate F(x)*x to find moment at A
        def g(x): return m3[0]*x**3 + m3[1]*x**2 + m3[2]*x
        J = quad(g, la, l+la)[0]

        #Show moment around A
        st.latex(r'''M_{A} = \int_{''' + str(la) + r'''}^{''' + str(la+l) + r'''}F(x)\cdot x \;dx = ''' + str(np.round(-1*J,decimals=2)) + r'''\; kN''')    
        
        #Find and show centroid of load
        xc = J/I
        st.latex(r'''x_c = ''' + str(np.round(xc,decimals=2)) + r'''\; m''')
        
        #Find and show the moment around B
        K = I*(la+l-xc)
        st.latex(r'''M_{B} = \int_{''' + str(la) + r'''}^{''' + str(la+l) + r'''}F(x)\cdot (L-x) \;dx = ''' + str(np.round(K,decimals=2)) + r'''\; kN''')
    except:
        st.write('Cannot compute, check if matrix is singular')
st.button("Reset", type="primary")

