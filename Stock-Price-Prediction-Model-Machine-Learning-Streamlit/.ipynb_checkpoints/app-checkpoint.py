import yfinance as yf
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np 
import pandas as pd 
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense,LSTM
from tensorflow.keras.models import load_model
import streamlit as st

st.title("Stock Price Predictor App")

stock = st.text_input("Enter the stock ID","GOOG")

end = datetime.now()
start = datetime(end.year-20,end.month,end.day)
input_data = yf.download(stock,start,end)

model = load_model("Latest-Stock-Prediction-Model.keras")
st.subheader("Stock Data")
st.write(input_data)

splitting_len = int(len(input_data)*0.7)

xtest = pd.DataFrame(input_data.Close[splitting_len:])


def plot_graph(values,data,extra_data = 0,extra_dataset= None):
    fig = plt.figure(figsize=(15,6))
    plt.plot(values,'Orange')
    plt.plot(data.Close,'b')
    plt.legend()
    if extra_data:
            plt.plot(extra_data)
    return fig
    
st.subheader("Original Close Price And Moving Average for 250 days")
input_data["Moving_Average_for_250_days"] = input_data.Close.rolling(250).mean()
st.pyplot(plot_graph(input_data["Moving_Average_for_250_days"],input_data,0))

st.subheader("Original Close Price And Moving Average for 200 days")
input_data["Moving_Average_for_200_days"] = input_data.Close.rolling(200).mean()
st.pyplot(plot_graph(input_data["Moving_Average_for_200_days"],input_data,0))

st.subheader("Original Close Price And Moving Average for 100 days")
input_data["Moving_Average_for_100_days"] = input_data.Close.rolling(100).mean()
st.pyplot(plot_graph(input_data["Moving_Average_for_100_days"],input_data,0))

scaler = MinMaxScaler(feature_range=(0,1))
scaled_data = scaler.fit_transform(xtest)

x_data = []
y_data = []

for i in range(100,len(scaled_data)):
    x_data.append(scaled_data[i-100:i])
    y_data.append(scaled_data[i])

x_data, y_data = np.array(x_data), np.array(y_data)

predictions = model.predict(x_data)

inv_pre = scaler.inverse_transform(predictions)
inv_y_test = scaler.inverse_transform(y_data)

ploting_data = pd.DataFrame(
 {
  'original_test_data': inv_y_test.reshape(-1),
    'predictions': inv_pre.reshape(-1)
 } ,
    index = input_data.index[splitting_len+100:]
)
st.subheader("Original values vs Predicted values")
st.write(ploting_data)

st.subheader('Original Close Price vs Predicted Close price')
fig = plt.figure(figsize=(15,6))
plt.plot(pd.concat([input_data.Close[:splitting_len+100],ploting_data], axis=0))
plt.legend(["Data- not used", "Original Test data", "Predicted Test data"])
st.pyplot(fig)











