from django.views import View
from django.shortcuts import render
from django.http import JsonResponse

class Boletim_Fluid(View):

    def get(self, request):

        context = {}

        return render(request, 'dashboard/fluid/dash-fluid.html', context)

    def post(self, request):

        context = {}

        return JsonResponse(context)