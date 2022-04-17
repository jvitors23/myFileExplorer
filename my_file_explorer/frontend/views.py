from django.contrib.auth.views import TemplateView


class LoginView(TemplateView):

    template_name = "login.html"


class IndexView(TemplateView):

    template_name = "index.html"
