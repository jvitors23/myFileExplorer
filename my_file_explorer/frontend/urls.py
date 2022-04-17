from django.urls import path
from frontend import views


urlpatterns = [
    path("login/", views.LoginView.as_view(), name="front_login"),
    path("", views.IndexView.as_view(), name="folder_index"),
    # path("register/", RegisterView.as_view(), name="logout"),

]