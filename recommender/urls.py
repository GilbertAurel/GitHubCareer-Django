from django.urls import path
from .views import home_view, get_all_job_view, get_value_view

app_name = 'recommender'

urlpatterns = [
    path('', home_view),
    path('home/', home_view),
    path('result/', get_value_view),
    path('all/', get_all_job_view),
]