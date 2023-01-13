from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.home, name='stockpicker'),
    path('stocklist/', views.StockListView.as_view()),
]