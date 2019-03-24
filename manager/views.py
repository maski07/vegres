from __future__ import print_function
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView

from manager.models import *

from .SearchYelpResForm import SearchYelpResForm

##ここからyelpの実装

import argparse
import json
import pprint
import requests
import sys
import urllib


# This client code can run on Python 2.x or 3.x.  Your imports can be
# simpler if you only need one of those.
try:
    # For Python 3.0 and later
    from urllib.error import HTTPError
    from urllib.parse import quote
    from urllib.parse import urlencode
except ImportError:
    # Fall back to Python 2's urllib2 and urllib
    from urllib2 import HTTPError
    from urllib import quote
    from urllib import urlencode

API_KEY= 'Mee1peM6diEGMyIEwt2RXeISI0kfPKT6sDxZeQJeNouXBmYfuMecxZOcANntEsvQa203NTcHuHYdB20vf6sTglGYjjQAsJCloWVoHEsWkL1C5-ERIHycaOf_5B5yXHYx'

# API constants, you shouldn't have to change these.
API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
BUSINESS_PATH = '/v3/businesses/'  # Business ID will come after slash.

# Defaults for our simple example.
DEFAULT_TERM = 'dinner'
DEFAULT_LOCATION = 'TOKYO'
SEARCH_LIMIT = 3

#import pdb; pdb.set_trace()#デバッグ

