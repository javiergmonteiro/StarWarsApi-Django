from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, Http404
from django.core.cache import cache
from django.db.models import Avg
from django.db.models import Max

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView

from decouple import config
import requests

from .serializer import Character_Rating_Serializer
from .models import Character_Rating


def get_rating_data(data,character_id):
    character_ratings = Character_Rating.objects.filter(character=character_id)
    if character_ratings:
        data['average_rating'] = character_ratings.aggregate(Avg('rating'))['rating__avg']
        data['max_rating'] = character_ratings.aggregate(Max('rating'))['rating__max']
    else:
        data['average_rating'] = 0
        data['max_rating'] = 0
    return data


class CharacterDetail(APIView):

    def get(self,request,pk):
        base_url = config('SWAPI_BASE_URL')
        cache_data = cache.get('character_'+str(pk))
        if not cache_data:
            try:
                request = requests.get(base_url+'/people/'+str(pk)+'/')
            except Exception as e:
                #print(e)
                return JsonResponse(
                    {'status':'error','message':'an error ocurr trying to get the requested data, please try again later'},
                    status=400
                    )
            if request.status_code == 404:
                return HttpResponse(status=404)
            else:
                data = request.json()
                # delete extra data
                extra_data = ['films', 'vehicles', 'starships', 'url', 'edited', 'created']
                for key in extra_data:
                    if key in data:
                        del data[key]
                # replace homeworld data to homeworld_name
                try:
                    homeworld = requests.get(data['homeworld'])
                except Exception as e:
                    #print(e)
                    return JsonResponse(
                        {'status':'error','message':'an error ocurr trying to get the requested data, please try again later'},
                        status=400
                        )
                if homeworld.status_code == 200:
                    if homeworld.json():
                        howeworld_data = {}
                        howeworld_data['name'] = homeworld.json()['name']
                        howeworld_data['population'] = homeworld.json()['population']
                        howeworld_data['known_residents_count'] = len(homeworld.json()['residents'])
                        data['homeworld'] = howeworld_data
                    else:
                        data['homeworld_name'] = None
                        del data['homeworld']
                else:
                    data['homeworld_name'] = None
                    del data['homeworld']
                # replace species data to species_name
                if data['species']:
                    try:
                        specie = requests.get(data['species'][0])
                    except Exception as e:
                        #print(e)
                        return JsonResponse(
                            {'status':'error','message':'an error ocurr trying to get the requested data, please try again later'},
                            status=400
                            )
                    if specie.status_code == 200:
                        if 'name' in specie.json():
                            data['species_name'] = specie.json()['name']
                            del data['species']
                        else:
                            data['species_name'] = None
                            del data['species']
                    else:
                        data['species_name'] = None
                        del data['species']
                else:
                    data['species_name'] = None
                    del data['species']
                
                # get the average_rate value and max_field value
                data = get_rating_data(data,pk)
                cache.set('character_'+str(pk),data)
                return JsonResponse(data,status=200)
        else:
            data = get_rating_data(cache_data,pk)
            return JsonResponse(data,status=200)

    
class CharacterRating(viewsets.GenericViewSet):

    def rate(self,request,pk):
        try:
            data = JSONParser().parse(request)
        except:
            return HttpResponse(status=406)
        
        serializer = Character_Rating_Serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        else:
            return JsonResponse(serializer.errors, status=400)

        

