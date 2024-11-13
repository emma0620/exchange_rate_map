from django.urls import path

from . import views

app_name = "pages"

urlpatterns = [
    path("", views.index, name="index"),
    path("exchange", views.exchange_calculation, name="exchange_calculation"),
    path("rate_history/<str:currency>/", views.rate_history, name="rate_history"),
    path("about", views.about, name="about"),
]
