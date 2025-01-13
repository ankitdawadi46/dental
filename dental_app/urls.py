"""
URL configuration for dental_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from dental_app.views import error_api

urlpatterns = [
    path("admin/", admin.site.urls),
    path("client/", include("client.urls", namespace="client")),
    path("users/", include("users.urls", namespace="users")),
    path("notice/", include("notice.urls", namespace="notice")),
    path("leave/", include("leave.urls", namespace="leave")),
    path("stock/", include("stock.urls", namespace="stock")),
    path("medical-history/", include("medical_history.urls", namespace="medical_history")),
    path(
        "dental-structure/",
        include("dental_structure.urls", namespace="dental_structure"),
    ),
    path("dental-plan/", include("dental_plan.urls", namespace="dental_plan")),
    path("office/", include("office.urls", namespace="office")),
    path("error-api/", error_api, name="error_api")
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
