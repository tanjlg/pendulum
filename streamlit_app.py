# -*- coding: utf-8 -*-
"""
Spyder Editor

Tan Jing Long
1st November 2021

This is a Python script for deployment on Streamlit.

The Streamlit app is intended to digitise the classic pendulum experiment we perform in secondary school, particularly for the data tabulation and analysis aspects.

The content for the pendulum experiment is standard. Here, I have adapted it from Physics Matters Practical Book (3rd ed.) by Charles Chew and Ho Boon Tiong.
"""

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import streamlit as st
from sklearn.linear_model import BayesianRidge, LinearRegression, ARDRegression
from sklearn.metrics import mean_squared_error
from PIL import Image

st.title('Pendulum Experiment')
st.header('Part I: Data Collection')
st.write('In Part I of the experiment, you will be physically performing the experiment and collecting the data in the laboratory.')

st.subheader('Aim')
st.write('To investigate the relationship between the period and the length of a simple pendulum')

st.subheader('Apparatus')
image1 = Image.open('./media/apparatus.jpg')
st.image(image1, caption='Figure 1: Apparatus')

st.write('Retort stand  \n',
         'Sets of boss and clamp  \n',
         'Split cork  \n',
         'Thread (approximately 120 cm long)  \n',
         'Pair of scissors  \n',
         'Metre rule  \n',
         'Bob weight  \n',
         'Stopwatch  \n',
         'Protractor')

image2 = Image.open('./media/exptsetup_side.jpg')
st.image(image2, caption='Figure 2: Experimental Set-up',)

length, t1, t2 = np.empty(6), np.empty(6), np.empty(6)

st.subheader('Procedure')
st.markdown("1. Set-up the experiment as in Figure 1 above, with the thread held tighly by the split cork.")
image3a = Image.open('./media/splitcork_unfixed.jpg')
image3b = Image.open('./media/splitcork_knot.jpg')
image3c = Image.open('./media/splitcork_fixed.jpg')
st.image([image3a, image3b, image3c],
         caption='Figure 3: Assembly of Split Cork',
         width=244)

st.markdown("2. Adjust the thread such that the length of the pendulum $𝑙$ is appoximately one metre.")
length[0] = st.number_input('Measure the length of the pendulum in centimetres.',
                     value=100.0, step=0.1)

st.markdown("3. Set the pendulum into oscillation by displacing the pendulum bob to one side by a small angle (less than $10^\circ$) and then releasing it. The motion of the pendulum from the point of release to the rightmost point and then back to the leftmost point is an example of a complete oscillation (video below). Ensure that the pendulum oscillates in a vertical plane instead of tracing a cone.")

video_file = open('./media/technique.mp4', 'rb')
video_bytes = video_file.read()
st.video(video_bytes)

st.markdown("4. Record the time $t_1$ taken for 20 oscillations using a stopwatch, in seconds.")
t1[0] = st.number_input(label='First reading', step=0.1)
st.markdown("5. Repeat step 3 and record the time $t_2$ for another 20 oscillations, in seconds.")
t2[0] = st.number_input(label='Second reading', step=0.1)

st.markdown('Repeat steps 3-4 with five more values of $l$ varying from 100.0 cm to 30.0 cm.')

length[1] = st.number_input('Measure the length of the pendulum in centimetres.',
                     value=90.0, step=0.1)
t1[1] = st.number_input(label='First reading of time taken for 20 oscillations for length of approximately 80-100 cm', step=0.1)
t2[1] = st.number_input(label='Second reading of time taken for 20 oscillations for length of approximately 80-100 cm', step=0.1)

length[2] = st.number_input('Measure the length of the pendulum in centimetres.',
                     value=70.0, step=0.1)
t1[2] = st.number_input(label='First reading of time taken for 20 oscillations for length of approximately 60-80 cm', step=0.1)
t2[2] = st.number_input(label='Second reading of time taken for 20 oscillations for length of approximately 60-80 cm', step=0.1)

length[3] = st.number_input('Measure the length of the pendulum in centimetres.',
                     value=60.0, step=0.1)
t1[3] = st.number_input(label='First reading of time taken for 20 oscillations for length of approximately 50-70 cm', step=0.1)
t2[3] = st.number_input(label='Second reading of time taken for 20 oscillations for length of approximately 50-70 cm', step=0.1)

length[4] = st.number_input('Measure the length of the pendulum in centimetres.',
                     value=50.0, step=0.1)
t1[4] = st.number_input(label='First reading of time taken for 20 oscillations for length of approximately 40-60 cm', step=0.1)
t2[4] = st.number_input(label='Second reading of time taken for 20 oscillations for length of approximately 40-60 cm', step=0.1)

length[5] = st.number_input('Measure the length of the pendulum in centimetres.',
                     value=40.0, step=0.1)
t1[5] = st.number_input(label='First reading of time taken for 20 oscillations for length of approximately 30-50 cm', step=0.1)
t2[5] = st.number_input(label='Second reading of time taken for 20 oscillations for length of approximately 30-50 cm', step=0.1)


st.write("Check that the time readings for 20 oscillations correspond to the respective lengths. Otherwise, you may correct and re-enter them above.")
df = pd.DataFrame({'length/cm': length, 't1/s': t1, 't2/s': t2})
st.write(df)


st.header('Part II: Data Analysis')
st.write('In Part II of the experiment, you will be processing the collected data and inferring the relationship between the period and length of the pendulum.')
st.write('There will be some questions below. Return your answers to these questions and those in Part III, alongside screen captures of the completed page to your teacher.')

st.subheader('Procedure')
st.markdown("5. Calculate the average time for 20 oscillations, usng the formula $<t>=(t_1+t_2)/2$. (Why do we have to take two readings and find their average?) Hence, calculate the period of the pendulum $T = <t>/20$ and $T^2$. (Why couldn't we have just timed one oscillation?)")
t = (t1+t2) / 2
T = t / 20
T2 = T ** 2
df2 = df
df2['<t>/s'] = t
df2['Period/s'] = T
df2['T^2/s^2'] = T2

if st.button('Calculate'):
    st.write(df2)

st.markdown("6. Plot the graph of $T^2/\mathrm{s}^2$ against $l/$cm.")
fig, ax = plt.subplots()
plt.plot(length, T2, 'x', markersize=3)
plt.xlim(0,120)
plt.ylim(0,4.5)
plt.grid(b=True)
plt.xlabel('Length of Pendulum/ cm')
plt.ylabel('Period^2/ s^2')

if st.button('Plot'):
    st.pyplot(fig)
    
st.markdown('7. By drawing an appropriate line, deduce the relationship between the period $T$ and length $l$ of the pendulum.')
if st.button('Draw'):
    m = st.slider('Gradient', min_value=0.00, max_value=0.10, value=0.04, step=0.001)            
    c = st.slider('Intercept (vertical)', min_value=-0.10, max_value=0.10, value=0.0, step=0.01)
    plt.plot(length, m*length+c)
    plt.xlim(0,120)
    plt.ylim(0,4.5)     
    st.pyplot(fig)
    
    
st.header('Part III: Questions')
st.write('In Part III, you wil be using the inferred relationship between the dependent and independent variable to make some predictions.')

st.markdown('1. From the graph, estimate the length of the pendulum that will yield a period of 2.0 s')
st.markdown('2. The formula for the period of a pendulum is $2\pi\sqrt{l/g}$, where $l$ is the length of the pendulum. Derive the value of $g$, including its units and comment on its physical significiance.')

    
