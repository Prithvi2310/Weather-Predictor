import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

# load the historical weather data
data = pd.read_csv('historical_weather_data.csv')

# convert the date column to a datetime object
data['date'] = pd.to_datetime(data['date'])

# create a new column for the day of the year (1-365)
data['day_of_year'] = data['date'].dt.dayofyear

# create a new column for the year
data['year'] = data['date'].dt.year

# split the data into training and testing sets
train, test = train_test_split(data, test_size=0.2, random_state=42)

# extract the features and target variables
train_X = train[['day_of_year', 'year']]
train_y = train['temperature']

test_X = test[['day_of_year', 'year']]
test_y = test['temperature']

from keras.models import Sequential
from keras.layers import Dense, LSTM

# create the model
model = Sequential()

# add the LSTM layer
model.add(LSTM(50, input_shape=(2, 1)))

# add the output layer
model.add(Dense(1))

# compile the model
model.compile(loss='mean_squared_error', optimizer='adam')

# reshape the input data to match the expected input shape of the LSTM
train_X = train_X.values.reshape((train_X.shape[0], 2, 1))
test_X = test_X.values.reshape((test_X.shape[0], 2, 1))

# train the model
model.fit(train_X, train_y, epochs=50, batch_size=72, validation_data=(test_X, test_y), verbose=2)

# create a new dataframe for the future dates
future_dates = pd.date_range(start='2023-03-06', end='2023-03-31')
future_data = pd.DataFrame({'date': future_dates})

# create the day of year and year columns for the future dates
future_data['day_of_year'] = future_data['date'].dt.dayofyear
future_data['year'] = future_data['date'].dt.year

# make predictions using the model
future_X = future_data[['day_of_year', 'year']]
future_X = future_X.values.reshape((future_X.shape[0], 2, 1))
future_y = model.predict(future_X)

# add the predicted temperatures to the dataframe
future_data['temperature'] = future_y

# print the predicted temperatures
print(future_data['temperature'])
