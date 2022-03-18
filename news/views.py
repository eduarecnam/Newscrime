from django.http.response import ResponseHeaders
from django.shortcuts import render
from datetime import date, datetime
import re
from django import forms
import requests
import json
import time

from requests.models import to_native_string

# <!-- <li><a href="{% url 'polls:detail' question.id %}">{{ question.question_text }}</a></li> -->

"""
Function that returns a list with all of the forces name
"""
def get_forces():
    url_forces = 'https://data.police.uk/api/forces'
    response_forces = requests.get(url_forces)
    forces = []
    for force in response_forces.json():    
        forces.append(force['id'])
    return forces

"""
Function that returns a list with all of the crime categories current year
"""
def get_crime_categories_current_year():
    url_crime_categories = 'https://data.police.uk/api/crime-categories?date={}'.format(datetime.now().year)
    response_crime_categories = requests.get(url_crime_categories)
    crime_categories = []
    for category in response_crime_categories.json():
        crime_categories.append(category['url'])
    return crime_categories

"""
Function that returns the first month (current year) which there were crimes
"""
def get_first_month_with_crimes(month, year, url_crimes, forces):
    
    total_crimes = 0
    query_month = '00'
    for force in forces:    
        query_month = str(month)
        if len(query_month) < 2:
            query_month = '0'+query_month
        while query_month != '00': 
            response_crimes = requests.get(url_crimes.format(force, year, query_month))
            if response_crimes.status_code == 200 and len(response_crimes.json()) > 0:
                return query_month
        month -= 1
    return query_month



def index(request):
    context = {}
    return render(request, 'news/index.html', context)


def forces(request):
    url_forces = 'https://data.police.uk/api/forces'
    response_forces = requests.get(url_forces)
    forces = {}
    if response_forces.status_code == 200:        
        for force in response_forces.json():    
            forces[force['id']]  = force['name']
        return render(request, 'news/forces.html', context = {'forces': json.dumps(forces)})
    else:
        return render(request, 'news/forces.html', context = {'forces':'Error, there was a problem, please try again later'})

def details_force(request, force):
    url_force = 'https://data.police.uk/api/forces/{}'
    response_force = requests.get(url_force.format(force))
    aux_response = response_force.json()
    # print(aux_response['description'])
    if aux_response['description'] != None:
        clean = re.compile('<.*?>')
        aux_response['description'] = re.sub(clean, '', aux_response['description'])
    return render(request, 'news/details_force.html', context = {'force':aux_response})

def seniors(request):
    url_seniors = 'https://data.police.uk/api/forces/{}/people'
    seniors_per_force = {}
    forces = get_forces()
    for force in forces:
        response_seniors = requests.get(url_seniors.format(force))
        seniors_per_force[force] = len(response_seniors.json())
    return render(request, 'news/seniors.html', context = {'seniors': json.dumps(seniors_per_force)})

def crimes(request):
    url_crimes = 'https://data.police.uk/api/crimes-no-location?category=all-crime&force={}&date={}-{}'
    url_last_update = 'https://data.police.uk/api/crime-last-updated'
    categories_current_year = get_crime_categories_current_year()
    categories_current_year.pop(0) #all-crime is removed it
    forces = get_forces()
    
    year = datetime.now().year
    month = requests.get(url_last_update)
    format = "%Y-%m-%d"
    month = datetime.strptime(month.json()['date'], format).month
    total_crimes_category = {}
    for category in categories_current_year:
        total_crimes_category[category] = 0

    if len(str(month)) < 2:
        month = '0'+str(month)
    for force in forces:
        response_crimes = requests.get(url_crimes.format(force, year, month))
        if response_crimes.status_code == 200 and len(response_crimes.json()) > 0:
            crimes = response_crimes.json()
            for crime in crimes:
                total_crimes_category[crime['category']] += 1
    
    return render(request, 'news/crimes.html', context = {
        'total_crimes_category': json.dumps(total_crimes_category), 
        'month': str(year)+'-'+month
        })