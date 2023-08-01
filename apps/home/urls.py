from apps.home import views
from django.urls import path, re_path
from apps.home.views import Fluid, Ada
from apps.boletim.views import Boletim_fluid

urlpatterns = [
    # Dashboards
    path("/dash-fluid", Fluid.as_view(), name="dash-fluid"),
    path("/dash-ada", Ada.as_view(), name="dash-ada"),

    # Boletins
    path("/boletim-fluid", Boletim_fluid.as_view(), name="boletim-fluid"),

    path('', views.index, name='home'),
    re_path(r'^.*\.*', views.pages, name='pages'),
    ]
