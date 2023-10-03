import json
from django.views import View
from django.shortcuts import render
from django.http import JsonResponse
from apps.home.forms import DateForm
from apps.home.data.fluid.sql_server import group_clients,total_de_coletas
from apps.home.data.ada.postgresql import  get_cliente_ativos 
from apps.home.data.ada.api_ada import get_sector, get_devices_ada, get_alarmes, get_press

class Boletim_fluid(View):

    def get(self, request):

        context = {}

        cliente = group_clients()

        context = {
            'cliente': cliente,
        }
        context['form'] = DateForm()

        return render(request, 'boletim/fluid/boletim-fluid.html', context)

    def post(self, request):

        context = {}
        form = DateForm(request.POST)
        data = json.loads(request.body)

        get_client = data.get('id', None)

        get_name = data.get('name', None)

        date1 = data.get('date_1', None)
        date2 = data.get('date_2', None)

        date_1_pdf = "/".join(date1.split("-")[::-1]) if date1 else None
        date_2_pdf = "/".join(date2.split("-")[::-1]) if date2 else None

        form = DateForm(data={'date_1': date1, 'date_2': date2})

        if form.is_valid() and get_client:
            
            date1 = form.cleaned_data.get('date_1').isoformat() + ' 00:00:00'
            date2 = form.cleaned_data.get('date_2').isoformat() + ' 23:59:59'

            coletas_totais, pontos, classes = total_de_coletas(get_client,date1,date2)

            print(get_name)

            context = {
                'clientNm': get_name,
                'classes' : classes,
                'pontos' : pontos,
                't_coletas':coletas_totais, 
                'date_1': date_1_pdf,
                'date_2': date_2_pdf,

            }

            request.session['context'] = context

            return JsonResponse(context)

        else:
            print(form.errors)
            return JsonResponse({'error': 'Invalid data'})
        
    def process_data(self, request):

        context = request.session.get('context', None)

        return context

class Boletim_pdf(Boletim_fluid):

    def get(self, request):
        context = self.process_data(request)

        return render(request, 'boletim/fluid/context/boletim_pdf.html', {'context': context})


class JSON_Boletim_pdf(Boletim_fluid):

    def get(self, request):

        context = self.process_data(request)

        return JsonResponse({'context': context})
    

class Boletim_ada(View):

    def get(self,request):
        
        clientes = get_cliente_ativos()

        context = {
            "clientes" : clientes,
        }
        context['form'] = DateForm()

        print(context)
        return render(request, 'boletim/ada/boletim-ada.html', context)

    def post(self,request):

        context = {}

        form = DateForm(request.POST)
        data = json.loads(request.body)

        get_client = data.get("id_cliente", None)
        get_client_sub = data.get("sectorId", None)
        
        date1 = data.get('date_1', None)
        date2 = data.get('date_2', None)
        date_1_pdf = "/".join(date1.split("-")[::-1]) if date1 else None
        date_2_pdf = "/".join(date2.split("-")[::-1]) if date2 else None

        form = DateForm(data={'date_1': date1, 'date_2': date2})

        if get_client is not None:

            sector_names = get_sector(get_client)

            request.session['client_id'] = get_client

            print(sector_names)
            context = {
                "sector_names":sector_names,
            }

        if form.is_valid() :
            if get_client_sub is not None:
                date1 = form.cleaned_data.get('date_1').isoformat() + ' 00:00:00'
                date2 = form.cleaned_data.get('date_2').isoformat() + ' 23:59:59'
                id_cliente = request.session.get('client_id')

                hidraulioc = get_devices_ada(get_client_sub, id_cliente,date1,date2)
                
                alarmes = get_alarmes(get_client_sub,id_cliente,date1,date2)
                pressao = get_press(get_client_sub,id_cliente,date1,date2)

                context = {
                    "alarmes" : alarmes,
                    "pressao" : pressao,
                    "sector_names" : None,
                    "hidraulioc": hidraulioc,
                    'date_1': date_1_pdf,
                    'date_2': date_2_pdf,
                }
            request.session['context'] = context

            return JsonResponse(context)
        
    def process_data(self, request):

        context = request.session.get('context', None)

        return context
    
class JSON_Boletim_pdf_ada(Boletim_ada):

    def get(self, request):

        context = self.process_data(request)

        return JsonResponse({'context': context})
    
class Boletim_pdf_ada(Boletim_ada):

    def get(self, request):
        context = self.process_data(request)

        return render(request, 'boletim/ada/context/boleteim-pdf-ada.html', {'context': context})