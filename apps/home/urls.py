from apps.home import views
from django.urls import path, re_path
from apps.home.views import Fluid

urlpatterns = [
    path("/dash-fluid", Fluid.as_view(), name="dash-fluid"),
    path('', views.index, name='home'),
    re_path(r'^.*\.*', views.pages, name='pages'),
    
    ]
