from __future__ import print_function
# Create your views here.
from django.shortcuts import render  # , redirect, get_object_or_404
from django.views.generic import TemplateView

# from manager.models import *

# from .SearchYelpResForm import SearchYelpResForm

# ここからyelpの実装

import argparse
import pprint
import requests
import sys
import json
# import urllib

# This client code can run on Python 2.x or 3.x.  Your imports can be
# simpler if you only need one of those.
try:
    # For Python 3.0 and later
    from urllib.error import HTTPError
    from urllib.parse import quote
    # from urllib.parse import urlencode
except ImportError:
    # Fall back to Python 2's urllib2 and urllib
    from urllib2 import HTTPError
    from urllib import quote
    # from urllib import urlencode


# API constants, you shouldn't have to change these.
API_KEY='Mee1peM6diEGMyIEwt2RXeISI0kfPKT6sDxZeQJeNouXBmYfuMecxZOcANntEsvQa203NTcHuHYdB20vf6sTglGYjjQAsJCloWVoHEsWkL1C5-ERIHycaOf_5B5yXHYx'
API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
BUSINESS_PATH = '/v3/businesses/'  # Business ID will come after slash.

# Defaults for our simple example.
DEFAULT_TERM = 'vegan'
DEFAULT_LOCATION = 'TOKYO'
SEARCH_LIMIT = 3

# デバッグ用コード
# import pdb; pdb.set_trace()


class SearchYelpRestaurant(TemplateView):
    # TODO:検索機能はオブジェクト化したい

    template_name = "searchResult.html"

    def get(self, request, *args, **kwargs):
        context = super(SearchYelpRestaurant, self).get_context_data(**kwargs)
        # context['restaurant'] = response  # 入れ物に入れる
        return render(self.request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        context = super(SearchYelpRestaurant, self).get_context_data(**kwargs)
        # yelp-API呼び出し
        response = self.searchRestaurant(request)
        # 入れ物に入れる
        context['restaurant'] = response

        # html表示用にparamsを作成
        params = self.makeParams(response)

        return render(self.request, self.template_name, params)

    def makeParams(self, response):
        if response is not None:
            businesses = response["businesses"]
            params = {
                'restaurant': response,
                'title': 'Vegetable',
                'alias': businesses[0]["alias"],  # 店舗名
                'address': businesses[0]["location"]["display_address"],
                'phone': businesses[0]["phone"],
                'url': businesses[0]["url"],
                'image_url': businesses[0]["image_url"]
            }
            return params
        return response

    def searchRestaurant(self, request):
        # 使い方不明のため一旦コメントアウト
        ''' parser = argparse.ArgumentParser()
        parser.add_argument('-q', '--term', dest='term', default=DEFAULT_TERM,
                            type=str, help='Search term (default: %(default)s)')
        parser.add_argument('-l', '--location', dest='location',
                            default=DEFAULT_LOCATION, type=str,
                            help='Search location (default: %(default)s)')
        import pdb; pdb.set_trace()#デバッグ
        input_values = parser.parse_args() #requestを受け取ってる？<-たぶん
        '''
        if(request.method == 'POST'):
            term = DEFAULT_TERM
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
        except KeyError:
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
        # どのように使うのかわからないのでコメントアウト
        # response = self.get_business(API_KEY, business_id)

        print(u'Result for business "{0}" found:'.format(business_id))
        pprint.pprint(response, indent=2)
        return response

        # どうやって使うのかわからないメソッド
    def get_business(self, api_key, business_id):
        """Query the Business API by a business ID.

        Args:
            business_id (str): The ID of the business to query.

        Returns:
            dict: The JSON response from the request."""

    #    business_path = BUSINESS_PATH + business_id

    #    return request(API_HOST, business_path, api_key)

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
