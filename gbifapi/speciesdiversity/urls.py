from django.urls import path
from . import views

app_name = 'speciesdiversity'
urlpatterns = [
    path("", views.index, name="index"),
    path('speciesdiversity/', views.speciesdiversity, name='speciesdiversity'),
    path('speciesdata/<str:country_code>/', views.species_data_view, name='species_data'),
    path('species_data_view/', views.species_data_view, name='species_data_view'),

]
