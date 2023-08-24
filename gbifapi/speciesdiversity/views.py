from django.shortcuts import render
import requests
from collections import Counter
import math
import matplotlib.pyplot as plt
import os

def speciesdiversity(request):
    countries = get_country_list()
    return render(request, 'speciesdiversity/country_selection.html', {'countries': countries})


def get_country_list():
    url = "https://api.gbif.org/v1/enumeration/country"
    response = requests.get(url)
    if response.status_code == 200:
        raw_countries = response.json()
        countries = [{'title': country['title'], 'iso2': country['iso2']} for country in raw_countries]
        return countries
    else:
        return []


def index(request):
    countries = get_country_list()
    selected_country = request.GET.get('country')  # Obtener el valor de country desde la URL
    if selected_country:
        species_data, total_records = get_species_data(selected_country)
        if species_data:
            species_abundances = Counter(species_data)
            diversity_index, richness_index = calculate_diversity_indexes(species_abundances)
            context = {
                'countries': countries,
                'species_abundances': species_abundances,
                'total_records': total_records,
                'diversity_index': diversity_index,
                'richness_index': richness_index,
                'selected_country': selected_country  # Pasar el valor de country a la plantilla
            }
            bar_chart_view(request, species_abundances)
            return render(request, 'speciesdiversity/main_page.html', context)

    return render(request, 'speciesdiversity/main_page.html', {'countries': countries})


def get_species_data(country_code):
    url = f"https://api.gbif.org/v1/occurrence/search?country={country_code}&limit=5000"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        species_list = [record.get('species') for record in data.get('results', []) if 'species' in record]
        total_records = len(species_list)
        return species_list, total_records
    else:
        return [], 0


def calculate_diversity_indexes(species_abundances): # Función para calcular índices de diversidad
    total_records = sum(species_abundances.values())
    shannon_index = 0
    simpson_index = 0

    for species_abundance in species_abundances.values(): # Calculamos el índice de Shannon
        pi = species_abundance / total_records # Primero sacando la proporción total de abundancia de N
        shannon_index += pi * math.log(pi) # Luego, por cada especie se multiplica la proporción por el ln

    shannon_index = -shannon_index # Guardamos el resultado y lo convertimos para legibilizar

    for species_abundance in species_abundances.values():
        pi = species_abundance / total_records
        simpson_index += pi ** 2

    simpson_index = 1 / simpson_index
    return shannon_index, simpson_index


def species_data_view(request):
    selected_country = request.GET.get('country')
    countries = get_country_list()
    diversity_index = 0
    richness_index = 0
    species_abundances = {}  # Diccionario para almacenar las abundancias de especies
    total_records = 0

    if selected_country:
        species_data, total_records = get_species_data(selected_country)
        if species_data:
            species_abundances = dict(Counter(species_data))  # Obtener el Counter como diccionario
            print("Species Abundances:", species_abundances)
            diversity_index, richness_index = calculate_diversity_indexes(species_abundances)

    # print("Antes de pasar el contexto:", type(species_abundances)) Debug para encontrar tipo de datos
    context = {
        'countries': countries,
        'species_abundances': species_abundances,
        'total_records': total_records,
        'diversity_index': diversity_index,
        'richness_index': richness_index,
        'selected_country': selected_country
    }
    # print("Después de pasar el contexto:", type(context['species_abundances']))

    bar_chart_view(request, species_abundances)
    return render(request, 'speciesdiversity/main_page.html', context)


def bar_chart_view(request, species_abundances):
    species_names = list(species_abundances.keys())
    abundances = list(species_abundances.values())

    plt.figure(figsize=(20, 12))
    plt.bar(species_names, abundances)
    plt.xlabel('Especies')
    plt.ylabel('Abundancia')
    plt.title('Gráfica de Abundancia de Especies')
    plt.xticks(ticks=[], labels=[])

    # Obtener la ruta completa para guardar la imagen en la carpeta static
    image_filename = 'grafica.png'
    image_path = os.path.join('speciesdiversity/static/speciesdiversity', image_filename)

    # Guardar la imagen en la ruta
    plt.savefig(image_path, format='png')
    plt.close()




