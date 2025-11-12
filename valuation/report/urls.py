from django.urls import path
from . import views

app_name = 'report'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('reports/', views.valuation_list, name='valuation_list'),
    path('reports/create/', views.valuation_create, name='valuation_create'),
    path('reports/<int:pk>/', views.valuation_detail, name='valuation_detail'),
    path('properties/', views.property_list, name='property_list'),
    path('properties/add/<int:valuation_pk>/', views.property_add, name='property_add'),
    path('properties/<int:pk>/edit/', views.property_edit, name='property_edit'),
    path('plots/', views.plot_list, name='plot_list'),
    path('owners/', views.owner_list, name='owner_list'),
]