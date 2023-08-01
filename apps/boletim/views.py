from django.views import View
from django.shortcuts import render
from django.http import JsonResponse
from apps.home.forms import DateForm


class Boletim_fluid(View):

    def get(self, request):

        context = {}

        context['form'] = DateForm()

        return render(request, 'boletim/fluid/boletim-fluid.html', context)

    def post(self, request):

        context = {}

        form = DateForm(request.POST)

        if form.is_valid():
            request.POST.get('')
        else:
            context['errors'] = form.errors

        return JsonResponse(context)
