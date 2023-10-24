import json
from .forms import DateForm
from django import template
from django.views import View
from django.urls import reverse
from django.template import loader
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from .data.fluid.sql_server import  get_amostras_status
from .data.ada.postgresql import  get_cliente_ativos
from .data.ada.api_ada import get_sector, get_devices


class Fluid(View):

    def get(self, request):

        context = {}
        dados,meses_unicos = get_amostras_status()

        context = {
            'datas': meses_unicos,
            'grupos': dados,
        }
        
        context['form'] = DateForm()

        return render(request, 'dashboard/fluid/base/dash-fluid.html', context)

    def post(self, request):

        context = {}

        form = DateForm(request.POST)

        if form.is_valid():
            request.POST.get('')
        else:
            context['errors'] = form.errors

        return JsonResponse(context)


class Ada(View):

    def get(self, request):

        context = {}

        clientes = get_cliente_ativos()

        context['form'] = DateForm()

        context = {
            "clientes" : clientes,
        }
        
        return render(request, 'dashboard/ada/dash-ada.html', context)

    def post(self, request):

        context = {}

        data = json.loads(request.body)

        get_client = data.get("id_cliente", None)
        get_client_sub = data.get("sectorId", None)

        if get_client is not None:

            sector_names = get_sector(get_client)

            request.session['client_id'] = get_client

            # print(sector_names)
            context = {
                "sector_names":sector_names,
            }
            
        if get_client_sub is not None:
            # print(f"teste {get_client_sub}")
            id_cliente = request.session.get('client_id')

            devices, data_conn, consistencia_dados, hidraulioc, correlation_matrix = get_devices(get_client_sub, id_cliente)
            # print(f"teste  = {devices}")
            # print(f"teste  = {data_conn}")
            # print(f"teste  = {consistencia_dados}")
            # print(f"teste  = {hidraulioc}")

            context = {
                "correlation_matrix":correlation_matrix,
                "sector_names" : None,
                "hidraulioc": hidraulioc,
                "devices" : devices,
                "devices_conn":data_conn,
                "consistencia_dados":consistencia_dados,
            }

        return JsonResponse(context)


@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}
    context['form'] = DateForm()

    # html_template = loader.get_template('dashboard/fluid/base/dash-fluid.html')
    html_template = loader.get_template('layouts/base.html')

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
