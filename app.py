import streamlit as st
import requests
from datetime import datetime, timedelta
import pandas as pd


api_key = 'f101202d0d81e93cb1245ad877f53f4a'

st.set_page_config(layout="wide")

url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid={}'

gif_file = open("design.gif", "rb").read()



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



    
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)


#web app

st.write("##")

with st.container():
    col_1,col_2 = st.columns(2)
    with col_1:
        st.title("Weather Predictor Application")
        st.markdown("<h7 style='text-align: left; color: white;'>🔵 An application that fetches current weather data from openweathermap.org API</h1>", unsafe_allow_html=True)
        st.markdown("<h7 style='text-align: left; color: white;'>🟢 Gives the user the current temperature, the feels like temperaure and humidity of the user input city!", unsafe_allow_html=True)
        st.markdown("<h7 style='text-align: left; color: white;'>🟣 On further analysis, this application can help us forecast the future weather data</h1>", unsafe_allow_html=True)
    
        st.subheader("General Instructions " )
        st.write("1. User must input a valid city name, i.e, there shouldn't be any spelling mistakes")
        st.write("2. The city name is not case sensetive")
        st.write("3. The accuracy of the information predicted in not 100%")

        st. write('##')

        st.markdown("<h10 style='text-align: left; color: red;'>NOTE: Since there are APIs that come under FOSS the future forecasting can be done through the integration of Machine Learning model</h1>", unsafe_allow_html=True)

    with col_2:
        st.image(gif_file)

st.write('##')
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
        
    st.write("---")
    st.header("Get in Touch With US")

    with st.form(key="contact_form"):
        # Add input fields for the user's name, email address, and message
        name = st.text_input("Name")
        email = st.text_input("Email")
        message = st.text_area("Message")

        # Add a submit button to the form
        submit_button = st.form_submit_button(label="Submit")

        if submit_button:
            st.write("Your Response has been recorded. We will get back to you shortly")
