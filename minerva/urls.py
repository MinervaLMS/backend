from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.documentation import include_docs_urls

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("accounts.urls")),  # Include accounts urls
    path("", include("courses.urls")),  # Include courses urls
    path("", include("social.urls")),  # Include social urls
    path("", include("ioc.urls")), # Include ioc urls
    path(
        "docs/", include_docs_urls(title="Minerva API")
    ),  # Route for API documentation
] + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)  # Serve an url for any media file
