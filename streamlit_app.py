import altair as alt
import numpy as np
import pandas as pd
import streamlit as st
from calculator import exportString, stringToArray, infiniteXinfinite, infTextToInt2, condense, lcm

"""
# Infinite Number Calculator

The two numbers can be any number expressed with digits. Numbers with repeating digit sets are expressed with parenthesis around the digit set.
  Ex: 1.(3) = 1.3333...; (4)9 = ...4444449

Acceptable operations include '+' (addition), '-' (subtraction), '*' (multiplication), '/' (division), '//' (integer division), '%' (modulo), '^' (exponent), '=' (comparison)

Enter the same number of Relative Repetitions as Repeating Digit Sets. 

For example, (7) needs one Relative Repetition, such as [8]. (8)9(3) needs two, such as [0, -3]
"""

calcCol1, calcCol2 = st.columns(2)

num_points = calcCol1.text_input("First Number", placeholder="Enter a number")

firstRR = calcCol1.text_input('#1 Relative Repetitions',value="[0]", placeholder="ex: [10, -3]")

exportString = ""

num_points2 = calcCol1.text_input("Second Number", placeholder="Enter a number")

SecondtRR = calcCol1.text_input('#2 Relative Repetitions', value="[0]", placeholder="ex: [0, 0]")

operationRadio = calcCol2.radio("Select Operation",["\+","\-","\*","/","//","%","^","="],captions=["Addition","Subtraction","Multiplication","Division","Integer Division","Modulo","Exponent","Comparison"])


display_sum = infiniteXinfinite(num_points, num_points2, stringToArray(firstRR), stringToArray(SecondtRR), operationRadio)

st.text(display_sum)