class WorkerListView(TemplateView):
    template_name = "worker_list.html"

    def get(self, request, *args, **kwargs):
        context = super(WorkerListView, self).get_context_data(**kwargs)
        #response = self.searchRestaurant(request)  # yelp-API呼び出し
        #response = self.tempRes() #インターネット接続できない時用
        #context['restaurant'] = response  # 入れ物に入れる
        params = {
            'title':'Vegetable',
            'term':'dinner',
            'location':'Tokyo'#,
            #'restaurant':response
        }

        return render(self.request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        context = super(WorkerListView, self).get_context_data(**kwargs)
        response = self.searchRestaurant(request)  # yelp-API呼び出し
        #response = self.tempRes() #インターネットに接続できない時用
        context['restaurant'] = response  # 入れ物に入れる
        params = {
            'title':'Vegetable',
            'term':'dinner',
            'location':'Tokyo',
            'restaurant':response
        }
        return render(self.request, self.template_name, context)

    def searchRestaurant(self, request):
        parser = argparse.ArgumentParser()
        '''parser.add_argument('-q', '--term', dest='term', default=DEFAULT_TERM,
                            type=str, help='Search term (default: %(default)s)')
        parser.add_argument('-l', '--location', dest='location',
                            default=DEFAULT_LOCATION, type=str,
                            help='Search location (default: %(default)s)')
        import pdb; pdb.set_trace()#デバッグ
        input_values = parser.parse_args() #requestを受け取ってる？<-たぶん
        '''
        if(request.method == 'POST'):
            term = request.POST['term']
            location = request.POST['location']
        try:
            response = self.query_api(term, location)
        except HTTPError as error:
            sys.exit(
                'Encountered HTTP error {0} on {1}:\n {2}\nAbort program.'.format(
                    error.code,
                    error.url,
                    error.read(),
                )
            )
        except KeyError :
            return '入力ミス'
        return response

    def query_api(self, term, location):
        """Queries the API by the input values from the user.

        Args:
            term (str): The search term to query.
            location (str): The location of the business to query.
        """
        response = self.search(API_KEY, term, location)

        businesses = response.get('businesses')

        if not businesses:
            print(u'No businesses for {0} in {1} found.'.format(term, location))
            return

        business_id = businesses[0]['id']

        print(u'{0} businesses found, querying business info ' \
            'for the top result "{1}" ...'.format(
                len(businesses), business_id))
        #一旦コメントアウト（ここでエラー出る）
        #response = get_business(API_KEY, business_id)

        print(u'Result for business "{0}" found:'.format(business_id))
        pprint.pprint(response, indent=2)
        return response

    def get_business(self, api_key, business_id):
        """Query the Business API by a business ID.

        Args:
            business_id (str): The ID of the business to query.

        Returns:
            dict: The JSON response from the request.
        """
        business_path = BUSINESS_PATH + business_id

        return request(API_HOST, business_path, api_key)

    def search(self, api_key, term, location):
        """Query the Search API by a search term and location.

        Args:
            term (str): The search term passed to the API.
            location (str): The search location passed to the API.

        Returns:
            dict: The JSON response from the request.
        """
        url_params = {
            'term': term.replace(' ', '+'),
            'location': location.replace(' ', '+'),
            'limit': SEARCH_LIMIT
        }
        response = self.reqRestaurant(API_HOST, SEARCH_PATH, api_key, url_params=url_params)
        return response

    def reqRestaurant(self, host, path, api_key, url_params=None):
        """Given your API_KEY, send a GET request to the API.

        Args:
            host (str): The domain host of the API.
            path (str): The path of the API after the domain.
            API_KEY (str): Your API Key.
            url_params (dict): An optional set of query parameters in the request.

        Returns:
            dict: The JSON response from the request.

        Raises:
            HTTPError: An error occurs from the HTTP request.
        """
        url_params = url_params or {}
        url = '{0}{1}'.format(host, quote(path.encode('utf8')))
        headers = {
            'Authorization': 'Bearer %s' % api_key,
        }
        print(u'Querying {0} ...'.format(url))
        response = requests.request('GET', url, headers=headers, params=url_params)

        return response.json()

    def tempRes(self):
        response = {
    "businesses": [
        {
            "id": "FmGF1B-Rpsjq1f5b56qMwg",
            "alias": "molinari-delicatessen-san-francisco",
            "name": "Molinari Delicatessen",
            "image_url": "https://s3-media3.fl.yelpcdn.com/bphoto/6He-NlZrAv2mDV-yg6jW3g/o.jpg",
            "is_closed": "false",
            "url": "https://www.yelp.com/biz/molinari-delicatessen-san-francisco?adjust_creative=xe2y73KrodGMkJrboERFnA&utm_campaign=yelp_api_v3&utm_medium=api_v3_business_search&utm_source=xe2y73KrodGMkJrboERFnA",
            "review_count": 1044,
            "categories": [
                {
                    "alias": "delis",
                    "title": "Delis"
                }
            ],
            "rating": 4.5,
            "coordinates": {
                "latitude": 37.79838,
                "longitude": -122.40782
            },
            "transactions": [
                "pickup",
                "delivery"
            ],
            "price": "$$",
            "location": {
                "address1": "373 Columbus Ave",
                "address2": "",
                "address3": "",
                "city": "San Francisco",
                "zip_code": "94133",
                "country": "US",
                "state": "CA",
                "display_address": [
                    "373 Columbus Ave",
                    "San Francisco, CA 94133"
                ]
            },
            "phone": "+14154212337",
            "display_phone": "(415) 421-2337",
            "distance": 1453.998141679007
        },
        {
            "id": "BcW0vRdM8N-rteR2FfV1jg",
            "alias": "deli-board-san-francisco",
            "name": "Deli Board",
            "image_url": "https://s3-media3.fl.yelpcdn.com/bphoto/m5dL_mNk9rjSJ5jQu17hVw/o.jpg",
            "is_closed": "false",
            "url": "https://www.yelp.com/biz/deli-board-san-francisco?adjust_creative=xe2y73KrodGMkJrboERFnA&utm_campaign=yelp_api_v3&utm_medium=api_v3_business_search&utm_source=xe2y73KrodGMkJrboERFnA",
            "review_count": 1218,
            "categories": [
                {
                    "alias": "delis",
                    "title": "Delis"
                },
                {
                    "alias": "sandwiches",
                    "title": "Sandwiches"
                }
            ],
            "rating": 4.5,
            "coordinates": {
                "latitude": 37.7776247966103,
                "longitude": -122.407012712007
            },
            "transactions": [],
            "price": "$$",
            "location": {
                "address1": "1058 Folsom St",
                "address2": "",
                "address3": "",
                "city": "San Francisco",
                "zip_code": "94103",
                "country": "US",
                "state": "CA",
                "display_address": [
                    "1058 Folsom St",
                    "San Francisco, CA 94103"
                ]
            },
            "phone": "+14155527687",
            "display_phone": "(415) 552-7687",
            "distance": 1201.0092939107112
        },
        {
            "id": "eZ2_6Wx-Lqp_mLtG6-zzTg",
            "alias": "sammys-on-2nd-san-francisco",
            "name": "Sammy's on 2nd",
            "image_url": "https://s3-media2.fl.yelpcdn.com/bphoto/GWvs007fUKMbyftq-_E7QQ/o.jpg",
            "is_closed": "false",
            "url": "https://www.yelp.com/biz/sammys-on-2nd-san-francisco?adjust_creative=xe2y73KrodGMkJrboERFnA&utm_campaign=yelp_api_v3&utm_medium=api_v3_business_search&utm_source=xe2y73KrodGMkJrboERFnA",
            "review_count": 199,
            "categories": [
                {
                    "alias": "beer_and_wine",
                    "title": "Beer, Wine & Spirits"
                },
                {
                    "alias": "sandwiches",
                    "title": "Sandwiches"
                }
            ],
            "rating": 4,
            "coordinates": {
                "latitude": 37.7881,
                "longitude": -122.40028
            },
            "transactions": [],
            "price": "$",
            "location": {
                "address1": "84 2nd St",
                "address2": "null",
                "address3": "",
                "city": "San Francisco",
                "zip_code": "94105",
                "country": "US",
                "state": "CA",
                "display_address": [
                    "84 2nd St",
                    "San Francisco, CA 94105"
                ]
            },
            "phone": "+14152430311",
            "display_phone": "(415) 243-0311",
            "distance": 146.3807329561209
        },
        {
            "id": "VH9Zfe0ip-7LRKrvNT_5Iw",
            "alias": "the-boys-deli-san-francisco-3",
            "name": "The Boy's Deli",
            "image_url": "https://s3-media4.fl.yelpcdn.com/bphoto/Hcf08mV7wZKONU1Pm4olPQ/o.jpg",
            "is_closed": "false",
            "url": "https://www.yelp.com/biz/the-boys-deli-san-francisco-3?adjust_creative=xe2y73KrodGMkJrboERFnA&utm_campaign=yelp_api_v3&utm_medium=api_v3_business_search&utm_source=xe2y73KrodGMkJrboERFnA",
            "review_count": 11,
            "categories": [
                {
                    "alias": "sandwiches",
                    "title": "Sandwiches"
                },
                {
                    "alias": "breakfast_brunch",
                    "title": "Breakfast & Brunch"
                },
                {
                    "alias": "soup",
                    "title": "Soup"
                }
            ],
            "rating": 4.5,
            "coordinates": {
                "latitude": 37.79214,
                "longitude": -122.40285
            },
            "transactions": [],
            "location": {
                "address1": "315 Montgomery St",
                "address2": "Ste E",
                "address3": "null",
                "city": "San Francisco",
                "zip_code": "94104",
                "country": "US",
                "state": "CA",
                "display_address": [
                    "315 Montgomery St",
                    "Ste E",
                    "San Francisco, CA 94104"
                ]
            },
            "phone": "+14156587970",
            "display_phone": "(415) 658-7970",
            "distance": 635.180371008062
        },
        {
            "id": "0mZeR3TwxmZGLCxzcf620A",
            "alias": "5th-avenue-deli-and-market-san-francisco",
            "name": "5th Avenue Deli & Market",
            "image_url": "https://s3-media2.fl.yelpcdn.com/bphoto/kCw-46xiRawlFBGyK85OwA/o.jpg",
            "is_closed": "false",
            "url": "https://www.yelp.com/biz/5th-avenue-deli-and-market-san-francisco?adjust_creative=xe2y73KrodGMkJrboERFnA&utm_campaign=yelp_api_v3&utm_medium=api_v3_business_search&utm_source=xe2y73KrodGMkJrboERFnA",
            "review_count": 36,
            "categories": [
                {
                    "alias": "delis",
                    "title": "Delis"
                },
                {
                    "alias": "grocery",
                    "title": "Grocery"
                },
                {
                    "alias": "sandwiches",
                    "title": "Sandwiches"
                }
            ],
            "rating": 4.5,
            "coordinates": {
                "latitude": 37.79553,
                "longitude": -122.39623
            },
            "transactions": [
                "pickup",
                "delivery"
            ],
            "price": "$",
            "location": {
                "address1": "4 Embarcadero Ctr",
                "address2": "",
                "address3": "",
                "city": "San Francisco",
                "zip_code": "94111",
                "country": "US",
                "state": "CA",
                "display_address": [
                    "4 Embarcadero Ctr",
                    "San Francisco, CA 94111"
                ]
            },
            "phone": "+14157570950",
            "display_phone": "(415) 757-0950",
            "distance": 1005.1181487091517
        },
        {
            "id": "dv9gdJrBG7SZ8aWYkxG_3w",
            "alias": "sutter-st-cafe-san-francisco",
            "name": "Sutter St. Cafe",
            "image_url": "https://s3-media3.fl.yelpcdn.com/bphoto/VcKDYThd72i27lPfwoRlPg/o.jpg",
            "is_closed": "false",
            "url": "https://www.yelp.com/biz/sutter-st-cafe-san-francisco?adjust_creative=xe2y73KrodGMkJrboERFnA&utm_campaign=yelp_api_v3&utm_medium=api_v3_business_search&utm_source=xe2y73KrodGMkJrboERFnA",
            "review_count": 173,
            "categories": [
                {
                    "alias": "cafes",
                    "title": "Cafes"
                },
                {
                    "alias": "delis",
                    "title": "Delis"
                }
            ],
            "rating": 4.5,
            "coordinates": {
                "latitude": 37.7894760577176,
                "longitude": -122.407699611023
            },
            "transactions": [
                "pickup"
            ],
            "price": "$",
            "location": {
                "address1": "450 Sutter St",
                "address2": "null",
                "address3": "",
                "city": "San Francisco",
                "zip_code": "94108",
                "country": "US",
                "state": "CA",
                "display_address": [
                    "450 Sutter St",
                    "San Francisco, CA 94108"
                ]
            },
            "phone": "+14153628342",
            "display_phone": "(415) 362-8342",
            "distance": 737.7876443304846
        },
        {
            "id": "MWV8AoySYObkfVpaLhaqKQ",
            "alias": "sf-deli-and-wine-san-francisco-3",
            "name": "SF Deli & Wine",
            "image_url": "https://s3-media3.fl.yelpcdn.com/bphoto/54PEA7BhYSnyTs3YqOxa5Q/o.jpg",
            "is_closed": "false",
            "url": "https://www.yelp.com/biz/sf-deli-and-wine-san-francisco-3?adjust_creative=xe2y73KrodGMkJrboERFnA&utm_campaign=yelp_api_v3&utm_medium=api_v3_business_search&utm_source=xe2y73KrodGMkJrboERFnA",
            "review_count": 25,
            "categories": [
                {
                    "alias": "beer_and_wine",
                    "title": "Beer, Wine & Spirits"
                },
                {
                    "alias": "delis",
                    "title": "Delis"
                }
            ],
            "rating": 4,
            "coordinates": {
                "latitude": 37.7839431994157,
                "longitude": -122.405098485531
            },
            "transactions": [
                "pickup",
                "delivery"
            ],
            "price": "$",
            "location": {
                "address1": "810 Mission St",
                "address2": "",
                "address3": "",
                "city": "San Francisco",
                "zip_code": "94103",
                "country": "US",
                "state": "CA",
                "display_address": [
                    "810 Mission St",
                    "San Francisco, CA 94103"
                ]
            },
            "phone": "+14155127847",
            "display_phone": "(415) 512-7847",
            "distance": 556.544681533414
        },
        {
            "id": "zYUgm_qOcly8mhLdTSFnKw",
            "alias": "palermo-ii-delicatessen-san-francisco",
            "name": "Palermo II Delicatessen",
            "image_url": "https://s3-media4.fl.yelpcdn.com/bphoto/47DciaUfzII175Wj4Stm_w/o.jpg",
            "is_closed": "false",
            "url": "https://www.yelp.com/biz/palermo-ii-delicatessen-san-francisco?adjust_creative=xe2y73KrodGMkJrboERFnA&utm_campaign=yelp_api_v3&utm_medium=api_v3_business_search&utm_source=xe2y73KrodGMkJrboERFnA",
            "review_count": 46,
            "categories": [
                {
                    "alias": "delis",
                    "title": "Delis"
                },
                {
                    "alias": "sandwiches",
                    "title": "Sandwiches"
                },
                {
                    "alias": "italian",
                    "title": "Italian"
                }
            ],
            "rating": 5,
            "coordinates": {
                "latitude": 37.79894,
                "longitude": -122.4086
            },
            "transactions": [
                "pickup",
                "delivery"
            ],
            "location": {
                "address1": "658 Vallejo St",
                "address2": "null",
                "address3": "",
                "city": "San Francisco",
                "zip_code": "94133",
                "country": "US",
                "state": "CA",
                "display_address": [
                    "658 Vallejo St",
                    "San Francisco, CA 94133"
                ]
            },
            "phone": "+14159370161",
            "display_phone": "(415) 937-0161",
            "distance": 1517.0065811617371
        },
        {
            "id": "uFeOc6t94xLp-JPP6fhnaA",
            "alias": "wise-sons-jewish-delicatessen-san-francisco-2",
            "name": "Wise Sons Jewish Delicatessen",
            "image_url": "https://s3-media3.fl.yelpcdn.com/bphoto/Gp9tnIQJqnCN9sWMacCn8g/o.jpg",
            "is_closed": "false",
            "url": "https://www.yelp.com/biz/wise-sons-jewish-delicatessen-san-francisco-2?adjust_creative=xe2y73KrodGMkJrboERFnA&utm_campaign=yelp_api_v3&utm_medium=api_v3_business_search&utm_source=xe2y73KrodGMkJrboERFnA",
            "review_count": 275,
            "categories": [
                {
                    "alias": "sandwiches",
                    "title": "Sandwiches"
                },
                {
                    "alias": "bagels",
                    "title": "Bagels"
                },
                {
                    "alias": "soup",
                    "title": "Soup"
                }
            ],
            "rating": 3.5,
            "coordinates": {
                "latitude": 37.7861320529474,
                "longitude": -122.40342621841
            },
            "transactions": [],
            "price": "$$",
            "location": {
                "address1": "736 Mission St",
                "address2": "",
                "address3": "The Contemporary Jewish Museum",
                "city": "San Francisco",
                "zip_code": "94103",
                "country": "US",
                "state": "CA",
                "display_address": [
                    "736 Mission St",
                    "The Contemporary Jewish Museum",
                    "San Francisco, CA 94103"
                ]
            },
            "phone": "+14156557887",
            "display_phone": "(415) 655-7887",
            "distance": 314.79308965734816
        },
        {
            "id": "KRO4PzfmbRgCu1Ayt1LE1g",
            "alias": "mortys-delicatessen-san-francisco",
            "name": "Morty's Delicatessen",
            "image_url": "https://s3-media3.fl.yelpcdn.com/bphoto/NW5NwtCk404qF-UJd-OlVg/o.jpg",
            "is_closed": "false",
            "url": "https://www.yelp.com/biz/mortys-delicatessen-san-francisco?adjust_creative=xe2y73KrodGMkJrboERFnA&utm_campaign=yelp_api_v3&utm_medium=api_v3_business_search&utm_source=xe2y73KrodGMkJrboERFnA",
            "review_count": 508,
            "categories": [
                {
                    "alias": "sandwiches",
                    "title": "Sandwiches"
                },
                {
                    "alias": "delis",
                    "title": "Delis"
                },
                {
                    "alias": "vegetarian",
                    "title": "Vegetarian"
                }
            ],
            "rating": 4,
            "coordinates": {
                "latitude": 37.78188,
                "longitude": -122.41522
            },
            "transactions": [
                "pickup",
                "delivery"
            ],
            "price": "$",
            "location": {
                "address1": "280 Golden Gate Ave",
                "address2": "null",
                "address3": "",
                "city": "San Francisco",
                "zip_code": "94102",
                "country": "US",
                "state": "CA",
                "display_address": [
                    "280 Golden Gate Ave",
                    "San Francisco, CA 94102"
                ]
            },
            "phone": "+14155673354",
            "display_phone": "(415) 567-3354",
            "distance": 1457.5130699421723
        },
        {
            "id": "ZXwnSN4GlEuSTNCRrjjRMg",
            "alias": "bite-san-francisco",
            "name": "Bite",
            "image_url": "https://s3-media3.fl.yelpcdn.com/bphoto/sqHzrKnBj7dLOCJYX34Hzg/o.jpg",
            "is_closed": "false",
            "url": "https://www.yelp.com/biz/bite-san-francisco?adjust_creative=xe2y73KrodGMkJrboERFnA&utm_campaign=yelp_api_v3&utm_medium=api_v3_business_search&utm_source=xe2y73KrodGMkJrboERFnA",
            "review_count": 707,
            "categories": [
                {
                    "alias": "delis",
                    "title": "Delis"
                },
                {
                    "alias": "sandwiches",
                    "title": "Sandwiches"
                },
                {
                    "alias": "salad",
                    "title": "Salad"
                }
            ],
            "rating": 4,
            "coordinates": {
                "latitude": 37.7884239641,
                "longitude": -122.415666133
            },
            "transactions": [
                "pickup",
                "delivery"
            ],
            "price": "$$",
            "location": {
                "address1": "912 Sutter St",
                "address2": "",
                "address3": "",
                "city": "San Francisco",
                "zip_code": "94104",
                "country": "US",
                "state": "CA",
                "display_address": [
                    "912 Sutter St",
                    "San Francisco, CA 94104"
                ]
            },
            "phone": "+14155632483",
            "display_phone": "(415) 563-2483",
            "distance": 1389.7519934105944
        },
        {
            "id": "kEhq0qT_JFxgeh-pCS4lPA",
            "alias": "the-sentinel-san-francisco",
            "name": "The Sentinel",
            "image_url": "https://s3-media4.fl.yelpcdn.com/bphoto/bmLhuYADb1MNQJATh5Bfzw/o.jpg",
            "is_closed": "false",
            "url": "https://www.yelp.com/biz/the-sentinel-san-francisco?adjust_creative=xe2y73KrodGMkJrboERFnA&utm_campaign=yelp_api_v3&utm_medium=api_v3_business_search&utm_source=xe2y73KrodGMkJrboERFnA",
            "review_count": 1285,
            "categories": [
                {
                    "alias": "sandwiches",
                    "title": "Sandwiches"
                }
            ],
            "rating": 4,
            "coordinates": {
                "latitude": 37.7882977785009,
                "longitude": -122.401372356986
            },
            "transactions": [
                "pickup",
                "delivery"
            ],
            "price": "$",
            "location": {
                "address1": "37 New Montgomery St",
                "address2": "",
                "address3": "",
                "city": "San Francisco",
                "zip_code": "94105",
                "country": "US",
                "state": "CA",
                "display_address": [
                    "37 New Montgomery St",
                    "San Francisco, CA 94105"
                ]
            },
            "phone": "+14157698109",
            "display_phone": "(415) 769-8109",
            "distance": 199.81617618665948
        },
        {
            "id": "kK0s7FAovaLmVDM4D_NdSQ",
            "alias": "good-luck-cafe-and-deli-san-francisco",
            "name": "Good Luck Cafe and Deli",
            "image_url": "https://s3-media3.fl.yelpcdn.com/bphoto/7diLgtddAjlrYm_62uLvUQ/o.jpg",
            "is_closed": "false",
            "url": "https://www.yelp.com/biz/good-luck-cafe-and-deli-san-francisco?adjust_creative=xe2y73KrodGMkJrboERFnA&utm_campaign=yelp_api_v3&utm_medium=api_v3_business_search&utm_source=xe2y73KrodGMkJrboERFnA",
            "review_count": 392,
            "categories": [
                {
                    "alias": "delis",
                    "title": "Delis"
                },
                {
                    "alias": "cafes",
                    "title": "Cafes"
                },
                {
                    "alias": "sandwiches",
                    "title": "Sandwiches"
                }
            ],
            "rating": 4.5,
            "coordinates": {
                "latitude": 37.793838,
                "longitude": -122.404846
            },
            "transactions": [],
            "price": "$",
            "location": {
                "address1": "621 Kearny St",
                "address2": "null",
                "address3": "",
                "city": "San Francisco",
                "zip_code": "94108",
                "country": "US",
                "state": "CA",
                "display_address": [
                    "621 Kearny St",
                    "San Francisco, CA 94108"
                ]
            },
            "phone": "+14157812328",
            "display_phone": "(415) 781-2328",
            "distance": 885.8862602767963
        },
        {
            "id": "gtBDOQq3TyiiulKmJpny0g",
            "alias": "lous-cafe-san-francisco-5",
            "name": "Lou's Cafe",
            "image_url": "https://s3-media1.fl.yelpcdn.com/bphoto/SnjVCB4U3dr83c381ZNyQA/o.jpg",
            "is_closed": "false",
            "url": "https://www.yelp.com/biz/lous-cafe-san-francisco-5?adjust_creative=xe2y73KrodGMkJrboERFnA&utm_campaign=yelp_api_v3&utm_medium=api_v3_business_search&utm_source=xe2y73KrodGMkJrboERFnA",
            "review_count": 144,
            "categories": [
                {
                    "alias": "salad",
                    "title": "Salad"
                },
                {
                    "alias": "soup",
                    "title": "Soup"
                },
                {
                    "alias": "sandwiches",
                    "title": "Sandwiches"
                }
            ],
            "rating": 4.5,
            "coordinates": {
                "latitude": 37.7926406860352,
                "longitude": -122.398971557617
            },
            "transactions": [
                "pickup",
                "delivery"
            ],
            "price": "$",
            "location": {
                "address1": "100 Pine St",
                "address2": "Ste 102",
                "address3": "",
                "city": "San Francisco",
                "zip_code": "94111",
                "country": "US",
                "state": "CA",
                "display_address": [
                    "100 Pine St",
                    "Ste 102",
                    "San Francisco, CA 94111"
                ]
            },
            "phone": "+14152834777",
            "display_phone": "(415) 283-4777",
            "distance": 639.8335087574524
        },
        {
            "id": "RZKmlQqq8XN82VwcEgMhqQ",
            "alias": "kama-o-deli-san-francisco",
            "name": "Kama O Deli",
            "image_url": "https://s3-media4.fl.yelpcdn.com/bphoto/kuOuELX_obb5YiS9Qq1YRw/o.jpg",
            "is_closed": "false",
            "url": "https://www.yelp.com/biz/kama-o-deli-san-francisco?adjust_creative=xe2y73KrodGMkJrboERFnA&utm_campaign=yelp_api_v3&utm_medium=api_v3_business_search&utm_source=xe2y73KrodGMkJrboERFnA",
            "review_count": 74,
            "categories": [
                {
                    "alias": "delis",
                    "title": "Delis"
                },
                {
                    "alias": "japanese",
                    "title": "Japanese"
                }
            ],
            "rating": 4,
            "coordinates": {
                "latitude": 37.7801891062951,
                "longitude": -122.394493681462
            },
            "transactions": [
                "pickup"
            ],
            "price": "$$",
            "location": {
                "address1": "590 3rd St",
                "address2": "",
                "address3": "",
                "city": "San Francisco",
                "zip_code": "94107",
                "country": "US",
                "state": "CA",
                "display_address": [
                    "590 3rd St",
                    "San Francisco, CA 94107"
                ]
            },
            "phone": "+14158729622",
            "display_phone": "(415) 872-9622",
            "distance": 879.3176729871393
        },
        {
            "id": "B61vZd9neTI8F7zZ-vApmw",
            "alias": "the-boys-deli-san-francisco",
            "name": "The Boy's Deli",
            "image_url": "https://s3-media3.fl.yelpcdn.com/bphoto/qXbjX3opOgmgN_5NsCb9Cw/o.jpg",
            "is_closed": "false",
            "url": "https://www.yelp.com/biz/the-boys-deli-san-francisco?adjust_creative=xe2y73KrodGMkJrboERFnA&utm_campaign=yelp_api_v3&utm_medium=api_v3_business_search&utm_source=xe2y73KrodGMkJrboERFnA",
            "review_count": 281,
            "categories": [
                {
                    "alias": "delis",
                    "title": "Delis"
                },
                {
                    "alias": "meats",
                    "title": "Meat Shops"
                },
                {
                    "alias": "sandwiches",
                    "title": "Sandwiches"
                }
            ],
            "rating": 4.5,
            "coordinates": {
                "latitude": 37.7971806,
                "longitude": -122.421842
            },
            "transactions": [
                "pickup",
                "delivery"
            ],
            "price": "$",
            "location": {
                "address1": "2222 Polk St",
                "address2": "",
                "address3": "Polk & Green Produce Market",
                "city": "San Francisco",
                "zip_code": "94109",
                "country": "US",
                "state": "CA",
                "display_address": [
                    "2222 Polk St",
                    "Polk & Green Produce Market",
                    "San Francisco, CA 94109"
                ]
            },
            "phone": "+14157763099",
            "display_phone": "(415) 776-3099",
            "distance": 2235.2674125931903
        },
        {
            "id": "4NInBK_67cLRyUS7sq0CEg",
            "alias": "millers-east-coast-deli-san-francisco",
            "name": "Miller's East Coast Deli",
            "image_url": "https://s3-media4.fl.yelpcdn.com/bphoto/dp0f0riyDlevyCG2hwKx-Q/o.jpg",
            "is_closed": "false",
            "url": "https://www.yelp.com/biz/millers-east-coast-deli-san-francisco?adjust_creative=xe2y73KrodGMkJrboERFnA&utm_campaign=yelp_api_v3&utm_medium=api_v3_business_search&utm_source=xe2y73KrodGMkJrboERFnA",
            "review_count": 1452,
            "categories": [
                {
                    "alias": "delis",
                    "title": "Delis"
                },
                {
                    "alias": "sandwiches",
                    "title": "Sandwiches"
                },
                {
                    "alias": "breakfast_brunch",
                    "title": "Breakfast & Brunch"
                }
            ],
            "rating": 3.5,
            "coordinates": {
                "latitude": 37.79273,
                "longitude": -122.42145
            },
            "transactions": [
                "pickup",
                "delivery"
            ],
            "price": "$$",
            "location": {
                "address1": "1725 Polk St",
                "address2": "",
                "address3": "",
                "city": "San Francisco",
                "zip_code": "94109",
                "country": "US",
                "state": "CA",
                "display_address": [
                    "1725 Polk St",
                    "San Francisco, CA 94109"
                ]
            },
            "phone": "+14155633542",
            "display_phone": "(415) 563-3542",
            "distance": 1993.4476800653433
        },
        {
            "id": "CaqzKTAzHfPOIFkLp7xyBQ",
            "alias": "mendocino-farms-san-francisco",
            "name": "Mendocino Farms",
            "image_url": "https://s3-media2.fl.yelpcdn.com/bphoto/SO2h0y1fsVft0aUWp1d2Uw/o.jpg",
            "is_closed": "false",
            "url": "https://www.yelp.com/biz/mendocino-farms-san-francisco?adjust_creative=xe2y73KrodGMkJrboERFnA&utm_campaign=yelp_api_v3&utm_medium=api_v3_business_search&utm_source=xe2y73KrodGMkJrboERFnA",
            "review_count": 114,
            "categories": [
                {
                    "alias": "sandwiches",
                    "title": "Sandwiches"
                },
                {
                    "alias": "salad",
                    "title": "Salad"
                }
            ],
            "rating": 4,
            "coordinates": {
                "latitude": 37.79278,
                "longitude": -122.40219
            },
            "transactions": [],
            "price": "$$",
            "location": {
                "address1": "465 California St",
                "address2": "",
                "address3": "null",
                "city": "San Francisco",
                "zip_code": "94104",
                "country": "US",
                "state": "CA",
                "display_address": [
                    "465 California St",
                    "San Francisco, CA 94104"
                ]
            },
            "phone": "+14153212170",
            "display_phone": "(415) 321-2170",
            "distance": 673.0068373556628
        },
        {
            "id": "zHqoPRK7sWS0trwa5emlMw",
            "alias": "liquor-and-deli-on-union-square-san-francisco",
            "name": "Liquor & Deli On Union Square",
            "image_url": "https://s3-media4.fl.yelpcdn.com/bphoto/k-RcZMZVehmkN_RyPhXp1Q/o.jpg",
            "is_closed": "false",
            "url": "https://www.yelp.com/biz/liquor-and-deli-on-union-square-san-francisco?adjust_creative=xe2y73KrodGMkJrboERFnA&utm_campaign=yelp_api_v3&utm_medium=api_v3_business_search&utm_source=xe2y73KrodGMkJrboERFnA",
            "review_count": 33,
            "categories": [
                {
                    "alias": "beer_and_wine",
                    "title": "Beer, Wine & Spirits"
                },
                {
                    "alias": "delis",
                    "title": "Delis"
                }
            ],
            "rating": 4,
            "coordinates": {
                "latitude": 37.79,
                "longitude": -122.40729
            },
            "transactions": [
                "pickup"
            ],
            "price": "$",
            "location": {
                "address1": "423 Stockton St",
                "address2": "",
                "address3": "",
                "city": "San Francisco",
                "zip_code": "94108",
                "country": "US",
                "state": "CA",
                "display_address": [
                    "423 Stockton St",
                    "San Francisco, CA 94108"
                ]
            },
            "phone": "+14154348210",
            "display_phone": "(415) 434-8210",
            "distance": 729.9634773299399
        },
        {
            "id": "2TUrb8EZwHY3Ouj67sdaaA",
            "alias": "wise-sons-delicatessen-san-francisco-4",
            "name": "Wise Sons Delicatessen",
            "image_url": "https://s3-media3.fl.yelpcdn.com/bphoto/cCEHQjWY_Ajwizbn-rk4eQ/o.jpg",
            "is_closed": "false",
            "url": "https://www.yelp.com/biz/wise-sons-delicatessen-san-francisco-4?adjust_creative=xe2y73KrodGMkJrboERFnA&utm_campaign=yelp_api_v3&utm_medium=api_v3_business_search&utm_source=xe2y73KrodGMkJrboERFnA",
            "review_count": 155,
            "categories": [
                {
                    "alias": "delis",
                    "title": "Delis"
                },
                {
                    "alias": "sandwiches",
                    "title": "Sandwiches"
                }
            ],
            "rating": 4,
            "coordinates": {
                "latitude": 37.7953897580148,
                "longitude": -122.393274307251
            },
            "transactions": [],
            "price": "$$",
            "location": {
                "address1": "Ferry Building Farmer's Market",
                "address2": "",
                "address3": "1 Ferry Bldg",
                "city": "San Francisco",
                "zip_code": "94105",
                "country": "US",
                "state": "CA",
                "display_address": [
                    "Ferry Building Farmer's Market",
                    "1 Ferry Bldg",
                    "San Francisco, CA 94105"
                ]
            },
            "phone": "+14157875534",
            "display_phone": "(415) 787-5534",
            "distance": 1114.1486963413138
        }
    ],
    "total": 810,
    "region": {
        "center": {
            "longitude": -122.399972,
            "latitude": 37.786882
        }
    }
}

        return response
