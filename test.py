import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pandas_datareader as data
from pandas_datareader import data as pdr
import yfinance as yf
from keras.models import load_model
import streamlit as st

yf.pdr_override()

st.title('PSTP: Pepperoni Stock Trend Predictor')
st.caption("To restart - press :violet[R]")
st.divider()
user_input_symbol = st.text_input('Enter stock symbol:')
user_input_start_date = st.text_input('Enter starting date in a format "yyyy-mm-dd": ')
user_input_end_date = st.text_input('Enter end date in a format "yyyy-mm-dd": ')
st.divider()

df = pdr.get_data_yahoo(user_input_symbol, user_input_start_date, user_input_end_date)

#Describing data
st.subheader('Data from ' + user_input_start_date + " to " + user_input_end_date)
st.write(df.describe())

#Visualizations

#Plotting a simple closing price chart
st.subheader('Closing Price in Dollars vs Time chart')
fig = plt.figure(figsize = (12, 6), dpi = 100)
plt.plot(df.Close, 'b')
st.pyplot(fig)

#100 Moving Average
st.subheader('Closing Price vs Time chart with 100MA')
ma100 = df.Close.rolling(100).mean()
fig = plt.figure(figsize = (12,6))
plt.plot(ma100, 'r')
plt.plot(df.Close, 'b')
st.pyplot(fig)

#200 Moving Average
st.subheader('Closing Price vs Time chart with 100MA & 200MA')
ma100 = df.Close.rolling(100).mean()
ma200 = df.Close.rolling(200).mean()
fig = plt.figure(figsize = (12,6))
plt.plot(ma100, 'r')
plt.plot(ma200, 'g')
plt.plot(df.Close, 'b')
st.pyplot(fig)

#Splitting data into training and testing
data_training = pd.DataFrame(df['Close'][0:int(len(df)*0.7)])
data_testing = pd.DataFrame(df['Close'][int(len(df)*0.7):int(len(df))])

#scaling
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler(feature_range=(0,1))

data_training_array = scaler.fit_transform(data_training)

#loading the model
model = load_model('Stock_Predictor_Model.h5')

#testing
past_100_days = data_training.tail(100)
final_df = pd.concat([past_100_days, data_testing], ignore_index=True)
input_data = scaler.fit_transform(final_df)

x_test = []
y_test = []

for i in range(100, input_data.shape[0]):
  x_test.append(input_data[i-100:i])
  y_test.append(input_data[i, 0])

x_test, y_test = np.array(x_test), np.array(y_test)

#predictions
y_predicted = model.predict(x_test)

data_scaler = scaler.scale_

scale_factor = 1/data_scaler[0]
y_predicted = y_predicted * scale_factor
y_test = y_test * scale_factor

#final graph
st.subheader('Predictions vs original')
fig2 = plt.figure(figsize=(12,6))
plt.plot(y_test, 'b', label = 'Original Price')
plt.plot(y_predicted, 'r', label = 'Predicted Price')
plt.xlabel('Time')
plt.ylabel('Price')
plt.legend()
st.pyplot(fig2)