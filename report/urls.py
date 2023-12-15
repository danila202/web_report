from django.urls import path, include
from . import views

app_name = 'report'

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search_fence, name='search'),
    path("select2/", include("django_select2.urls")),

]
