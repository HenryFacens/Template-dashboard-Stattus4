from django import template
from django.views import View
from django.urls import reverse
from django.template import loader
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect

class Fluid(View):

    def get(self, request):

        context = {}

        return render(request, 'dashboard/fluid/dash-fluid.html', context)

    def post(self, request):

        context = {}

        return JsonResponse(context)
    

class Ada(View):

    def get(self, request):

        context = {}

        return render(request, 'dashboard/ada/dash-ada.html', context)

    def post(self, request):

        context = {}

        return JsonResponse(context)


@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('dashboard/fluid/dash-fluid.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))
