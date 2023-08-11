from django.urls import re_path, include

urlpatterns = (
    re_path("", include(("api.licenses.urls", "api"), namespace="api_v1")),
)