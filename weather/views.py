from django.shortcuts import render, redirect
import requests
from .models import City
from .forms import CityForm

# Create your views here.
def index(request):
    # Register with Open weather map and recieve api id and input into url below
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=###INSERT API ID HERE###'

    error_message = ''
    message = ''
    message_class = ''

    if request.method == 'POST':
        form = CityForm(request.POST)

        if form.is_valid():
            new_city = form.cleaned_data['name']
            excisting_cities = City.objects.filter(name=new_city).count()
            if excisting_cities == 0:
                response = requests.get(url.format(new_city)).json()
                if response['cod'] == 200:
                    form.save()
                else:
                    error_message = 'City does not exist'
            else:
                error_message = 'Already have city'

        if error_message:
            message =error_message
            message_class = 'is-danger'
        else:
            message = 'City added'
            message_class = 'is-success'
    form = CityForm()

    cities = City.objects.all()
    weather_data = []

    for city in cities:
        response = requests.get(url.format(city)).json()

        city_weather = {
            'city': city.name,
            'temperature': response['main']['temp'],
            'description': response['weather'][0]['description'],
            'icon': response['weather'][0]['icon']
        }
        weather_data.append(city_weather)

    context = {'weather_data': weather_data,
               'form': form,
               'message': message,
               'message_class': message_class}
    return render(request, 'weather/weather.html', context)

def delete_city(request, city_name):
    City.objects.get(name=city_name).delete()
    return redirect('home')
