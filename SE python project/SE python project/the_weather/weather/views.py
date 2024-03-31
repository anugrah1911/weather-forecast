from django.shortcuts import render
import requests
from .models import City
from .forms import CityForm

def index(request):
    cities = City.objects.all() # Return all the cities in the database

    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=271d1234d3f497eed5b1d80a07b3fcd1'

    if request.method == 'POST': # Only true if form is submitted
        form = CityForm(request.POST) # Add actual request data to form for processing
        if form.is_valid(): # Validate the form data
            form.save() # Save the valid form data to the database

    form = CityForm()

    weather_data = []

    for city in cities:
        try:
            city_weather = requests.get(url.format(city.name)).json() # Request the API data and convert the JSON to Python data types
            
            weather = {
                'city' : city.name,
                'temperature' : city_weather['main']['temp'],
                'description' : city_weather['weather'][0]['description'],
                'icon' : city_weather['weather'][0]['icon']
            }

            weather_data.append(weather) # Add the data for the current city into our list
        except Exception as e:
            print(f"Error fetching weather data for {city.name}: {e}")
            # You can choose to handle the error here, for example, by skipping this city and continuing with the loop

    context = {'weather_data' : weather_data, 'form' : form}

    return render(request, 'weather/index.html', context) # Returns the index.html template
