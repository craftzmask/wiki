from django.urls import path

from . import views

app_name = 'encyclopedia'

urlpatterns = [
    path('', views.index, name='index'),
    path('wiki/<str:title>', views.view_entry, name='view_entry'),
    path('search/', views.search, name='search'),
    path('create/', views.create, name='create'),
    path('edit/<str:title>', views.edit, name='edit')
]
