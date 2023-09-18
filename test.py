import matplotlib.pyplot as plt
import yfinance as yf
from keras.models import load_model
import streamlit as st

st.title('PSTP: Pepperoni Stock Trend Predictor')
st.caption("To restart - press :violet[R]")
st.divider()
user_input_symbol = st.text_input('Enter stock symbol:')
user_input_start_date = st.text_input('Enter starting date in a format "yyyy-mm-dd": ')
user_input_end_date = st.text_input('Enter end date in a format "yyyy-mm-dd": ')
st.divider()

df = yf.download(user_input_symbol, start=user_input_start_date, end=user_input_end_date)

#Visualizations

#Plotting a simple closing price chart
st.subheader('Closing Price in Dollars vs Time chart')
fig = plt.figure(figsize = (12, 6), dpi = 100)
plt.plot(df['Close'], 'b')
st.pyplot(fig)

#100 Moving Average
st.subheader('Closing Price vs Time chart with 100MA')
ma100 = df['Close'].rolling(100).mean()
fig = plt.figure(figsize = (12,6))
plt.plot(ma100, 'r')
plt.plot(df['Close'], 'b')
st.pyplot(fig)

#200 Moving Average
st.subheader('Closing Price vs Time chart with 100MA & 200MA')
ma100 = df['Close'].rolling(100).mean()
ma200 = df['Close'].rolling(200).mean()
fig = plt.figure(figsize = (12,6))
plt.plot(ma100, 'r')
plt.plot(ma200, 'g')
plt.plot(df['Close'], 'b')
st.pyplot(fig)

#Splitting data into training and testing
data_training = df['Close'][:int(len(df) * 0.7)]
data_testing = df['Close'][int(len(df) * 0.7):]

#scaling function
def custom_min_max_scaler(data):
  min_val = min(data)
  max_val = max(data)
  scaled_data = [(x - min_val) / (max_val - min_val) for x in data]
  return scaled_data

data_training_array = custom_min_max_scaler(data_training.tolist())

#loading the model
model = load_model('Stock_Predictor_Model.h5')

#testing

#using python lists for data manipulation
past_100_days = data_training.tail(100)
final_df = past_100_days.tolist() + data_testing.tolist()
input_data = custom_min_max_scaler(final_df)

x_test = []
y_test = []

for i in range(100, len(input_data)):
    x_test.append(input_data[i - 100:i])
    y_test.append(input_data[i])

# Predictions
y_predicted = model.predict(x_test)

# Scaling back to original values
min_val = min(data_training)
max_val = max(data_training)
scale_factor = max_val - min_val

y_predicted = [y * scale_factor + min_val for y in y_predicted]
y_test = [y * scale_factor + min_val for y in y_test]

# Final graph
st.subheader('Predictions vs original')
fig2 = plt.figure(figsize=(12,6))
plt.plot(y_test, 'b', label = 'Original Price')
plt.plot(y_predicted, 'r', label = 'Predicted Price')
plt.xlabel('Time')
plt.ylabel('Price')
plt.legend()
st.pyplot(fig2)
