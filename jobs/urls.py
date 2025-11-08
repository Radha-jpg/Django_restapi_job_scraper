from django.urls import path
from .views import login_view
from .api import scrape_and_save_jobs, get_saved_jobs

urlpatterns = [
    path('login/', login_view, name='login'),
    path('jobs/scrape/', scrape_and_save_jobs, name='scrape_and_save_jobs'),
    path('jobs/', get_saved_jobs, name='get_saved_jobs'),
]
