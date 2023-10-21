import streamlit as st
import numpy as np
from scipy.integrate import quad 
from PIL import Image
from fractions import Fraction
import matplotlib.pyplot as plt

fig, ax = plt.subplots()


st.subheader('General Distributed Load Analysis By Kuval Bora', divider='rainbow')
image = Image.open('HW2.png')
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
        st.latex(r'''p(x) = ''' + str(m3[0]) + r'''x^2 + ''' + str(m3[1]) + r'''x + ''' + str(m3[2]) + r'''''')
        
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
        K = I*(la+l+lb-xc)
        st.latex(r'''M_{B} = F_{resultant}\cdot (l_a+l+l_b-x_c) \;dx = ''' + str(np.round(K,decimals=2)) + r'''\; kN''')
        
        #Supports code
        st.header('Supports')
        
        #Support 1
        st.subheader('Support 1', divider='rainbow')
        image = Image.open('S1.png')
        st.image(image)
        st.latex(r'''
        \Sigma F_x = R_1cos45^o + R_2cos45^o - R_3cos45^o = 0\\
        \Sigma F_y = -R_1sin45^o + R_2sin45^o + R_3sin45^o - F= 0\\
        \Sigma M_a = M_{aF} + R_3sin45^o''')
        #Support 2
        st.subheader('Support 2', divider='rainbow')
        image = Image.open('S2.png')
        st.image(image)

        #Support 3
        st.subheader('Support 3', divider='rainbow')
        image = Image.open('S3.png')
        st.image(image)
        
        
        #Methods text (Not computing anything)
        st.subheader('Methods', divider='rainbow')
        st.write('First, I made a generalized quadratic equation')
        st.latex(r'''p(x) = Ax^2 + Bx + C''')
        st.write('Then, I found the three points proivded by the generalization image (seen at the top)')
        st.latex(r'''p(l_a) = a \\ p(l_a + l) = b \\ p(l_a + \frac{l}{2}) = \frac{a+b}{2} + f''')
        st.write('''Then, I made a matrix of all the solutions to find A,B, and C.
                 Note that the coefficient for C (third column) is 1 for all cases, because there are no cofficients for that variable.''')
        st.latex(r'''\left[\begin{array}{ccc|c}  
        ''' + str(x3) + r'''^2 & ''' + str(x3) + r''' & 1 & ''' + str(c) + r'''\\  
        ''' + str(x2) + r'''^2 & ''' + str(x2) + r''' & 1 & ''' + str(b) + r'''\\
        ''' + str(x1) + r'''^2 & ''' + str(x1) + r''' & 1 & ''' + str(a) + r'''
        \end{array}\right]''')
        st.write('This evaluates to: ')
        st.latex(r'''\left[\begin{array}{ccc|c}  
        ''' + str(x3**2) + r''' & ''' + str(x3) + r''' & 1 & ''' + str(c) + r'''\\  
        ''' + str(x2**2) + r''' & ''' + str(x2) + r''' & 1 & ''' + str(b) + r'''\\
        ''' + str(x1**2) + r''' & ''' + str(x1) + r''' & 1 & ''' + str(a) + r'''
        \end{array}\right]''')
        st.write('Now we can solve this Matrix like so:')
        st.latex(r'''[A | b]''')
        st.latex(r'''bA^{-1} = \begin{bmatrix}A\\B\\C\end{bmatrix}''')
        st.write('In this case the matrix evaluates to:')
        st.latex(r'''\begin{bmatrix}A\\B\\C\end{bmatrix} = \begin{bmatrix}''' + str(m3[0]) + r'''\\''' + str(m3[1]) + r'''\\''' + str(m3[2]) + r'''\end{bmatrix}''')
        st.write('Using this, we eventually get the p(x) equation seen above and evaluate')
    except:
        st.write('Cannot compute, check if matrix is singular')
st.button("Reset", type="primary")

