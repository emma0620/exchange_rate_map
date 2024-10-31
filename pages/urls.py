from . import views
from django.urls import  path
app_name = "pages"

urlpatterns = [
    path("", views.index, name="index"),
    path("exchange",views.exchange_calculation, name="exchange_calculation"),
    path("about", views.about, name="about"),

]
