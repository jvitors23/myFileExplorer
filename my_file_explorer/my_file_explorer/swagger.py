from drf_yasg.generators import OpenAPISchemaGenerator
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings


class BothHttpAndHttpsSchemaGenerator(OpenAPISchemaGenerator):
    def get_schema(self, request=None, public=False):
        schema = super().get_schema(request, public)
        if settings.DEBUG:
            schema.schemes = ["http"]
        else:
            schema.schemes = ["https"]
        return schema


schema_view = get_schema_view(
   openapi.Info(
      title="MyFileExplorer API",
      default_version='v1',
      description="API for access custom filesystem",
      contact=openapi.Contact(email="jvss23031999@gmail.com"),
      license=openapi.License(name="MIT License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
   generator_class=BothHttpAndHttpsSchemaGenerator,
)
