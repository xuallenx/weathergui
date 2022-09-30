from tkinter import *
from tkinter import messagebox
from configparser import ConfigParser
import requests


url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid={}'

config_file = 'config.ini'
config = ConfigParser()
config.read(config_file)
api_key = config['api_key']['key']


def get_weather(city):
    result = requests.get(url.format(city, api_key))
    if result:
        json = result.json()
        # want weather function to return tuple of (City, Country, Celsius, Fahrenheit, Icon, Weather)
        city = json['name']
        country = json['sys']['country']
        kelvin = json['main']['temp']
        celsius = kelvin - 273.15
        fahrenheit = (kelvin - 273.15) * 9 / 5 + 32
        icon = json['weather'][0]['icon']
        weather = json['weather'][0]['main']
        description = json['weather'][0]['description']
        final = (city, country, celsius, fahrenheit, icon, weather, description)
        return final

    else:
        return None


def search():
   city = city_text.get()
   weather = get_weather(city)
   if weather:
       location_label['text'] = '{}, {}'.format(weather[0], weather[1])
       # weather[4] accesses the icon key in json
       # however macbook downloads the icons with extra '@2x' at the end
       temp = weather[4]+'@2x'
       image['bitmap'] = 'weather_icons/{}.png'.format(temp)
       temp_label['text'] = '{:.2f}°C, {:.2f}°F'.format(weather[2], weather[3]) #  :.2f limits string to 2 decimals
       weather_label['text'] = weather[5]
       description_label['text'] = weather[6]


   else:
       messagebox.showerror('Error', 'Cannot find city {}'.format(city))



app = Tk()
app.title("Weather Forecasing")
app.geometry('700x350')

city_text = StringVar()
city_entry = Entry(app, textvariable=city_text)
city_entry.pack()

search_btn = Button(app, text="Search Location", width=12, command=search)
search_btn.pack()

location_label = Label(app, text="Location", font=('bold', 20))
location_label.pack()

image = Label(app, bitmap='') #no image now
image.pack()

temp_label = Label(app, text='temperature')
temp_label.pack()

weather_label = Label(app, text='weather')
weather_label.pack()

description_label = Label(app, text='Description')
description_label.pack()





app.mainloop()