from django.shortcuts import render
import requests
from django.http import JsonResponse


OMDB_API_KEY = '7f81358e'

def fetch_movie_data(request, movie_title):
    url = f"http://www.omdbapi.com/?t={movie_title}&apikey={OMDB_API_KEY}"
    response = requests.get(url)

    if response.status_code == 200:
        return JsonResponse(response.json(), safe=False)
    else:
        return JsonResponse({'error': 'Error fetching data from OMDb'}, status=500)

