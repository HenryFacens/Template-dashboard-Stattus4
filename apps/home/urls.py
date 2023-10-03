from apps.home import views
from django.urls import path, re_path
from apps.home.views import Fluid, Ada
from apps.boletim.views import Boletim_fluid, JSON_Boletim_pdf, Boletim_pdf, Boletim_ada, Boletim_pdf_ada, JSON_Boletim_pdf_ada

urlpatterns = [
    # Dashboards
    path("dash-fluid/", Fluid.as_view(), name="dash-fluid"),
    path("dash-ada/", Ada.as_view(), name="dash-ada"),

    # Boletins
    path("boletim-fluid/", Boletim_fluid.as_view(), name="boletim-fluid"),
    path('boletim_json/', JSON_Boletim_pdf.as_view(), name='boletim_json'),
    path('boletim-pdf-fluid/', Boletim_pdf.as_view(), name='boletim-pdf-fluid'),
    path("boletim-ada/", Boletim_ada.as_view(), name="boletim-ada"),
    path('boletim-pdf-ada/', Boletim_pdf_ada.as_view(), name='boletim-pdf-ada'),
    path('boletim_json_ada/', JSON_Boletim_pdf_ada.as_view(), name='boletim_json'),

    # Pages
    path('', views.index, name='home'),
    re_path(r'^.*\.*', views.pages, name='pages'),
    ]
