from django.urls import path
from . import views

app_name = 'agentportal'

urlpatterns = [
        path('', views.index, name='index'),
	path('showDeliveries', views.showDeliveries, name='showDeliveries'),
]

