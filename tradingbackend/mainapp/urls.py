from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.stockPicker, name='stockpicker'),
    path('stocklist/', views.StockListView.as_view()),
]