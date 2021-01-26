#!/usr/bin/env python3

##########################################################################
#
# Versión: 0.0.1 (07/01/2021)
# Autor: Francisco José Morón Reyes (fjmoronreyes@gmail.com)
#
##########################################################################

"""
Aplicación python que llama a una API para autenticarnos y descargar información de una red social, foros o de la web.
Podemos descargar el contenido en diversos formatos: HTML, XML o JSON.
"""

import tweepy
import json
import shutil, os
import requests
import xmltodict
from datetime import date

# Fecha
DATE = date.today()

###############
## API KEYS  ##
###############
'''
Claves necesarias para acceder a cada API. Son obtenidas tras el registro en cada página:
Twitter: https://developer.twitter.com/en/apply-for-access
Twingly: https://app.twingly.com/
Social Searcher: https://www.social-searcher.com/api-v2/
'''

# Twitter
CONSUMER_KEY = 'EprN4Z6QzAwe8oYCsGRGfQ7AM'
CONSUMER_SECRET = 'UFhLjH6ObQDJEry40MNICAp2qGbgX5rnZ3XvpMgmiey6QG8TN4'

ACCESS_TOKEN = '1341696673697959936-vsOwjoqvLna96OL7G8AKcjzOAJYGex'
ACCESS_TOKEN_SECRET = '8upfosxDjsS4O7NyN29sTZKgOaYq0nr1hquKdKT9iAB6C'

# Twingly
TWINGLY_API_KEY = '1F23CB5D-D84D-410E-B457-B6C6BCBFF172'

# Social Searcher
SOCIAL_SEARCHER_API_KEY = '132e156f84bb05ec69698590b9308586'


################################
## AUTENTICACIÓN Y PETICIONES ##
################################
'''Apartado donde realizamos la llamada a cada API. En función de la naturaleza de cada una, descargaremos
una serie de datos (aunque todos se pasarán a formato .JSON).'''



############
## TWITTER #
############
'''
Tweets

Aunque podemos extraer gran cantidad de información de twitter: followers, followees etc. Vamos a centrarnos en recuperar
Tweets en castellano y en inglés de diferentes usuarios.
'''

# Autenticación Twitter
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

# Petición GET (Usando .Cursor y llamando a la API de Twitter)
user = 'ZafonOficial'
tweets = tweepy.Cursor(api.user_timeline, screen_name=user, tweet_mode='extended').items(15)
num_name = 1

for tweet in tweets:
    tweet = json.dumps(tweet._json, indent=2)
    with open('TWITTER-' + user + '_' + str(num_name) + '-' + str(DATE) + '.json', 'w') as json_file:
        json_file.write(tweet)
    num_name = num_name + 1


############
## TWINGLY #
############
'''
Información de FOROS.

Twingly nos ofrece, mediante Query String, la posibilidad de hacer llamadas a su API. Para ello solo necesitamos
contar con la API Key y conocer la sintaxis de sus parámetros. Como nos devuelve un XML, lo parsearemos a JSON.
'''

twingly_base_url = 'https://api.twingly.com/blog/search/api/v3/search'
twingly_query = 'theater'
tspan = '24h'

# Petición GET (Usando la librería requests)
twingly_response = requests.get(twingly_base_url + '?apikey=' + TWINGLY_API_KEY + 
                                '&q=' + twingly_query + '%20tspan:' + tspan)
twingly_json = json.dumps(xmltodict.parse(twingly_response.text), indent=4)

with open('TWINGLY-' + twingly_query + '-' + tspan +
           '-' + str(DATE) + '.json', 'w') as json_file:
    json_file.write(twingly_json)
print(twingly_json)


########################
## SOCIAL SEARCHER API #
########################
'''
Información WEB genérica e información específica de varias redes sociales.

Social Searcher también ofrece su propia API accesible mediante Query String de la misma forma que Twingly. 
'''


# Petición GET de Información Web (Usando la librería requests)
social_searcher_base_url = 'https://api.social-searcher.com/v2/search?'
web = 'web'
social_searcher_query = 'shakespeare'

social_searcher_response = requests.get(social_searcher_base_url + 'q=' + social_searcher_query + 
                                       '&network=' + web + '&key=' + SOCIAL_SEARCHER_API_KEY).json()
social_searcher_json = json.dumps(social_searcher_response, indent=4)

with open('SOCIAL_SEARCHER-' + web.upper() + '-' + social_searcher_query 
          + '-' + str(DATE) + '.json', 'w') as json_file:
    json_file.write(social_searcher_json)
#print(social_searcher_json)


# Petición GET de Información sobre una red social determinada (Usando la librería request)
social_searcher_network_url = 'https://api.social-searcher.com/v2/users/'
network = 'twitter'
user = 'PatrickRothfuss'

social_searcher_network_response = requests.get('https://api.social-searcher.com/v2/users/' + user + 
                                                '/posts?key=' + SOCIAL_SEARCHER_API_KEY + '&network='
                                                + network).json()
network_json = json.dumps(social_searcher_network_response, indent=4)

with open('SOCIAL_SEARCHER-' + network.upper() + '-' + user + '-' + str(DATE) + '.json', 'w') as json_file:
    json_file.write(network_json)
print(network_json)
