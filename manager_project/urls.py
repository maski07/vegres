"""manager_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
# from django.urls import include, path

import manager.views as manager_view
import manager.homeView as manager_homeView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # url(r'', 'django.views.generic.simple.redirect_to', {'url': '/home/'}),
    url(r'home/', manager_homeView.Home.as_view(), name='home'),
    url(r'^searchResult/', manager_view.SearchYelpRestaurant.as_view(), name='searchResult')
]
'''
urlpatterns = [
    path('admin/', admin.site.urls),
    path('searchResult/', manager_view.SearchYelpRestaurant, name = 'searchResult')
]
'''
