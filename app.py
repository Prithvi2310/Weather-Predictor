import streamlit as st
import requests
from datetime import datetime, timedelta
import pandas as pd
from streamlit_lottie import st_lottie

api_key = 'f101202d0d81e93cb1245ad877f53f4a'
url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid={}'
url_2 = 'http://api.openweathermap.org/data/3.0/history/timemachine?lat={}&lon={}&dt={}&appid={}'

def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code !=200:
        return None
    return r.json()


def getweather(city):
    result = requests.get(url.format(city, api_key))

    if result:
        json = result.json()
        country = json['sys']['country']
        temp = json['main']['temp'] - 273
        temp_feels = json['main']['feels_like'] - 273
        humid = json['main']['humidity'] 
        icon = json['weather'][0]['icon']
        lon = json['coord']['lon']
        lat = json['coord']['lat']
        des = json['weather'][0]['description']
        res = [country, round(temp,1), round(temp_feels,1), humid, lon, lat, icon, des]

        return res, json
    
    else:
        print("Error in Search!")


def get_hist_data(lat, lon, start):
    res = requests.get(url_2.format(lat,lon,start,api_key))
    data = res.json()
    temp = []
    for hour in data["hourly"]:
        t = hour["temp"]
        temp.append(t)
    return data, temp

#web app

with st.container():
    col_1,col_2 = st.columns(2)
    with col_1:
        st.title("Weather Predictor Application")
        st.write('An application that fetches current weather data from an API and analyses the historical data (of past 5 days)')
    with col_2:
        lottie_weather = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_cHA3rG.json")
        st_lottie(lottie_weather, height = 250, key = "weather")

with st.container():
    col1, col2 = st.columns(2)
    with col1:
        city_name = st.text_input("Please enter your city name")
        if city_name:
            r, json = getweather(city_name)
            st.subheader('Status: ' + str(r[7]))
            web_str = "![Alt Text]" + "(http://openweathermap.org/img/wn/" + str(r[6])+"@2x.png)"
            st.markdown(web_str)


    with col2:
        if city_name:
            r, json = getweather(city_name)
            st.success('Current: ' + str(round(r[1],2)) + ' °C')
            st.info('Feels Like: ' + str(round(r[2],2)) + ' °C')
            st.info('Humidity: ' + str(round(r[3],2)) + ' %')

with st.container():
    #Number_of_Days = st.number_input("Enter the number of days you want the data of")
    if city_name:
        r, json = getweather(city_name)
        #show_hist = st.expander(label = f'Last {Number_of_Days} Days History')
        show_hist = st.expander(label = 'Last 5 Days History')
        with show_hist:
            start_date_string = st.date_input('Current Date')
            date_df = []
            max_temp_df =[]
            for i in range (5):
                date_str = start_date_string - timedelta(i)
                start_date = datetime.strptime(str(date_str), "%Y-%m-%d")
                timestamp_1 = datetime.timestamp(start_date)
                data, temp = get_hist_data(r[5], r[4], int(timestamp_1))
                date_df.append(date_str)
                max_temp_df.append(max(temp) - 273)

            df = pd.DataFrame()
            df['Date'] = date_df
            df['Max_temp'] = max_temp_df  
            st.table(df)          
                
