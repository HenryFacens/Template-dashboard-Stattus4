import json
from django.views import View
from django.shortcuts import render
from django.http import JsonResponse
from apps.home.forms import DateForm
from apps.home.data.fluid.sql_server import group_clients,total_de_coletas


class Boletim_fluid(View):

    def get(self, request):

        context = {}

        dados = {}

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
        date1 = data.get('date_1', None)
        date2 = data.get('date_2', None)

        date_1_pdf = "/".join(date1.split("-")[::-1]) if date1 else None
        date_2_pdf = "/".join(date2.split("-")[::-1]) if date2 else None

        form = DateForm(data={'date_1': date1, 'date_2': date2})

        if form.is_valid() and get_client:
            
            date1 = form.cleaned_data.get('date_1').isoformat() + ' 00:00:00'
            date2 = form.cleaned_data.get('date_2').isoformat() + ' 23:59:59'

            coletas_totais = total_de_coletas(get_client,date1,date2)

            context = {
                't_coletas':coletas_totais, 
                'date_1': date_1_pdf,
                'date_2': date_2_pdf,

            }

            return JsonResponse(context)

        else:
            print(form.errors)
            return JsonResponse({'error': 'Invalid data'})
