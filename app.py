import streamlit as st
import requests
from datetime import datetime, timedelta
import pandas as pd
from streamlit_lottie import st_lottie
import toml

with open("secrets.toml", 'r') as f:
    secrets = toml.load(f)

api_key = secrets["openweathermap"]["api_key"]

st.set_page_config(layout="wide")

url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid={}'
# url_2 = 'https://api.openweathermap.org/data/2.5/onecall/timemachine'
# url_3 = 'https://api.openweathermap.org/geo/1.0/direct'

gif_file = open("C:/Users/annar/Downloads/Untitled design.gif", "rb").read()



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
        st.write('An application that fetches current weather data from openweathermap.org API and gives the user the current temperature, the feels like temperaure and humidity of the user input city!')
    with col_2:
        st.image(gif_file)


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
            