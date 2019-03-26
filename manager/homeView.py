from django.shortcuts import render
from django.views.generic import TemplateView


class Home(TemplateView):
    # views.pyに統合したい

    HOME = "home.html"
    def get(self, request, *args, **kwargs):

        # context['restaurant'] = response  # 入れ物に入れる
        params = {
            'title': 'Vegetable'
        }

        return render(self.request, self.HOME, params)
