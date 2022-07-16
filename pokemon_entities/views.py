import folium
import json
import requests
import datetime


from django.http import HttpResponseNotFound
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from .models import PokemonEntity, Pokemon


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic models.IntegerFieldencoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    pokemons_entities = PokemonEntity.objects.filter(
        disappeared_at__gt=datetime.datetime.now(),
        appeared_at__lt=datetime.datetime.now()
    )

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in pokemons_entities:
        add_pokemon(
            folium_map, pokemon_entity.lat,
            pokemon_entity.lon,
            request.build_absolute_uri(f"media/{pokemon_entity.pokemon.image}")
        )

    pokemons_on_page = []
    pokemons = Pokemon.objects.all()
    for pokemon in pokemons:
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': request.build_absolute_uri(f"media/{pokemon.image}"),
            'title_ru': pokemon.name
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    try:
        pokemon = Pokemon.objects.get(id=pokemon_id)
    except ObjectDoesNotExist:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in pokemon.entitys.all():
        add_pokemon(
            folium_map, pokemon_entity.lat,
            pokemon_entity.lon,
            request.build_absolute_uri(pokemon.image.url)
        )

    pokemon_params = {
        "pokemon_id": pokemon.id,
        "title_ru": pokemon.name,
        "title_en": pokemon.name_en,
        "title_jp": pokemon.name_jp,
        "description": pokemon.description,
        "img_url": request.build_absolute_uri(pokemon.image.url)
    }

    if pokemon.prev_evolution:
        pokemon_params["previous_evolution"] = {
            "title_ru": pokemon.prev_evolution.name,
            "pokemon_id": pokemon.prev_evolution.id,
            "img_url": request.build_absolute_uri(
                pokemon.prev_evolution.image.url
            )
        }
    if pokemon.next_evolutions.count():
        pokemon_next_evolution = pokemon.next_evolutions.all()[0]
        pokemon_params["next_evolution"] = {
            "title_ru": pokemon_next_evolution.name,
            "pokemon_id": pokemon_next_evolution.id,
            "img_url": request.build_absolute_uri(
                pokemon_next_evolution.image.url
            )
        }

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon_params
    })
