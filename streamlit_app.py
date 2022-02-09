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

st.subheader('Experiment Set-up')
image2 = Image.open('./media/exptsetup_side.jpg')
st.image(image2, caption='Figure 2: Experimental Set-up',)

length, t1, t2, tave, T, T2 = np.zeros(8, dtype=np.float16), np.zeros(8, dtype=np.float16), np.zeros(8, dtype=np.float16), np.zeros(8, dtype=np.float16), np.zeros(8, dtype=np.float16), np.zeros(8, dtype=np.float16)

st.subheader('Procedure')
st.markdown("1. Set-up the experiment as in Figure 2 above, with the thread held tightly by the split cork.")
image3a = Image.open('./media/splitcork_unfixed.jpg')
image3b = Image.open('./media/splitcork_knot.jpg')
image3c = Image.open('./media/splitcork_fixed.jpg')
image3d = Image.open('./media/exptsetup_top.jpg')
st.image([image3a, image3b, image3c, image3d], width=244)

st.markdown("2. Adjust the thread such that the length of the pendulum $𝑙$ is approximately one metre.")
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

st.write("Check that the time readings for 20 oscillations correspond to the respective lengths. Otherwise, you may correct and re-enter them above. Measurements yet to be made are initialised as 0. The right three columns will be discussed in the next part.")
df = pd.DataFrame({'length/cm': length, 't1/s': t1, 't2/s': t2, '<t>/s': tave, 'Period/s': T, 'T^2/s^2': T2})

st.write(df)

@st.cache
def convert_df(df):
     # IMPORTANT: Cache the conversion to prevent computation on every rerun
     return df.to_csv().encode('utf-8')

csv_raw = convert_df(df)
st.download_button(
     label="Download the tabulated data as CSV",
     data=csv_raw,
     file_name='data_raw.csv',
     mime='text/csv',
 )

st.markdown('6. Repeat steps 3-5 with seven more values of $l$ varying from 100.0 cm to 30.0 cm. Record these values directly in the CSV file and save it for Part II. If you are not able to collect data in the laboratory, you may use the following CSV file.')

with open('./data_processed.csv') as f:
     st.download_button(
         label="Download artificial data as CSV",
         data=f,
         file_name='artificial_data.csv',
         mime='text/csv',
     )

st.header('Part II: Data Analysis')
st.write('In Part II of the experiment, you will be processing the collected data and inferring the relationship between the period and length of the pendulum.')
st.write('There will be some questions below. Return your answers to these questions and those in Part III, alongside screen captures of the completed page to your teacher.')

st.subheader('Procedure')

st.markdown("7. By using an Excel Spreadsheet or otherwise, calculate the average time for the two time readings and record it in the corresponding entry in the CSV file.")
if st.button('Hint'):
         st.markdown("The average of two time readings can be calculated with the formula $<t>=(t_1+t_2)/2$. Why do we have to take two readings and find their average?")

st.markdown("8. Calculate the period of the pendulum squared and record it in the corresponding entry in the CSV file.")
if st.button('Hint 2'):
         st.markdown("The period and period squared may be calculated from the average time taken for 20 oscillations with the formulae $T = <t>/20$ and $T^2$. Why couldn't we have just timed one oscillation?")

data_com = st.file_uploader("Upload the csv file with the inputted raw data and the derived quantities you computed.")
N = 8 # for computing root-mean-squared error

if data_com is not None:
  df = pd.read_csv(data_com)
  st.write(df)
  T2 = df['T^2/s^2']
  length = df['length/cm']
  N = np.count_nonzero(T2)

T2 = df['T^2/s^2']
length = df['length/cm']
         
st.markdown("9. Plot the graph of $T^2/\mathrm{s}^2$ against $l/$cm.")
fig, ax = plt.subplots()
plt.plot(length, T2, 'x', markersize=3)
plt.title('Scatterplot of Period squared against length of the pendulum')
plt.xlim(0,120)
plt.ylim(0,4.5)
plt.grid(b=True)
plt.xlabel('Length of Pendulum/ cm')
plt.ylabel('Period^2/ s^2')

if st.button('Plot'):
    st.pyplot(fig)
    
st.markdown('10. By manipulating the line to minimise the error value, deduce the relationship between the period $T$ and length $l$ of the pendulum. The root-mean-square error (RMSE) is similar to the standard deviation of a dataset except that it calculates the sum of squared distances from the hypothesised interpolated period squared $\hat{T^2}$ instead of the mean $<T^2>$.')
st.latex(r'''RMSE = \sqrt{\frac{1}{N_{readings}}\sum_{N=1}^{N_{readings}} \left(\hat{T^2}-T^2 \right)^2}''')
m = st.slider('Gradient', min_value=0.00, max_value=0.10, value=0.04, step=0.0001)
c = st.slider('Intercept (vertical)', min_value=-0.20, max_value=0.20, value=0.0, step=0.01)
# root-mean-square deviation error
residuals = T2-(m*length+c)
sum_squared_error = np.sum(residuals**2)
rms_error= np.sqrt(sum_squared_error/N)
st.write('Root-mean-squared error: ')
st.write(rms_error)

plt.plot(length, m*length+c)
plt.title('Linear fit of Period squared against length of the pendulum')
plt.xlim(0,120)
plt.ylim(0,4.5)     
st.pyplot(fig)
    
    
st.header('Part III: Questions')
st.write('In Part III, you will be using the parameters of the fitted best-fit line between the dependent and independent variables to estimate unknown physical quantities.')

st.markdown('1. From the fitted graph, estimate the length of the pendulum that will yield a period of 2.0 s')
st.markdown('2. The formula for the period of a pendulum is $2\pi\sqrt{l/g}$, where $l$ is the length of the pendulum, and $g$ an unknown constant. Derive the value of the physical constant $g$, including its units and comment on its physical significiance.')

    
